"Prediction Module"
import logging
from multiprocessing import process
from pathlib import Path
from typing import List, Tuple

import numpy as np
import rasterio
from rasterio.windows import Window

from classifier.settings import US_ALGORITHMS
from classifier.timeseries import get_timeseries_samples
from classifier.utils.config import Configuration
from classifier.utils.general import write_tifs
from classifier.utils.raster import iterate_rasters_for_data

# need to set the temp dir for multiprocessing in a container
process.current_process()._config['tempdir'] = '/tmp/'

# Load all rasters in a windowed manner (in a vrt) and do the prediction
PREDICT_LOGGER = logging.getLogger(__name__)


def prediction_class_probabilities(
        predicted: np.ndarray, valid: np.ndarray, meta: dict,
        config: Configuration, window: Window) -> None:
    """Gets probability for the classified class and writes the tif for a
    windows

    Args:
        predicted (np.ndarray): The probabilities for all classes
        valid (np.ndarray): Array with valid values for prediction
        meta (dict): rasterio meta for writing tif
        config (Configuration)class): Contains config
        window (rasterio.Window) to predict and write

    """
    labels_internal_proba = (np.nanmax(predicted, axis=1)
                             .astype(np.float32))
    result_proba = np.full(valid.shape, -9999, np.float32)
    result_proba[valid] = labels_internal_proba
    write_tifs(config.tmp_dir / 'probability',
               window,
               meta['dst_proba_meta'],
               result_proba)


def prediction_all_probabilities(
        predicted: np.ndarray,
        valid: np.ndarray,
        labels: dict,
        meta: dict,
        config: Configuration,
        window: Window) -> None:
    """Gets probability for the classified class and writes the tif for a
    windows

    Args:
        predicted (np.ndarray): The probabilities for all classes
        valid (np.ndarray): Array with valid values for prediction
        labels (dict): Conversion dictionary for labels
        meta (dict): rasterio meta for writing tif
        config (Configuration)class): Contains config
        window (rasterio.Window): processing window

    """
    # loop over the classes and save them all separately
    for internal_label in range(predicted.shape[1]):
        probabilities = predicted[:, internal_label]
        result_proba = np.full(valid.shape, -9999, np.float32)
        result_proba[valid] = probabilities
        write_tifs(
            config.tmp_dir / str(labels[internal_label]),
            window,
            meta['dst_proba_meta'],
            result_proba)


def do_prediction_proba_su(
        data: np.ndarray, valid: np.ndarray, model_dict: dict,
        config: Configuration, meta: dict, window: Window) -> np.ndarray:
    """Does the actual prediction and probability description for supervised
    methods

    Args:
        data (np.ndarray): Features
        valid (np.ndarray): Valid values for prediction
        model_dict (dict): The model dictionary containing model and
            algorithm info
        config (Configuration): The cli configuration
        meta (dict): rasterio meta for writing tif
        window (rasterio.window): asterio Window for which to do the prediction

    Returns:
        The predictions array

    """
    predicted = model_dict['model'].predict_proba(data)
    # Get the final indices of the highest probabilities
    labels_external = np.nanargmax(predicted, axis=1)

    # Label keys to int
    model_dict['labels'] = {
        int(k): int(v) for k, v in
        model_dict['labels'].items()
    }
    # Indices need to be transformed to the proper labels
    labels_transformed = np.vectorize(
        model_dict['labels'].get)(labels_external)
    result = np.full(valid.shape, -9999, np.int32)
    result[valid] = labels_transformed

    # See if we need to output some of the modelled probabilities
    if config.supervised.probability:
        prediction_class_probabilities(
            predicted,
            valid,
            meta,
            config,
            window
        )
    if config.supervised.all_probabilities:
        prediction_all_probabilities(
            predicted,
            valid,
            model_dict['labels'],
            meta,
            config,
            window
        )

    return result


def do_prediction_proba(
        data: np.ndarray, valid: np.ndarray, model_dict: dict,
        config: Configuration, meta: dict, window: Window) -> np.ndarray:
    """Calls the actual probability functions for (un)supervised
    methods

    Args:
        data (np.ndarray): Features
        valid (np.ndarray): Valid values for prediction
        model_dict (dict): The model dictionary containing model and
        algorithm info
        config (Configuration): The cli configuration
        meta (dict): rasterio meta for writing tif
        window: The rasterio Window for which to do the prediction

    Returns:
        The probability array

    """
    if config.app.algorithm == 'singleclass':
        result = predict_single_class(
            data,
            valid,
            model_dict,
            config,
            meta,
            window
        )
        return result
    return do_prediction_proba_su(data,
                                  valid,
                                  model_dict,
                                  config,
                                  meta,
                                  window)


def gather_data_for_prediction(rasters: List[Path],
                               meta: dict, config: Configuration,
                               window: Window) -> Tuple[np.ndarray, np.ndarray]:
    """ Gather all the data from the input rasters and return validity raster

    Args:
        raster (List[str]): Rasters
        meta (dict): rasterio meta for writing tif
        prediction_dict (dict): Parameters for the prediction
        window (rasterio.window): window of the chunk to predict

    Returns:
        data (np.ndarray): Array with data for prediction
        valid (np.ndarray): Validity array
    """
    with rasterio.open(rasters[0], 'r') as first:
        f_data = first.read(window=window)
        # Set the correct sizes for output blocks and set the transformation
        for meta_type in ['dst_meta', 'dst_proba_meta']:
            meta[meta_type].update(
                width=f_data.shape[2],
                height=f_data.shape[1],
                transform=first.window_transform(window))

        # Create the data array
        data_array = np.zeros((meta['bandcount'],
                               f_data.shape[1],
                               f_data.shape[2]))

        data, valid = iterate_rasters_for_data(
            window,
            first,
            f_data,
            data_array,
            rasters,
            config
        )
        return data, valid


def gather_data_for_prediction_ts(
        rasters: List[Path],
        meta: dict,
        config: Configuration,
        window: Window) -> Tuple[np.ndarray, np.ndarray]:
    """Gathers all the data neccessary for a prediction using a raster TS

        Args:
            raster (List[Path]): Rasters
            meta (dict): rasterio meta for writing tif
            prediction_dict (dict): Parameters for the prediction
            window (rasterio Window): window of the chunk to predict
        Returns:
            data (np.array): Gathered and imputed data
            valid (np.array): Array with indices of locations of valid data
     """
    # Get all data in a df with pixels as columns and dates and bands as the
    # indices
    with rasterio.open(rasters[0], 'r') as src:
        shape = src.read(window=window).shape
        x_min, y_min, x_max, y_max = src.window_bounds(window)
        for meta_type in ['dst_meta', 'dst_proba_meta']:
            meta[meta_type].update(
                width=shape[2],
                height=shape[1],
                transform=src.window_transform(window))

    window_polygon = [[(x_min, y_min),
                       (x_min, y_max),
                       (x_max, y_max),
                       (x_max, y_min)]]

    rois = {'properties': {'id': 1},
            'geometry': {'coordinates': window_polygon,
                         'type': 'Polygon'}}

    pixel_data = get_timeseries_samples(rasters,
                                        rois,
                                        out_dir=None,
                                        config=config)
    data = pixel_data.transpose().values
    # All TS is imputed, so we assume that all data is valid.
    valid = np.ones(shape[1:], dtype=bool)
    return data, valid


def prediction(window: Window, rasters: List[Path], model_dict: dict,
               meta: dict, config: Configuration) -> None:
    """ Prediction for a window and save to a tmp file

    Args:
        window (rasterio.Window): A rasterio window
        rasters (List[Path]):  Rasters
        model_dict (dict): specifying the algorithm, model labels
        meta (dict): The meta files from source, destination and dest_proba
        config (Configuration)class): contains config
    """
    if config.app.rasters_are_timeseries:
        data, valid = \
            gather_data_for_prediction_ts(rasters, meta, config,  window)
    else:
        data, valid = \
            gather_data_for_prediction(rasters, meta, config, window)
    if not valid.any():
        return

    if not config.app.algorithm in \
            US_ALGORITHMS:
        result = do_prediction_proba(
            data,
            valid,
            model_dict,
            config,
            meta,
            window
        )
    else:
        labels_external = model_dict['model'].predict(data)
        result = np.full(valid.shape, -9999, np.int32)
        result[valid] = labels_external

    # Write the classification results to tifs
    write_tifs(config.tmp_dir / 'classification',
               window,
               meta['dst_meta'],
               result)


def predict_proba_single_class(
        data: np.ndarray, valid: np.ndarray, model_dict: dict,
        config: Configuration, meta: dict, window: Window) -> None:
    """Predict the probability for an array

    Args:
        data (np.ndarray): Features
        valid (np.ndarray): Valid values for prediction
        model_dict (dict): The model dictionary containing model and
        config (Configuration): The cli configuration
        meta (dict): rasterio meta for writing tif
        window: The rasterio Window for which to do the prediction

    Returns:
        None
    """
    meta.update(dtype=rasterio.dtypes.float32, nodata=-9999)
    result = np.full(valid.shape, -9999, np.float32)
    labels_internal_highest_p = model_dict['model'].decision_function(data)
    result_proba = result.copy().astype(np.float32)
    result_proba[valid] = labels_internal_highest_p

    write_tifs(config.tmp_dir / 'probability',
               window,
               meta["dst_proba_meta"],
               result_proba)


def predict_single_class(
        data: np.ndarray, valid: np.ndarray, model_dict: dict,
        config: Configuration, meta: dict, window: Window) -> np.ndarray:
    """Predict the probability for an array

    Args:
        data (np.ndarray): Features
        valid (np.ndarray): Valid values for prediction
        model_dict (dict): The model dictionary containing model and
            algorithm info
        config (Configuration): The cli configuration
        meta (dict): rasterio meta for writing tif
        window: The rasterio Window for which to do the prediction

    Returns:
        predicted array

    """
    # Get the final classification of the highest probabilities
    predicted = model_dict['model'].predict(data)

    result = np.full(valid.shape, -9999, np.int32)

    # See if we need to output some of the modelled probabilities
    if config.supervised.probability:
        predict_proba_single_class(data,
                                   valid,
                                   model_dict,
                                   config,
                                   meta,
                                   window)
    result[valid] = predicted
    return result

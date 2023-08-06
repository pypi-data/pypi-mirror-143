"""An sk-learn classifier for landcover classification"""

import logging
import shutil
import sys
import time
from pathlib import Path
from typing import Any, List, Optional

import fiona
import pandas as pd

from classifier.accuracy import (plot_feature_importances,
                                 write_confusion_matrix)
from classifier.dataprep import createdataset, outlier_removal
from classifier.predict import prediction
from classifier.settings import US_ALGORITHMS
from classifier.timeseries import get_timeseries_samples
from classifier.train import train_dataset
from classifier.unsupervised import make_input_array, train_kmeans
from classifier.utils.config import Configuration
from classifier.utils.general import parallel_function, read_model, save_model
from classifier.utils.raster import get_meta, stitch


START = time.time()
CLASSIFIER_LOGGER = logging.getLogger(__name__)


def read_samples(samples: Path, remove_outliers: bool = True) -> pd.DataFrame:
    """Read a samples file.

    Args:
        samples (Path): CSV file containing samples
        remove_outliers (Bool): Flag for removing outliers from samples

    Returns:
        sample_df (pd.DataFrame): DF containing samples

    """
    sample_df = pd.read_csv(samples, index_col=0)
    if remove_outliers:
        sample_df = outlier_removal(sample_df)
    return sample_df


def get_rois_extent(rois: Path) -> Any:
    """

    Args:
        rois (Path): path to a rois file

    Returns:
        bounds of rois (list): ulx, uly, llx, lly coordinates

    """
    with fiona.open(rois, "r") as shapefile:
        return shapefile.bounds


def gather_samples(
        rois: Path, rasters: List[Path],
        out_dir: Path, config: Configuration) -> pd.DataFrame:
    """Gather samples from a rois file and raster files

    Args:
        rois (Path): The path to a rois file
        rasters (List[Path]): A list of raster files
        out_dir (Path): Path where to write the dataset file
        config (Configuration): contains config

    Returns:
        samples (pd.DataFrame): containing pixel values and classes
    """
    # Train a model and continue
    samples = createdataset(
        rasters,
        rois,
        out_dir,
        config)
    samples.to_csv(out_dir / 'samples.csv')
    return samples


def train(samples: pd.DataFrame, rasters: List[Path], out_dir: Path,
          config: Configuration, rois_extent: List[float] = None) -> dict:
    """Train a model using samples and rasters

    Args:
        samples (pd.DataFrame): Samples dataframe containing pixel
            values and class values
        rasters (List[Path]): A list of raster files
        out_dir (Path): Path where to write the dataset file
        config (Configuration): contains config
        rois_extent (List[float]): The extent of the training data

    Returns:
        model_dict (dict): Containing the name, model and label
                           encoder.
    """
    CLASSIFIER_LOGGER.info("\n####-----Training----#####\n")
    dataset = samples
    windows, _ = get_meta(rasters, config.app.window)
    if config.app.algorithm in US_ALGORITHMS and len(samples) < 1:
        # Do unsupervised
        array = make_input_array(
            rasters,
            windows,
            config
        )
        model_dict = train_kmeans(array,
                                  config)
    else:  # All supervised methods
        model_dict, test = train_dataset(
            dataset,
            config.app.algorithm,
            out_dir,
            config
        )
        if config.app.algorithm in ['randomforest', 'xgboost'] \
                and config.accuracy.perform_assesment:
            # Do the accuracy analysis
            cm_fn = out_dir / 'confusion_matrix'
            fi_fn = out_dir / 'feature_importance.png'
            write_confusion_matrix(model_dict, test, cm_fn)
            plot_feature_importances(model_dict, fi_fn)
    # save the model as a python pickle
    if not rois_extent is None:
        model_dict['rois_bounds'] = rois_extent
    if config.app.model_save:
        save_model(model_dict, out_dir, config)
    CLASSIFIER_LOGGER.info("\nFinished Training\n")
    return model_dict


def predict(
        model_dict: dict, rasters: List[Path],
        out_dir: Path, config: Configuration) -> None:
    """Prediction function using a trained model and raster files

    Args:
        model_dict (dict): Containing the name, model and label
                        encoder.
        rasters (List[Path]): A list of raster files
        out_dir (Path): Path where to write the dataset file
        config (Configuration): contains config
    """
    threads = config.app.threads
    CLASSIFIER_LOGGER.info("\n####-----Prediction----#####\n")
    windows, meta = get_meta(rasters, config.app.window)

    # Set model n_jobs to 1 for prediction
    if 'n_jobs' in model_dict['model'].get_params():
        model_dict['model'] = \
            model_dict['model'].set_params(**{'n_jobs': 1})

    iterable = [
        {
            'window': window[1],
            'rasters': rasters,
            'model_dict': model_dict,
            'meta': meta,
            'config': config
        }
        for window in windows
    ]
    if threads > 1 or threads == -1:
        parallel_function(prediction,
                          iterable,
                          threads)
    else:
        for wins in iterable:
            prediction(**wins)

    # ##--------------------STITCHING-----------------------------------###

    CLASSIFIER_LOGGER.info("\n####-----Stitching----#####\n")

    # Run the gdalwarp command in the command line
    stitch(out_dir, meta, config)
    CLASSIFIER_LOGGER.info("Cleaning up..")
    shutil.rmtree(config.tmp_dir)
    CLASSIFIER_LOGGER.info(
        "Total run time was %i seconds", (int(time.time() - START)))


def train_and_predict_with_samples(samples: pd.DataFrame, rasters: List[Path],
                                   out_dir: Path, config: Configuration,
                                   rois_extent: List[float] = None) -> None:
    """Train model using samples

    Args:
        samples (pd.DataFrame): Samples dataframe containing pixel values
            and class values
        rasters (List[Path]): A list of raster files
        out_dir (Path): Path where to write the dataset file
        config (Configuration): contains config
        rois_extent (List[float]): The extent of the training data
    """
    model_dict = train(samples, rasters, out_dir, config, rois_extent)
    predict(model_dict, rasters, out_dir, config)


def gather_train_predict_rois(
        rois: Path, rasters: List[Path],
        out_dir: Path, config: Configuration) -> None:
    """Gather samples from rois file and rasters and continue with training and
    prediction

    Args:
        rois (Path): The path to a rois file
        rasters (List[Path]): A list of raster files
        out_dir (Path): Path where to write the dataset file
        config (Configuration): contains config

    Returns:
        The return value. True for success, False otherwise.

    """
    samples = gather_samples(rois, rasters, out_dir, config)
    rois_extent = get_rois_extent(rois)
    return train_and_predict_with_samples(samples,
                                          rasters,
                                          out_dir,
                                          config,
                                          rois_extent)


def classify_(
        rasters: List[Path], config: Configuration,
        out_dir: Path, rois: Optional[Path] = None) -> None:
    """Entry point function for pixel-based classification

        Args:
            rasters (List[Path]): A list of raster files
            config (Configuration): contains config
            out_dir (Path): Path where to write the dataset file
            rois (Path): The path to a rois file

    """
    if config.app.model is not None:
        model = read_model(config.app.model)
        predict(model, rasters, out_dir, config)
    if config.app.algorithm not in US_ALGORITHMS:
        print(config.app.algorithm)
        # Supervised classification
        if config.app.samples is not None:

            samples = read_samples(
                config.app.samples,
                config.supervised.remove_outliers)

            train_and_predict_with_samples(samples,
                                           rasters,
                                           out_dir,
                                           config)

        elif rois is not None:
            gather_train_predict_rois(
                rois,
                rasters,
                out_dir,
                config)
        else:
            CLASSIFIER_LOGGER.error(
                "You have chosen a supervised classification method but didn't "
                "provide rois or samples. Either provide one of these or run a "
                "unsupervised classification")
            sys.exit(1)
    else:
        if config.app.samples is not None or rois is not None:
            CLASSIFIER_LOGGER.error(
                "You have chosen an unsupervised classification "
                "method but provided samples or rois. Please choose "
                "a supervised method to use them or don't provide them for "
                "an unsupervised classification.")
            sys.exit(1)
        CLASSIFIER_LOGGER.info("Doing unsupervised classification")
        train_and_predict_with_samples([],
                                       rasters,
                                       out_dir,
                                       config)


def classify_timeseries(rasters: List[Path],
                        config: Configuration,
                        out_dir: Path,
                        rois: Path) -> None:
    """Main function to classifiy timeseries.

    For now, only from start to finish is supported. ie, supplying a model
    or samples does not work.

        Args:
            rasters (List[Path]): List of raster paths
            config (Configuration): contains config
            out_dir (Path): Path to output directory
            rois (Path): Path to rois file

    """
    # Gather samples and do imputation.
    CLASSIFIER_LOGGER.info("Now Getting Samples and doing imputation")
    if rois is None:
        CLASSIFIER_LOGGER.error(
            "You have to provide rois for timeseries classification.")
        sys.exit()
    samples_df = get_timeseries_samples(rasters, rois, out_dir, config)
    # Reshape it
    samples = samples_df.T
    samples['class'] = samples.index
    if config.app.algorithm in US_ALGORITHMS:
        CLASSIFIER_LOGGER.error(
            "Unsupervised classification not supported yet")
        sys.exit()
    model = train(samples,
                  rasters=rasters,
                  out_dir=out_dir,
                  config=config,
                  rois_extent=None)

    predict(model, rasters, out_dir, config)


if __name__ == "__main__":
    pass

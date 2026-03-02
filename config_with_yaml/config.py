# -*- coding: utf-8 -*-

__author__ = "aitormf"

import logging
import os
import warnings
import yaml
from .properties import Properties
from .loader import Loader

LOGGER = logging.getLogger(__name__)


def findConfigFile(filename):
    """
    Returns filePath or None if it couldn't find the file

    @param filename: Name of the file

    @type filename: String

    @return String with path or None

    """
    warnings.warn(
        "config.findConfigFile() is deprecated, use Loader.find_config_file() instead.",
        DeprecationWarning,
        stacklevel=2,
    )

    loader = Loader()
    return loader.find_config_file(filename)


def load(filename):
    """
    Returns the configuration as dict

    @param filename: Name of the file

    @type filename: String

    @return a dict with propierties reader from file

    """
    warnings.warn(
        "config.load() is deprecated, use Loader class instead. "
        "Create a Loader instance and call load() on it.",
        DeprecationWarning,
        stacklevel=2,
    )

    loader = Loader()
    return loader.load(filename)

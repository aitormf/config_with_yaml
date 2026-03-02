# -*- coding: utf-8 -*-

__author__ = "aitormf"

import logging
import os
import yaml
from .properties import Properties


class Loader:
    """
    YAML configuration loader with support for !include tags.

    Allows loading YAML configuration files with the ability to include
    other YAML files using the !include tag. Includes are resolved relative
    to the current file's directory.

    Attributes:
        max_include_depth: Maximum depth for nested includes (default: 5)
        log_level: Logging level for the loader's logger
        config_paths: Additional paths to search for config files

    Example:
        >>> loader = Loader(max_include_depth=3, log_level=logging.INFO)
        >>> prop = loader.load("config.yml")
        >>> loader.load("base.yml").getProperty("database.host")
    """

    def __init__(self, max_include_depth=5, log_level=logging.DEBUG, config_paths=None):
        """
        Initialize the Loader.

        Args:
            max_include_depth: Maximum depth for nested !include tags (default: 5)
            log_level: Logging level for the loader's logger (default: DEBUG)
            config_paths: Additional colon-separated paths to search for config files
        """
        self.max_include_depth = max_include_depth
        self.log_level = log_level
        self.config_paths = config_paths
        self._current_depth = 0

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(log_level)

    def load(self, filename):
        """
        Load a YAML configuration file.

        Args:
            filename: Name or path to the YAML file

        Returns:
            Properties: A Properties object containing the loaded configuration

        Raises:
            ValueError: If the config file cannot be found
            yaml.YAMLError: If there's an error parsing the YAML file

        Example:
            >>> loader = Loader()
            >>> prop = loader.load("config.yml")
            >>> prop.getProperty("database.host")
        """
        self._current_depth = 0
        self._current_file_dir = None

        filepath = self.find_config_file(filename)

        if not filepath:
            raise ValueError(f"Config file '{filename}' could not be found")

        self.logger.info("Loading Config file %s", filepath)

        dir_path = os.path.dirname(os.path.abspath(filepath))
        self._current_file_dir = dir_path

        with open(filepath, "r") as stream:
            cfg = yaml.load(stream, Loader=self._create_loader_class(dir_path))
            return Properties(cfg)

    def find_config_file(self, filename):
        """
        Find a configuration file in the search paths.

        Searches in: current directory, then paths from config_paths env var,
        then paths provided in constructor.

        Args:
            filename: Name of the file to find

        Returns:
            str or None: Absolute path to the file if found, None otherwise
        """
        search_paths = ["."]

        config_paths_env = os.getenv("YAML_CONFIG_PATHS")
        if config_paths_env:
            search_paths.extend(config_paths_env.split(":"))

        if self.config_paths:
            search_paths.extend(self.config_paths.split(":"))

        for path in search_paths:
            file_path = os.path.join(path, filename)
            if os.path.exists(file_path):
                return os.path.abspath(file_path)

        return None

    def _create_loader_class(self, dir_path):
        """
        Create a custom loader class that handles !include tags.

        Args:
            dir_path: Directory path to resolve relative includes

        Returns:
            A custom YAML Loader class
        """

        class _CustomLoader(yaml.SafeLoader):
            pass

        _CustomLoader._parent_dir = dir_path
        _CustomLoader._loader = self

        def custom_include(loader, node):
            include_path = loader.construct_scalar(node)
            return loader._loader._load_include(include_path)

        yaml.add_constructor("!include", custom_include, Loader=_CustomLoader)

        return _CustomLoader

    def _load_include(self, include_path):
        """
        Load an included YAML file.

        Resolves the path relative to the parent file's directory and loads
        the YAML content. Supports nested includes up to max_include_depth.

        Args:
            include_path: Relative path to the included YAML file

        Returns:
            dict: The loaded configuration as a dictionary

        Raises:
            ValueError: If include depth exceeds max_include_depth or file not found
        """
        self._current_depth += 1

        if self._current_depth > self.max_include_depth:
            raise ValueError(
                f"Maximum include depth ({self.max_include_depth}) exceeded. "
                "Check for circular includes."
            )

        frame = self._current_file_dir or "."

        full_path = os.path.join(frame, include_path)
        full_path = os.path.normpath(full_path)

        if not os.path.exists(full_path):
            raise ValueError(
                f"Include file '{include_path}' not found at '{full_path}'"
            )

        self.logger.debug("Including file: %s", full_path)

        parent_dir = os.path.dirname(full_path)

        old_depth = self._current_depth
        old_file_dir = self._current_file_dir

        self._current_file_dir = parent_dir

        try:
            with open(full_path, "r") as stream:
                result = yaml.load(stream, Loader=self._create_loader_class(parent_dir))
        finally:
            self._current_depth = old_depth
            self._current_file_dir = old_file_dir

        return result

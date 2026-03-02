import pytest
import os
import sys
import logging

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config_with_yaml import Loader


class TestLoaderInit:
    def test_default_values(self):
        loader = Loader()
        assert loader.max_include_depth == 5
        assert loader.log_level == logging.DEBUG
        assert loader.config_paths is None

    def test_custom_max_depth(self):
        loader = Loader(max_include_depth=3)
        assert loader.max_include_depth == 3

    def test_custom_log_level(self):
        loader = Loader(log_level=logging.INFO)
        assert loader.log_level == logging.INFO

    def test_custom_config_paths(self):
        loader = Loader(config_paths="/path1:/path2")
        assert loader.config_paths == "/path1:/path2"


class TestLoaderLoad:
    def test_load_simple_yaml(self, tmp_path):
        test_file = tmp_path / "test.yml"
        test_file.write_text("key: value\nnested:\n  child: data")

        original_dir = os.getcwd()
        try:
            os.chdir(tmp_path)
            loader = Loader()
            prop = loader.load("test.yml")
            assert prop.getProperty("key") == "value"
            assert prop.getProperty("nested.child") == "data"
        finally:
            os.chdir(original_dir)

    def test_load_file_not_found(self):
        loader = Loader()
        with pytest.raises(ValueError) as exc_info:
            loader.load("nonexistent_file.yml")
        assert "could not be found" in str(exc_info.value)

    def test_load_returns_properties_object(self, tmp_path):
        test_file = tmp_path / "test.yml"
        test_file.write_text("key: value")

        original_dir = os.getcwd()
        try:
            os.chdir(tmp_path)
            loader = Loader()
            result = loader.load("test.yml")
            assert result.getNode() == {"key": "value"}
        finally:
            os.chdir(original_dir)

    def test_load_with_custom_paths(self, tmp_path):
        path1 = tmp_path / "path1"
        path1.mkdir()

        test_file = path1 / "custom.yml"
        test_file.write_text("key: custom_value")

        original_dir = os.getcwd()
        try:
            os.chdir(tmp_path)
            loader = Loader(config_paths=str(path1))
            prop = loader.load("custom.yml")
            assert prop.getProperty("key") == "custom_value"
        finally:
            os.chdir(original_dir)

    def test_load_complex_yaml(self, tmp_path):
        test_file = tmp_path / "complex.yml"
        test_file.write_text("""
database:
  host: localhost
  port: 5432
  settings:
    timeout: 30
    pool_size: 10
features:
  - feature_a
  - feature_b
""")

        original_dir = os.getcwd()
        try:
            os.chdir(tmp_path)
            loader = Loader()
            prop = loader.load("complex.yml")
            assert prop.getProperty("database.host") == "localhost"
            assert prop.getProperty("database.port") == 5432
            assert prop.getProperty("database.settings.timeout") == 30
            assert prop.getProperty("features") == ["feature_a", "feature_b"]
        finally:
            os.chdir(original_dir)


class TestLoaderFindConfigFile:
    def test_finds_file_in_current_directory(self, tmp_path):
        test_file = tmp_path / "test.yml"
        test_file.write_text("key: value")

        original_dir = os.getcwd()
        try:
            os.chdir(tmp_path)
            loader = Loader()
            result = loader.find_config_file("test.yml")
            assert result is not None
            assert os.path.exists(result)
        finally:
            os.chdir(original_dir)

    def test_returns_none_when_file_not_found(self):
        loader = Loader()
        result = loader.find_config_file("nonexistent_file_12345.yml")
        assert result is None

    def test_searches_multiple_paths_from_env(self, monkeypatch, tmp_path):
        path1 = tmp_path / "path1"
        path2 = tmp_path / "path2"
        path1.mkdir()
        path2.mkdir()

        test_file = path2 / "multi.yml"
        test_file.write_text("key: value")

        monkeypatch.setenv("YAML_CONFIG_PATHS", f"{path1}:{path2}")

        original_dir = os.getcwd()
        try:
            os.chdir(tmp_path)
            loader = Loader()
            result = loader.find_config_file("multi.yml")
            assert result == str(test_file)
        finally:
            os.chdir(original_dir)

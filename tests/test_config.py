import pytest
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config_with_yaml import config


class TestFindConfigFile:
    def test_finds_file_in_current_directory(self, tmp_path):
        test_file = tmp_path / "test.yml"
        test_file.write_text("key: value")

        original_dir = os.getcwd()
        try:
            os.chdir(tmp_path)
            result = config.findConfigFile("test.yml")
            assert result is not None
            assert os.path.exists(result)
        finally:
            os.chdir(original_dir)

    def test_returns_none_when_file_not_found(self):
        result = config.findConfigFile("nonexistent_file_12345.yml")
        assert result is None

    def test_finds_file_using_env_variable(self, monkeypatch, tmp_path):
        test_file = tmp_path / "env_test.yml"
        test_file.write_text("key: value")

        other_dir = tmp_path / "other"
        other_dir.mkdir()

        monkeypatch.setenv("YAML_CONFIG_PATHS", str(other_dir))

        original_dir = os.getcwd()
        try:
            os.chdir(tmp_path)
            result = config.findConfigFile(str(test_file))
        finally:
            os.chdir(original_dir)

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
            result = config.findConfigFile("multi.yml")
            assert result == str(test_file)
        finally:
            os.chdir(original_dir)


class TestLoad:
    def test_loads_valid_yaml_file(self, tmp_path):
        test_file = tmp_path / "test.yml"
        test_file.write_text("key: value\nnested:\n  child: data")

        original_dir = os.getcwd()
        try:
            os.chdir(tmp_path)
            prop = config.load("test.yml")
            assert prop.getProperty("key") == "value"
            assert prop.getProperty("nested.child") == "data"
        finally:
            os.chdir(original_dir)

    def test_load_raises_error_for_missing_file(self):
        with pytest.raises(ValueError) as exc_info:
            config.load("nonexistent_file_12345.yml")

        assert "could not be found" in str(exc_info.value)

    def test_load_returns_properties_object(self, tmp_path):
        test_file = tmp_path / "test.yml"
        test_file.write_text("key: value")

        original_dir = os.getcwd()
        try:
            os.chdir(tmp_path)
            result = config.load("test.yml")
            assert result.getNode() == {"key": "value"}
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
            prop = config.load("complex.yml")
            assert prop.getProperty("database.host") == "localhost"
            assert prop.getProperty("database.port") == 5432
            assert prop.getProperty("database.settings.timeout") == 30
            assert prop.getProperty("features") == ["feature_a", "feature_b"]
        finally:
            os.chdir(original_dir)

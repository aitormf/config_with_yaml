import pytest
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config_with_yaml.properties import Properties


class TestProperties:
    def test_getNode_returns_config(self):
        cfg = {"key": "value"}
        prop = Properties(cfg)
        assert prop.getNode() == cfg

    def test_getProperty_simple_key(self):
        cfg = {"key": "value"}
        prop = Properties(cfg)
        assert prop.getProperty("key") == "value"

    def test_getProperty_nested_key(self):
        cfg = {"parent": {"child": "value"}}
        prop = Properties(cfg)
        assert prop.getProperty("parent.child") == "value"

    def test_getProperty_deeply_nested(self):
        cfg = {"a": {"b": {"c": "deep"}}}
        prop = Properties(cfg)
        assert prop.getProperty("a.b.c") == "deep"

    def test_getProperty_returns_correct_types(self):
        cfg = {
            "string": "hello",
            "int": 42,
            "float": 3.14,
            "bool": True,
            "list": [1, 2, 3],
            "dict": {"nested": "value"},
        }
        prop = Properties(cfg)

        assert prop.getProperty("string") == "hello"
        assert prop.getProperty("int") == 42
        assert prop.getProperty("float") == 3.14
        assert prop.getProperty("bool") is True
        assert prop.getProperty("list") == [1, 2, 3]
        assert prop.getProperty("dict") == {"nested": "value"}

    def test_getProperty_keyError_missing_key(self):
        cfg = {"existing": "value"}
        prop = Properties(cfg)

        with pytest.raises(KeyError):
            prop.getProperty("nonexistent")

    def test_getProperty_keyError_missing_nested_key(self):
        cfg = {"parent": {"child": "value"}}
        prop = Properties(cfg)

        with pytest.raises(KeyError):
            prop.getProperty("parent.missing")

    def test_getPropertyWithDefault_returns_value_when_exists(self):
        cfg = {"key": "value"}
        prop = Properties(cfg)

        assert prop.getPropertyWithDefault("key", "default") == "value"

    def test_getPropertyWithDefault_returns_default_when_missing(self):
        cfg = {"key": "value"}
        prop = Properties(cfg)

        assert prop.getPropertyWithDefault("missing", "default") == "default"

    def test_getPropertyWithDefault_with_none_default(self):
        cfg = {}
        prop = Properties(cfg)

        assert prop.getPropertyWithDefault("missing", None) is None

    def test_str_representation(self):
        cfg = {"key": "value"}
        prop = Properties(cfg)

        result = str(prop)
        assert "key" in result
        assert "value" in result

    def test_empty_config(self):
        cfg = {}
        prop = Properties(cfg)

        assert prop.getNode() == {}

    def test_getProperty_list_index_access(self):
        cfg = {"items": ["first", "second", "third"]}
        prop = Properties(cfg)

        with pytest.raises((KeyError, TypeError)):
            prop.getProperty("items.0")

import pytest
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config_with_yaml import Loader


class TestInclude:
    def test_include_simple_file(self, tmp_path):
        base_dir = tmp_path / "includes"
        base_dir.mkdir()

        included = base_dir / "database.yml"
        included.write_text("host: localhost\nport: 5432")

        main_file = base_dir / "main.yml"
        main_file.write_text("name: app\ndb: !include database.yml")

        original_dir = os.getcwd()
        try:
            os.chdir(tmp_path)
            loader = Loader()
            prop = loader.load("includes/main.yml")
            assert prop.getProperty("name") == "app"
            assert prop.getProperty("db.host") == "localhost"
            assert prop.getProperty("db.port") == 5432
        finally:
            os.chdir(original_dir)

    def test_include_multiple_files(self, tmp_path):
        base_dir = tmp_path / "includes"
        base_dir.mkdir()

        db_file = base_dir / "db.yml"
        db_file.write_text("host: localhost\nport: 5432")

        settings_file = base_dir / "settings.yml"
        settings_file.write_text("timeout: 30")

        main_file = base_dir / "main.yml"
        main_file.write_text(
            "database: !include db.yml\nsettings: !include settings.yml"
        )

        original_dir = os.getcwd()
        try:
            os.chdir(tmp_path)
            loader = Loader()
            prop = loader.load("includes/main.yml")
            assert prop.getProperty("database.host") == "localhost"
            assert prop.getProperty("settings.timeout") == 30
        finally:
            os.chdir(original_dir)

    def test_include_chained(self, tmp_path):
        base_dir = tmp_path / "includes"
        base_dir.mkdir()

        level3 = base_dir / "level3.yml"
        level3.write_text("value: deep")

        level2 = base_dir / "level2.yml"
        level2.write_text("nested: !include level3.yml")

        level1 = base_dir / "level1.yml"
        level1.write_text("data: !include level2.yml")

        original_dir = os.getcwd()
        try:
            os.chdir(tmp_path)
            loader = Loader()
            prop = loader.load("includes/level1.yml")
            assert prop.getProperty("data.nested.value") == "deep"
        finally:
            os.chdir(original_dir)

    def test_include_max_depth_exceeded(self, tmp_path):
        base_dir = tmp_path / "includes"
        base_dir.mkdir()

        l1 = base_dir / "l1.yml"
        l1.write_text("a: !include l2.yml")

        l2 = base_dir / "l2.yml"
        l2.write_text("b: !include l3.yml")

        l3 = base_dir / "l3.yml"
        l3.write_text("c: value")

        original_dir = os.getcwd()
        try:
            os.chdir(tmp_path)
            loader = Loader(max_include_depth=1)
            with pytest.raises(ValueError) as exc_info:
                loader.load("includes/l1.yml")
            assert "Maximum include depth" in str(exc_info.value)
        finally:
            os.chdir(original_dir)

    def test_include_file_not_found(self, tmp_path):
        base_dir = tmp_path / "includes"
        base_dir.mkdir()

        main_file = base_dir / "main.yml"
        main_file.write_text("data: !include nonexistent.yml")

        original_dir = os.getcwd()
        try:
            os.chdir(tmp_path)
            loader = Loader()
            with pytest.raises(ValueError) as exc_info:
                loader.load("includes/main.yml")
            assert "not found" in str(exc_info.value)
        finally:
            os.chdir(original_dir)

    def test_include_scalar_value(self, tmp_path):
        base_dir = tmp_path / "includes"
        base_dir.mkdir()

        value_file = base_dir / "value.yml"
        value_file.write_text("just_a_string")

        main_file = base_dir / "main.yml"
        main_file.write_text("key: !include value.yml")

        original_dir = os.getcwd()
        try:
            os.chdir(tmp_path)
            loader = Loader()
            prop = loader.load("includes/main.yml")
            assert prop.getProperty("key") == "just_a_string"
        finally:
            os.chdir(original_dir)

    def test_include_list_value(self, tmp_path):
        base_dir = tmp_path / "includes"
        base_dir.mkdir()

        list_file = base_dir / "list.yml"
        list_file.write_text("- item1\n- item2\n- item3")

        main_file = base_dir / "main.yml"
        main_file.write_text("items: !include list.yml")

        original_dir = os.getcwd()
        try:
            os.chdir(tmp_path)
            loader = Loader()
            prop = loader.load("includes/main.yml")
            assert prop.getProperty("items") == ["item1", "item2", "item3"]
        finally:
            os.chdir(original_dir)

    def test_include_resolves_relative_to_parent(self, tmp_path):
        subdir = tmp_path / "subdir"
        subdir.mkdir()

        other_dir = tmp_path / "other"
        other_dir.mkdir()

        included = other_dir / "data.yml"
        included.write_text("key: from_other_dir")

        main_file = subdir / "main.yml"
        main_file.write_text("data: !include ../other/data.yml")

        original_dir = os.getcwd()
        try:
            os.chdir(tmp_path)
            loader = Loader()
            prop = loader.load("subdir/main.yml")
            assert prop.getProperty("data.key") == "from_other_dir"
        finally:
            os.chdir(original_dir)

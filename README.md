# Config With YAML

Config With YAML is a pure-Python package to load config YAML files.

## Installation

```bash
pip install config_with_yaml
```

## Quick Start

```python
from config_with_yaml import Loader

loader = Loader()
cfg = loader.load("config.yml")

print(cfg.getProperty("database.host"))
print(cfg.getPropertyWithDefault("database.port", 5432))
print(cfg)
```

## Using !include

The `Loader` class supports the `!include` tag to include external YAML files. Paths are resolved relative to the current file's directory.

```yaml
# config.yml
app_name: myapp

database: !include database.yml
features: !include features.yml
```

```yaml
# database.yml
host: localhost
port: 5432
```

```yaml
# features.yml
debug: true
max_connections: 100
```

Loading the config:

```python
from config_with_yaml import Loader

loader = Loader()
cfg = loader.load("config.yml")

print(cfg.getProperty("app_name"))       # myapp
print(cfg.getProperty("database.host"))  # localhost
print(cfg.getProperty("features.debug")) # true
```

### Chained Includes

Includes can be chained (A includes B includes C). By default, maximum depth is 5.

```yaml
# level1.yml
data: !include level2.yml
```

```yaml
# level2.yml
nested: !include level3.yml
```

```yaml
# level3.yml
value: deep_value
```

```python
cfg = loader.load("level1.yml")
print(cfg.getProperty("data.nested.value"))  # deep_value
```

### Relative Paths

Use relative paths to include files from other directories:

```yaml
# subdir/config.yml
data: !include ../shared/common.yml
```

## Configuration

The `Loader` class accepts the following parameters:

- `max_include_depth` (int): Maximum depth for nested includes (default: 5)
- `log_level` (int): Logging level (default: logging.DEBUG)
- `config_paths` (str): Additional colon-separated paths to search for config files

```python
import logging
from config_with_yaml import Loader

loader = Loader(
    max_include_depth=3,
    log_level=logging.INFO,
    config_paths="/path/to/configs:/another/path"
)

cfg = loader.load("config.yml")
```

## Environment Variables

- `YAML_CONFIG_PATHS`: Colon-separated paths to search for config files (in addition to current directory)

```shell
export YAML_CONFIG_PATHS=path/to/folder1:path/to/folder2
```

## Legacy API (Deprecated)

The old `load()` function is still available but deprecated:

```python
import warnings
from config_with_yaml import load

# This will show a DeprecationWarning
warnings.filterwarnings('ignore', category=DeprecationWarning)
cfg = load("config.yml")
```

**Migration**: Replace with:

```python
from config_with_yaml import Loader

loader = Loader()
cfg = loader.load("config.yml")
```

## Config File Format

Example YAML config:

```yaml
Demo:
  Motors:
    Server: ROS
    Proxy: Motors:default -h localhost -p 9001
    Topic: '/turtlebotROS/mobile_base/commands/velocity'
    Name: basic_component_pyCamera
    maxW: 0.7
    maxV: 4

  Camera:
    Server: ROS
    Proxy: "CameraL:default -h localhost -p 9001"
    Format: RGB8
    Topic: "/TurtlebotROS/cameraL/image_raw"
    Name: basic_component_pyCamera

  NodeName: demo
```

Access properties:

```python
cfg = loader.load("demo.yml")
print(cfg.getProperty("Demo.Motors.Server"))       # ROS
print(cfg.getPropertyWithDefault("Demo.Motors.X", "default"))  # default
print(cfg.getProperty("Demo.Camera.Format"))        # RGB8
```

## Testing

```bash
pip install -e ".[dev]"
pytest tests/
```

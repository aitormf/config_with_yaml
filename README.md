# Config With YAML

Config With YAML is a pure-Python package to load config YAML files.

```python
import config_with_yaml as config

cfg = config.load("demo.yml")

print (cfg.getProperty("Demo.Motors.Server"))
print (cfg.getPropertyWithDefault("Demo.Motors.Server2", "Server2"))
print (cfg)
```
Config file content:
```
Demo:
  Motors:
    Server: ROS # Deactivate, Ice , ROS
    Proxy: Motors:default -h localhost -p 9001
    Topic: '/turtlebotROS/mobile_base/commands/velocity'
    Name: basic_component_pyCamera
    maxW: 0.7
    maxV: 4

  Camera:
    Server: ROS # Deactivate, Ice , ROS
    Proxy: "CameraL:default -h localhost -p 9001"
    Format: RGB8
    Topic: "/TurtlebotROS/cameraL/image_raw"
    Name: basic_component_pyCamera

  NodeName: demo
```

Output:
```
loading Config file ./demo.yml
ROS
Server2
Demo:
  Camera:
    Format: RGB8
    Name: basic_component_pyCamera
    Proxy: CameraL:default -h localhost -p 9001
    Server: ROS
    Topic: /TurtlebotROS/cameraL/image_raw
  Motors:
    Name: basic_component_pyCamera
    Proxy: Motors:default -h localhost -p 9001
    Server: ROS
    Topic: /turtlebotROS/mobile_base/commands/velocity
    maxV: 4
    maxW: 0.7
  NodeName: demo
```

## Extra Configuration

by default config_with_yaml uses the path to the file that is passed to it, but if you have all the cofiguration files in directory or several, you can set the value of the environment variable **"YAML_CONFIG_PATHS"** with these files separated by *:*, so just put the file name is able to find it.

```shell
export YAML_CONFIG_PATHS=path/to/folder1:path/to/folder2
```

# -*- coding: utf-8 -*-
__author__ = "aitormf"

import sys
import logging
from config_with_yaml import Loader

loader = Loader(log_level=logging.INFO)
cfg = loader.load(sys.argv[1])

print(cfg.getProperty("Demo.Motors.Server"))
print(cfg.getPropertyWithDefault("Demo.Motors.Server2", "Server2"))
print(cfg)

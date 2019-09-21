# -*- coding: utf-8 -*-
__author__ = 'aitormf'

import sys

import config_with_yaml as config

cfg = config.load(sys.argv[1])

print (cfg.getProperty("Demo.Motors.Server"))
print (cfg.getPropertyWithDefault("Demo.Motors.Server2", "Server2"))
print (cfg)


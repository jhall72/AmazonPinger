# -*- coding: utf-8 -*-
import pkg_resources  # part of setuptools
__version__ = pkg_resources.require("amazon-mws")[0].version

from .mws import *  # NOQA

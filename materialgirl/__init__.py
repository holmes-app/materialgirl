#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

__version__ = '0.5.0'

try:
    from materialgirl.materializer import Materializer  # NOQA
except ImportError:
    logging.warning('Import error while trying to import materializer. Probably setup.py installing materialgirl.')

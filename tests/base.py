#!/usr/bin/env python
# -*- coding: utf-8 -*-

import redis

from unittest import TestCase as PythonTestCase


class TestCase(PythonTestCase):
    def setUp(self):
        self.redis = redis.StrictRedis(host='localhost', port=7557, db=0)

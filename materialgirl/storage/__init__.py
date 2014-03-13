#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Storage(object):
    def store(self, key, value, expiration=None):
        raise NotImplementedError()

    def retrieve(self, key):
        raise NotImplementedError()

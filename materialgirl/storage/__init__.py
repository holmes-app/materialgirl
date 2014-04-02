#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Storage(object):
    def store(self, key, value, expiration=None, grace_period=None):
        raise NotImplementedError()

    def retrieve(self, key):
        raise NotImplementedError()

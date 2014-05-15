#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Storage(object):
    def store(self, key, value, expiration=None, grace_period=None):
        raise NotImplementedError()

    def retrieve(self, key):
        raise NotImplementedError()

    def release_lock(self, lock):
        raise NotImplementedError()

    def acquire_lock(self, key, expiration=None):
        raise NotImplementedError()

    def is_expired(self, key, expiration=None):
        raise NotImplementedError()

    def expire(self, key):
        raise NotImplementedError()

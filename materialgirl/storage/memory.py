#!/usr/bin/env python
# -*- coding: utf-8 -*-

from materialgirl.storage import Storage


class InMemoryStorage(Storage):
    def __init__(self):
        self.items = {}
        self.locks = []

    def store(self, key, value, expiration=None, grace_period=None):
        self.items[key] = value
        self.items.pop('_expired_%s' % key, None)

    def retrieve(self, key):
        return self.items.get(key, self.items.get('_expired_%s' % key, None))

    def release_lock(self, key):
        self.locks.remove(key)

    def acquire_lock(self, key):
        if key in self.locks:
            return None
        self.locks.append(key)
        return key

    def is_expired(self, key, expiration=None):
        return '_expired_%s' % key in self.items or key not in self.items

    def expire(self, key):
        if not self.is_expired(key):
            self.items['_expired_%s' % key] = self.items.pop(key)

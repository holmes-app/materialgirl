#!/usr/bin/env python
# -*- coding: utf-8 -*-

from materialgirl.storage import Storage


class InMemoryStorage(Storage):
    def __init__(self):
        self.items = {}
        self.locks = []

    def store(self, key, value, expiration=None, grace_period=None):
        self.items[key] = value

    def retrieve(self, key):
        return self.items.get(key, None)

    def release_lock(self, key):
        self.locks.remove(key)

    def acquire_lock(self, key):
        if key in self.locks:
            return None
        self.locks.append(key)
        return key

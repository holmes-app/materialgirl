#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from time import time


class Material(object):
    def __init__(self, key, get_method, expiration=10, grace_period=0, lock_timeout=None):
        self.key = key
        self.current_value = None
        self.get_method = get_method
        self.expiration = expiration
        self.expiration_date = time() + expiration
        self.grace_period = grace_period
        self.lock_timeout = lock_timeout

    @property
    def is_expired(self):
        return self.current_value is None or time() > self.expiration_date

    def get(self):
        self.current_value = self.get_method()
        return self.current_value


class Materializer(object):
    def __init__(self, storage, load_on_cachemiss=True):
        self.storage = storage
        self.load_on_cachemiss = load_on_cachemiss

        self.materials = {}

    def add_material(self, key, get_method, expiration=10, grace_period=0, lock_timeout=None):
        self.materials[key] = Material(key, get_method, expiration, grace_period, lock_timeout)

    def expire(self, key):
        if not key in self.materials:
            raise ValueError('Key %s not found in materials. Maybe you forgot to call "add_material" for this key?' % key)

        self.storage.expire(key)

    def is_expired(self, key):
        if not key in self.materials:
            raise ValueError('Key %s not found in materials. Maybe you forgot to call "add_material" for this key?' % key)

        return self.storage.is_expired(key)

    def run(self):
        for key, material in self.materials.items():
            logging.info('Acquiring lock for %s...' % key)
            lock = self.storage.acquire_lock(key, timeout=material.lock_timeout)

            if lock is None:
                logging.info('%s is locked, skipping.' % key)
                continue

            if self.storage.is_expired(key, material.expiration) or material.is_expired:
                logging.info('Retrieving %s...' % key)
                self.storage.store(key, material.get(), expiration=material.expiration, grace_period=material.grace_period)
                logging.info('Storing %s...' % key)
                material.expiration_date = time() + material.expiration

            logging.info('Releasing lock for %s...' % key)
            self.storage.release_lock(lock)

            logging.info('Done with %s.' % key)

    def get(self, key):
        if not key in self.materials:
            raise ValueError('Key %s not found in materials. Maybe you forgot to call "add_material" for this key?' % key)

        value = self.storage.retrieve(key)

        if value is None and self.load_on_cachemiss:
            material = self.materials[key]
            value = material.get()
            self.storage.store(key, value, expiration=material.expiration, grace_period=material.grace_period)

        return value

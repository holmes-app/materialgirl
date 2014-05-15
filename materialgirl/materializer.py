#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time import time


class Material(object):
    def __init__(self, key, get_method, expiration=10, grace_period=0):
        self.key = key
        self.current_value = None
        self.get_method = get_method
        self.expiration = expiration
        self.expiration_date = time() + expiration
        self.grace_period = grace_period

    @property
    def is_expired(self):
        return self.current_value is None or time() > self.expiration_date

    def get(self):
        self.current_value = self.get_method()
        return self.current_value


class Materializer(object):
    def __init__(self, storage):
        self.storage = storage

        self.materials = {}

    def add_material(self, key, get_method, expiration=10, grace_period=0):
        self.materials[key] = Material(key, get_method, expiration, grace_period)

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
            lock = self.storage.acquire_lock(key)

            if lock is None:
                continue

            if self.storage.is_expired(key, material.expiration) or material.is_expired:
                self.storage.store(key, material.get(), expiration=material.expiration, grace_period=material.grace_period)
                material.expiration_date = time() + material.expiration

            self.storage.release_lock(lock)

    def get(self, key):
        if not key in self.materials:
            raise ValueError('Key %s not found in materials. Maybe you forgot to call "add_material" for this key?' % key)

        value = self.storage.retrieve(key)

        if value is None:
            material = self.materials[key]
            value = material.get()
            self.storage.store(key, value, expiration=material.expiration, grace_period=material.grace_period)

        return value

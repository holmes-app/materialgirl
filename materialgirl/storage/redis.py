#!/usr/bin/env python
# -*- coding: utf-8 -*-

from materialgirl.storage import Storage


class RedisStorage(Storage):
    def __init__(self, redis):
        self.redis = redis

    def store(self, key, value, expiration=10):
        self.redis.psetex(name=key, value=value, time_ms=int(expiration * 1000))

    def retrieve(self, key):
        return self.redis.get(key)

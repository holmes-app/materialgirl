#!/usr/bin/env python
# -*- coding: utf-8 -*-

import msgpack

from materialgirl.storage import Storage


class RedisStorage(Storage):
    def __init__(self, redis):
        self.redis = redis

    def store(self, key, value, expiration=10):
        if value is None:
            return

        value = msgpack.packb(value, encoding='utf-8')
        self.redis.psetex(name=key, value=value, time_ms=int(expiration * 1000))

    def retrieve(self, key):
        value = self.redis.get(key)
        if value is None:
            return None

        return msgpack.unpackb(value, encoding='utf-8')

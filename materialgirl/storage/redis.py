#!/usr/bin/env python
# -*- coding: utf-8 -*-

import msgpack

from materialgirl.storage import Storage


class RedisStorage(Storage):
    def __init__(self, redis):
        self.redis = redis

    def store(self, key, value, expiration=10, grace_period=0):
        if value is None:
            return

        if grace_period > expiration:
            time_ms = int(grace_period * 1000)
        else:
            time_ms = int(expiration * 1000)

        value = msgpack.packb(value, encoding='utf-8')
        self.redis.psetex(name=key, value=value, time_ms=time_ms)

    def retrieve(self, key):
        value = self.redis.get(key)
        if value is None:
            return None

        return msgpack.unpackb(value, encoding='utf-8')

    def release_lock(self, lock):
        return lock.release()

    def lock_key(self, key):
        return self.redis.lock('material-girl-%s-lock' % key)

    def acquire_lock(self, key):
        lock = self.lock_key(key)
        has_acquired = lock.acquire(blocking=False)
        if not has_acquired:
            return None
        return lock

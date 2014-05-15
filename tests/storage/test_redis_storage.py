#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

from preggy import expect
import msgpack

from materialgirl.storage.redis import RedisStorage
from tests.base import TestCase


class TestRedisStorage(TestCase):
    def test_can_create_storage(self):
        storage = RedisStorage(redis=self.redis)
        expect(storage).not_to_be_null()
        expect(storage.redis).to_equal(self.redis)

    def test_can_store_none_as_value(self):
        key = 'test-%s' % time.time()
        storage = RedisStorage(self.redis)
        storage.store(key, None, expiration=10)

        value = self.redis.get(key)

        expect(value).to_be_null()

    def test_can_store_value(self):
        key = 'test-%s' % time.time()
        storage = RedisStorage(self.redis)
        storage.store(key, 'woot', expiration=10)

        value = self.redis.get(key)
        value = msgpack.unpackb(value, encoding='utf-8')

        expect(value).not_to_be_null()
        expect(value).to_equal('woot')

    def test_can_store_value_using_expiration(self):
        key = 'test-2-%s' % time.time()
        storage = RedisStorage(self.redis)
        storage.store(key, 'woot', expiration=10)

        value = self.redis.get(key)
        value = msgpack.unpackb(value, encoding='utf-8')

        expect(value).not_to_be_null()
        expect(value).to_equal('woot')

    def test_can_store_value_with_grace_value(self):
        key = 'test-2-%s' % time.time()
        storage = RedisStorage(self.redis)
        storage.store(key, 'woot', expiration=10, grace_period=20)

        value = self.redis.get(key)
        value = msgpack.unpackb(value, encoding='utf-8')

        expect(value).not_to_be_null()
        expect(value).to_equal('woot')

    def test_can_get_null_if_value_not_set(self):
        storage = RedisStorage(self.redis)

        expect(storage.retrieve('invalid-key')).to_be_null()

    def test_can_get_value(self):
        key = 'test-3-%s' % time.time()
        storage = RedisStorage(self.redis)
        storage.store(key, 'woot', expiration=10)

        value = storage.retrieve(key)

        expect(value).to_equal('woot')

    def test_can_acquire_lock(self):
        key = 'test-%s' % time.time()
        self.redis.delete(key)
        storage = RedisStorage(self.redis)

        lock = storage.acquire_lock(key)
        expect(lock).not_to_be_null()

        locked = storage.acquire_lock(key)
        expect(locked).to_be_null()

        storage.release_lock(lock)

    def test_can_release_lock(self):
        key = 'test-release-lock'
        self.redis.delete(key)
        storage = RedisStorage(self.redis)

        lock = storage.acquire_lock(key)
        expect(lock).not_to_be_null()

        storage.release_lock(lock)

        lock = storage.acquire_lock(key)
        expect(lock).not_to_be_null()

        storage.release_lock(lock)

    def test_can_check_not_expired(self):
        key = 'test-4-%s' % time.time()
        self.redis.delete(key)
        storage = RedisStorage(self.redis)

        expect(storage.is_expired(key)).to_be_true()

        storage.store(key, 'woot', expiration=10)

        expect(storage.is_expired(key)).to_be_false()

    def test_can_check_expired(self):
        key = 'test-4-%s' % time.time()
        self.redis.delete(key)
        storage = RedisStorage(self.redis)

        expect(storage.is_expired(key)).to_be_true()

        storage.store(key, 'woot', expiration=10, grace_period=20)
        self.redis.pexpire(key, 9000)

        expect(storage.is_expired(key, 10)).to_be_true()

    def test_can_expire(self):
        key = 'test-4-%s' % time.time()
        self.redis.delete(key)
        storage = RedisStorage(self.redis)
        storage.store(key, 'woot', expiration=10)

        storage.expire(key)

        expect(storage.is_expired(key)).to_be_true()

    def test_can_expire_invalid_key(self):
        key = 'test-4-%s' % time.time()
        self.redis.delete(key)
        storage = RedisStorage(self.redis)

        expect(storage.is_expired('invalid-key')).to_be_true()

        storage.expire('invalid-key')

        expect(storage.is_expired('invalid-key')).to_be_true()

    def test_can_store_expired(self):
        key = 'test-4-%s' % time.time()
        self.redis.delete(key)
        storage = RedisStorage(self.redis)
        storage.store(key, 'woot', expiration=10)

        storage.expire(key)

        expect(storage.is_expired(key)).to_be_true()

        storage.store(key, 'woot', expiration=10)

        value = storage.retrieve(key)

        expect(value).to_equal('woot')

    def test_can_get_even_if_expired(self):
        key = 'test-4-%s' % time.time()
        self.redis.delete(key)
        storage = RedisStorage(self.redis)
        storage.store(key, 'woot', expiration=10)

        storage.expire(key)

        expect(storage.is_expired(key)).to_be_true()

        value = storage.retrieve(key)

        expect(value).to_equal('woot')

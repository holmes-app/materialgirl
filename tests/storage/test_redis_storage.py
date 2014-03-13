#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

import redis
from preggy import expect

from materialgirl.storage.redis import RedisStorage
from tests.base import TestCase


class TestRedisStorage(TestCase):
    def setUp(self):
        self.redis = redis.StrictRedis(host='localhost', port=7557, db=0)

    def test_can_create_storage(self):
        storage = RedisStorage(redis=self.redis)
        expect(storage).not_to_be_null()
        expect(storage.redis).to_equal(self.redis)

    def test_can_store_value(self):
        key = 'test-%s' % time.time()
        storage = RedisStorage(self.redis)
        storage.store(key, 'woot', expiration=10)

        value = self.redis.get(key)

        expect(value).not_to_be_null()
        expect(value).to_equal('woot')

    def test_can_store_value_using_expiration(self):
        key = 'test-2-%s' % time.time()
        storage = RedisStorage(self.redis)
        storage.store(key, 'woot', expiration=0.001)
        time.sleep(0.1)

        value = self.redis.get(key)

        expect(value).to_be_null()

    def test_can_get_null_if_value_not_set(self):
        storage = RedisStorage(self.redis)

        expect(storage.retrieve('invalid-key')).to_be_null()

    def test_can_get_value(self):
        key = 'test-3-%s' % time.time()
        storage = RedisStorage(self.redis)
        storage.store(key, 'woot', expiration=10)

        value = storage.retrieve(key)

        expect(value).to_equal('woot')

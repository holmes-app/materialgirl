#!/usr/bin/env python
# -*- coding: utf-8 -*-

from preggy import expect

from materialgirl.storage.memory import InMemoryStorage
from tests.base import TestCase


class TestInMemoryStorage(TestCase):
    def test_can_create_storage(self):
        storage = InMemoryStorage()
        expect(storage.items).to_be_like({})

    def test_can_store_value(self):
        storage = InMemoryStorage()
        storage.store('test', 'woot', expiration=10)

        expect(storage.items).to_length(1)
        expect(storage.items).to_include('test')
        expect(storage.items['test']).to_equal('woot')

    def test_can_get_null_if_value_not_set(self):
        storage = InMemoryStorage()

        expect(storage.retrieve('key')).to_be_null()

    def test_can_get_value(self):
        storage = InMemoryStorage()
        storage.store('test', 'woot', expiration=10)

        value = storage.retrieve('test')

        expect(value).to_equal('woot')

    def test_can_acquire_lock(self):
        storage = InMemoryStorage()

        lock = storage.acquire_lock('key-test')
        expect(lock).not_to_be_null()

        lock = storage.acquire_lock('key-test')
        expect(lock).to_be_null()

    def test_can_release_lock(self):
        storage = InMemoryStorage()

        lock = storage.acquire_lock('key-test')
        expect(lock).not_to_be_null()

        storage.release_lock('key-test')

        lock = storage.acquire_lock('key-test')
        expect(lock).not_to_be_null()

    def test_can_check_not_expired(self):
        storage = InMemoryStorage()

        expect(storage.is_expired('test')).to_be_true()

        storage.store('test', 'woot', expiration=10)

        expect(storage.is_expired('test')).to_be_false()

    def test_can_expire(self):
        storage = InMemoryStorage()
        storage.store('test', 'woot', expiration=10)

        storage.expire('test')

        expect(storage.is_expired('test')).to_be_true()

    def test_can_expire_invalid_key(self):
        storage = InMemoryStorage()

        expect(storage.is_expired('invalid-key')).to_be_true()

        storage.expire('invalid-key')

        expect(storage.is_expired('invalid-key')).to_be_true()

    def test_can_store_expired(self):
        storage = InMemoryStorage()
        storage.store('test', 'woot', expiration=10)

        storage.expire('test')

        expect(storage.is_expired('test')).to_be_true()

        storage.store('test', 'woot', expiration=10)

        value = storage.retrieve('test')

        expect(value).to_equal('woot')

    def test_can_get_even_if_expired(self):
        storage = InMemoryStorage()
        storage.store('test', 'woot', expiration=10)

        storage.expire('test')

        expect(storage.is_expired('test')).to_be_true()

        value = storage.retrieve('test')

        expect(value).to_equal('woot')

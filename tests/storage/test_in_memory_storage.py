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

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from mock import Mock
from preggy import expect

from materialgirl import Materializer
from materialgirl.storage.memory import InMemoryStorage
from materialgirl.storage.redis import RedisStorage
from tests.base import TestCase


class TestMaterialGirl(TestCase):
    def test_can_create_girl(self):
        storage = InMemoryStorage()
        girl = Materializer(storage=storage)

        expect(girl).not_to_be_null()
        expect(girl.storage).not_to_be_null()
        expect(girl.storage).to_equal(storage)

    def test_can_add_material(self):
        storage = InMemoryStorage()
        girl = Materializer(storage=storage)

        girl.add_material(
            'test',
            lambda: 'woot'
        )

        girl.run()

        expect(storage.items).to_include('test')
        expect(storage.items['test']).to_equal('woot')

    def test_does_not_add_not_expired_materials(self):
        storage = InMemoryStorage()
        girl = Materializer(storage=storage)

        girl.add_material(
            'test',
            lambda: 'woot'
        )

        girl.run()

        storage.items = {}

        girl.run()

        expect(storage.items).to_be_empty()

    def test_raises_if_key_not_found(self):
        storage = InMemoryStorage()
        girl = Materializer(storage=storage)

        try:
            value = girl.get('test')
        except ValueError:
            err = sys.exc_info()[1]
            expect(err).to_have_an_error_message_of(
                'Key test not found in materials. Maybe you forgot to call "add_material" for this key?'
            )
        else:
            assert False, "Should not have gotten this far"

    def test_can_get_value_after_material_girl_run(self):
        storage = InMemoryStorage()
        girl = Materializer(storage=storage)

        girl.add_material(
            'test',
            lambda: 'woot'
        )

        girl.run()

        value = girl.get('test')
        expect(value).to_equal('woot')

    def test_can_get_value_if_material_girl_not_run(self):
        storage = InMemoryStorage()
        girl = Materializer(storage=storage)

        girl.add_material(
            'test',
            lambda: 'woot'
        )

        value = girl.get('test')
        expect(value).to_equal('woot')

    def test_can_lock_key(self):
        storage = RedisStorage(self.redis)
        girl = Materializer(storage=storage)

        girl.add_material(
            'test1',
            lambda: 'woot1'
        )

        girl.add_material(
            'test2',
            lambda: 'woot2'
        )

        girl.storage.store = Mock()

        girl.run()

        expect(girl.storage.store.call_count).to_equal(2)

        girl.storage.store = Mock()
        girl.storage.acquire_lock = Mock(return_value=None)
        girl.storage.release_lock = Mock()

        girl.run()

        expect(girl.storage.store.call_count).to_equal(0)

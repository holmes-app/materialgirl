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
    def woots_generator(self):
        woots = ['woot1', 'woot2', 'woot3', 'woot4']
        for woot in woots:
            yield woot

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

    def test_can_add_material_with_expiration_and_graceperiod(self):
        storage = InMemoryStorage()
        girl = Materializer(storage=storage)

        girl.add_material(
            'test',
            lambda: 'woot',
            expiration=2,
            grace_period=4
        )

        girl.run()

        expect(storage.items).to_include('test')
        expect(storage.items['test']).to_equal('woot')

    def test_can_expire_materials(self):
        storage = InMemoryStorage()
        girl = Materializer(storage=storage)

        girl.add_material(
            'test',
            lambda: 'woot'
        )

        girl.run()

        expect(storage.items).to_length(1)
        expect(storage.items['test']).to_equal('woot')

        girl.expire('test')

        expect(girl.is_expired('test')).to_be_true()

        expect(storage.items).to_length(1)
        expect(storage.items.get('test')).to_be_null()
        expect(storage.items['_expired_test']).to_equal('woot')

    def test_can_update_expired_materials(self):
        storage = InMemoryStorage()
        girl = Materializer(storage=storage)

        woots = self.woots_generator()

        girl.add_material(
            'test',
            lambda: woots.next()
        )

        girl.run()

        expect(storage.items).to_length(1)
        expect(storage.items['test']).to_equal('woot1')

        storage.expire('test')

        girl.run()

        expect(storage.items).to_length(1)
        expect(storage.items['test']).to_equal('woot2')

    def test_can_update_deleted_materials(self):
        storage = InMemoryStorage()
        girl = Materializer(storage=storage)

        woots = self.woots_generator()

        girl.add_material(
            'test',
            lambda: woots.next()
        )

        girl.run()

        expect(storage.items).to_length(1)
        expect(storage.items['test']).to_equal('woot1')

        storage.items = {}

        girl.run()

        expect(storage.items).to_length(1)
        expect(storage.items['test']).to_equal('woot2')

    def test_dont_update_not_expired_materials(self):
        storage = InMemoryStorage()
        girl = Materializer(storage=storage)

        woots = self.woots_generator()

        girl.add_material(
            'test',
            lambda: woots.next()
        )

        girl.run()

        expect(storage.items).to_length(1)
        expect(storage.items['test']).to_equal('woot1')

        girl.run()

        expect(storage.items).to_length(1)
        expect(storage.items['test']).to_equal('woot1')

    def test_raises_if_key_not_found(self):
        storage = InMemoryStorage()
        girl = Materializer(storage=storage)

        try:
            girl.get('test')
        except ValueError:
            err = sys.exc_info()[1]
            expect(err).to_have_an_error_message_of(
                'Key test not found in materials. Maybe you forgot to call "add_material" for this key?'
            )
        else:
            assert False, "Should not have gotten this far"

        try:
            girl.is_expired('test')
        except ValueError:
            err = sys.exc_info()[1]
            expect(err).to_have_an_error_message_of(
                'Key test not found in materials. Maybe you forgot to call "add_material" for this key?'
            )
        else:
            assert False, "Should not have gotten this far"

        try:
            girl.expire('test')
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

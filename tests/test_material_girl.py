#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from mock import Mock, patch, call
from preggy import expect

from materialgirl import Materializer
from materialgirl.storage.memory import InMemoryStorage
from tests.base import TestCase


class TestMaterialGirl(TestCase):
    @staticmethod
    def woots_generator():
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
            lambda: next(woots)
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
            lambda: next(woots)
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
            lambda: next(woots)
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

    @patch('logging.info')
    def test_can_lock_key(self, logging_info_mock):
        storage = Mock(
            store=Mock(),
            acquire_lock=Mock(),
            release_lock=Mock()
        )

        girl = Materializer(storage=storage)

        girl.add_material(
            'test1',
            lambda: 'woot1'
        )
        girl.add_material(
            'test2',
            lambda: 'woot2'
        )

        girl.run()

        expect(storage.store.call_count).to_equal(2)
        expect(storage.acquire_lock.call_count).to_equal(2)
        expect(storage.release_lock.call_count).to_equal(2)
        expect(logging_info_mock.call_count).to_equal(10)

    @patch('logging.info')
    def test_can_skip_locked_key(self, logging_info_mock):
        storage = Mock(
            store=Mock(),
            acquire_lock=Mock(return_value=None),
            release_lock=Mock()
        )

        girl = Materializer(storage=storage)

        girl.add_material(
            'test1',
            lambda: 'woot1'
        )
        girl.add_material(
            'test2',
            lambda: 'woot2'
        )

        girl.run()

        expect(storage.store.call_count).to_equal(0)
        expect(storage.acquire_lock.call_count).to_equal(2)
        expect(storage.release_lock.call_count).to_equal(0)
        expect(logging_info_mock.call_count).to_equal(4)

    def test_can_lock_key_without_timeout(self):
        storage = Mock(store=Mock(), acquire_lock=Mock())

        girl = Materializer(storage=storage)
        girl.add_material(
            'test1',
            lambda: 'woot'
        )
        girl.add_material(
            'test2',
            lambda: 'woot'
        )

        girl.run()

        expect(storage.store.call_count).to_equal(2)
        expect(storage.acquire_lock.call_count).to_equal(2)
        storage.acquire_lock.assert_has_calls([
            call(
                'test1',
                timeout=None
            ), call(
                'test2',
                timeout=None
            )
        ])

    def test_can_lock_key_with_timeout(self):
        storage = Mock(store=Mock(), acquire_lock=Mock())

        girl = Materializer(storage=storage)
        girl.add_material(
            'test1',
            lambda: 'woot',
            lock_timeout=1
        )
        girl.add_material(
            'test2',
            lambda: 'woot',
            lock_timeout=2
        )

        girl.run()

        expect(storage.store.call_count).to_equal(2)
        expect(storage.acquire_lock.call_count).to_equal(2)
        storage.acquire_lock.assert_has_calls([
            call(
                'test1',
                timeout=1
            ), call(
                'test2',
                timeout=2
            )
        ])

    def test_can_miss_the_cache(self):
        storage = Mock(retrieve=Mock(return_value=None))

        girl = Materializer(storage=storage, load_on_cachemiss=False)
        girl.add_material('test', lambda: 'woot')

        girl.run()
        value = girl.get('test')

        expect(value).to_be_null()
        expect(storage.acquire_lock.call_count).to_equal(1)
        storage.store.assert_called_once_with(
            'test',
            'woot',
            expiration=10,
            grace_period=0
        )

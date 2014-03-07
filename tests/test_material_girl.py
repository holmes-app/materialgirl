#!/usr/bin/env python
# -*- coding: utf-8 -*-

from preggy import expect

from materialgirl import Materializer
from materialgirl.storage.memory import InMemoryStorage
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

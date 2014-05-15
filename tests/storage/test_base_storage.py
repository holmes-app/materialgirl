#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from preggy import expect

from materialgirl.storage import Storage
from tests.base import TestCase


class TestBaseStorage(TestCase):
    def test_can_create_storage(self):
        storage = Storage()
        expect(storage).not_to_be_null()

    def test_store_raises(self):
        storage = Storage()

        try:
            storage.store('test', 'woot', expiration=10)
        except NotImplementedError:
            err = sys.exc_info()[1]
            expect(err).to_be_an_error_like(NotImplementedError)
        else:
            assert False, "Should not have gotten this far"

    def test_retrieve_raises(self):
        storage = Storage()

        try:
            storage.retrieve('test')
        except NotImplementedError:
            err = sys.exc_info()[1]
            expect(err).to_be_an_error_like(NotImplementedError)
        else:
            assert False, "Should not have gotten this far"

    def test_release_lock_raises(self):
        storage = Storage()

        try:
            storage.release_lock('test')
        except NotImplementedError:
            err = sys.exc_info()[1]
            expect(err).to_be_an_error_like(NotImplementedError)
        else:
            assert False, "Should not have gotten this far"

    def test_acquire_lock_raises(self):
        storage = Storage()

        try:
            storage.acquire_lock('test')
        except NotImplementedError:
            err = sys.exc_info()[1]
            expect(err).to_be_an_error_like(NotImplementedError)
        else:
            assert False, "Should not have gotten this far"

    def test_is_expired_raises(self):
        storage = Storage()

        try:
            storage.is_expired('test')
        except NotImplementedError:
            err = sys.exc_info()[1]
            expect(err).to_be_an_error_like(NotImplementedError)
        else:
            assert False, "Should not have gotten this far"

    def test_expire_raises(self):
        storage = Storage()

        try:
            storage.expire('test')
        except NotImplementedError:
            err = sys.exc_info()[1]
            expect(err).to_be_an_error_like(NotImplementedError)
        else:
            assert False, "Should not have gotten this far"

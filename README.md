MaterialGirl
============

MaterialGirl is a library to keep materialized views and consolidations up-to-date.

Installing
==========

Intalling it is as easy as::

    $ pip install materialgirl

Usage
=====

MaterialGirl can be used to keep a set of data, called "materials", up-to-date.

It is very useful to keep slow queries or consolidated data fast to get.

You also need to select a storage (more on storages later). MaterialGirl comes bundled with two storages:

* materialgirl.storage.memory.InMemoryStorage
* materialgirl.storage.redis.RedisStorage

Using MaterialGirl:

    from materialgirl import MaterialGirl
    from materialgirl.storage.memory import InMemoryStorage

    def get_very_slow_data():
        return "this is very slow to get"

    storage = InMemoryStorage()
    girl = MaterialGirl(storage=storage)

    girl.add_material(
        'my-very-slow-data-key',
        get_very_slow_data,  # this should be the function to get up-to-date data
        120  # the expiration in seconds
    )

    girl.run()  # this updates all the expired materials and should be run in a loop

Retrieving Up-To-Date Information
=================================

Whenever you need to get the up-to-date information you set with material girl, just call the get method on an instance with the
same materials as the one you are running to update date, like this:

    from materialgirl import MaterialGirl
    from materialgirl.storage.memory import InMemoryStorage

    def get_very_slow_data():
        return "this is very slow to get"

    storage = InMemoryStorage()
    girl = MaterialGirl(storage=storage)

    girl.add_material(
        'my-very-slow-data-key',
        get_very_slow_data,  # this should be the function to get up-to-date data
        120  # the expiration in seconds
    )

    assert girl.get('my-very-slow-data-key') == 'this is very slow to get'

MaterialGirl is lazy. If it has not the up-to-date value in storage to give you, it will call your get method, update the storage and return the proper value.

Storages
========

The in-memory storage is more of a proof of concept and should only be used for very simple scenarios as it stores the data in-process.

Redis Storage
-------------

The redis storage takes one parameter: a redis connection.

    import redis
    from materialgirl.storage.redis import RedisStorage

    storage = RedisStorage(redis=redis.StrictRedis())

Creating a Custom Storage
-------------------------

Creating a custom storage is as simple as implementing two methods: `store` and `retrieve`:

    from materialgirl.storage import Storage

    class MyCustomStorage(Storage):
        def store(self, key, value, expiration=None):
            # store the value somewhere under `key`

        def get(self, key):
            # retrieve the value for `key` from same storage solution

Contributing
============

Just fork, commit, pull request our way.

License
=======

MIT licensed.

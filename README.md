MaterialGirl
============

MaterialGirl is a library to keep materialized views and consolidations up-to-date.

Installing
==========

Intalling it is as easy as::

    $ pip install materialgirl

Usage
=====

MaterialGirl can be used to keep a set of data, called _materials_, up-to-date.

It is very useful to keep slow queries or consolidated data fast to get.

You also need to select a storage (more on storages later). MaterialGirl comes bundled with two storages:

* materialgirl.storage.memory.InMemoryStorage
* materialgirl.storage.redis.RedisStorage

Using MaterialGirl:

```python
from materialgirl import Materializer
from materialgirl.storage.memory import InMemoryStorage

def get_very_slow_data():
    return 'this is very slow to get'

storage = InMemoryStorage()
girl = Materializer(storage=storage)

girl.add_material(
    'my-very-slow-data-key',
    get_very_slow_data,  # this should be the function to get up-to-date data
    120  # the expiration in seconds
)

girl.run()  # this updates all the expired materials and should be run in a loop
```

To run the loop you can use whatever daemon, worker, runner solution you'd like. We recommend [Sheep](http://heynemann.github.io/sheep/).

Retrieving Up-To-Date Information
=================================

Whenever you need to get the up-to-date information you set with material girl, just call the get method on an instance with the
same materials as the one you are running to update the data, like this:

```python
from materialgirl import Materializer
from materialgirl.storage.memory import InMemoryStorage

def get_very_slow_data():
    return 'this is very slow to get'

storage = InMemoryStorage()
girl = Materializer(storage=storage)

girl.add_material(
    'my-very-slow-data-key',
    get_very_slow_data,  # this should be the function to get up-to-date data
    120  # the expiration in seconds
)
assert girl.get('my-very-slow-data-key') == 'this is very slow to get'
```

MaterialGirl is lazy. If it has not the up-to-date value in storage to give you, it will call your get method, update the storage and return the proper value.

Defining a grace period
=======================

Sometimes you may need an information just before material girl updates it. In such cases you may have a cache miss. To avoid this, you can define a _grace period_ of time for the cached information:

```python
import time
from materialgirl import Materializer
from materialgirl.storage.memory import InMemoryStorage

def get_very_slow_data():
    return 'this is very slow to get'

storage = InMemoryStorage()
girl = Materializer(storage=storage)

girl.add_material(
    'my-very-slow-data-key',
    get_very_slow_data,  # this should be the function to get up-to-date data
    120,  # the expiration in seconds
    240  # the grace period in seconds
)

time.sleep(140)

assert girl.get('my-very-slow-data-key') == 'this is very slow to get'
```

This may not be the most up-to-date information, but cache misses become rare.

Forcing and checking expiration
===============================

In cases you find necessary to force the expiration for a given material or check if it's expired, material girl won't walk away:

```python
import time
from materialgirl import Materializer
from materialgirl.storage.memory import InMemoryStorage

def get_critical_data():
    return 'this is a very critical information'

storage = InMemoryStorage()
girl = Materializer(storage=storage)

girl.add_material(
    'my-very-critical-data-key',
    get_critical_data,  # this should be the function to get up-to-date data
    120,  # the expiration in seconds
    240  # the grace period in seconds
)

assert girl.is_expired('my-very-critical-data-key') is False

girl.expire('my-very-critical-data-key')

assert girl.is_expired('my-very-critical-data-key') is True

# ...
```

Although expired materials will be updated in the next round of updates – a.k.a. `girl.run()` – they remain available until grace period is reached:

```python
# ...

time.sleep(140)

assert girl.get('my-very-critical-data-key') == 'this is a very critical information'
```

Storages
========

The in-memory storage is more of a proof of concept and should only be used for very simple scenarios as it stores the data in-process.

Redis Storage
-------------

The redis storage takes one parameter: a redis connection.

```python
import redis
from materialgirl.storage.redis import RedisStorage

storage = RedisStorage(redis=redis.StrictRedis())
```

Creating a Custom Storage
-------------------------

Creating a custom storage is as simple as implementing two methods: `store` and `retrieve`:

```python
from materialgirl.storage import Storage

class MyCustomStorage(Storage):
    def store(self, key, value, expiration=None):
        # store the value somewhere under `key`

    def retrieve(self, key):
        # retrieve the value for `key` from same storage solution

    def release_lock(self, lock):
        # release a lock

    def acquire_lock(self, key, expiration=None):
        # acquire the lock for `key`
```

Contributing
============

Just fork, commit, pull request our way.

License
=======

MIT licensed.

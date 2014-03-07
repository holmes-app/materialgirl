test: redis unit

unit:
	@coverage run --branch `which nosetests` -vv --with-yanc -s tests/
	@coverage report -m --fail-under=80

coverage-html: unit
	@coverage html -d cover

tox:
	@PATH=$$PATH:~/.pythonbrew/pythons/Python-2.6.*/bin/:~/.pythonbrew/pythons/Python-2.7.*/bin/:~/.pythonbrew/pythons/Python-3.0.*/bin/:~/.pythonbrew/pythons/Python-3.1.*/bin/:~/.pythonbrew/pythons/Python-3.2.3/bin/:~/.pythonbrew/pythons/Python-3.3.0/bin/ tox

setup:
	@pip install -U -e .\[tests\]

kill_redis:
	-redis-cli -p 7557 shutdown

redis: kill_redis
	redis-server ./redis.conf; sleep 1
	redis-cli -p 7557 info > /dev/null

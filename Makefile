################################
# the makefile provides convenience commands
## "all in docker" steps
# to start the flask app, the worker & redis containers
# $ make start-all-docker
# to stop and remove all containers
# $ make clean

# run tests
# $ make test-docker

## flask app & worker natively + redis in docker (faster development)
# $ make start-redis-docker
# $ make start-worker-native

# $ make start-flask-native

# run tests
# $ make test-local

################################



# $ make test-local
# to run tests using a native python interpreter installed on your host machine
test-native:
	PYTHONPATH=src SIMPLE_SETTINGS=settings_common,settings_testing flask test



# $ make test-docker
# to run tests within a docker container (if you don't want to use your host python interpreter)
test-docker:clean build
	docker-compose run -e SIMPLE_SETTINGS=settings_common,settings_testing web flask test
	#docker run -e SIMPLE_SETTINGS=settings_common,settings_testing web flask test


# ---- local app + dockerised dependancies
# setup a development environment where the flask app runs via native python interpreter
# but its dependancies (redis + worker) run within docker

# $ make start-redis-docker
# if using a native python interpreter, but want to use a docker redis
start-redis-docker:
	docker-compose up -d redis
	#docker up -d redis

# $ make start-worker-native
# start on your host machine the rq worker only. redis must be running
start-worker-native:
	PYTHONPATH=src REDIS_HOST=localhost SIMPLE_SETTINGS=settings_common rq worker --with-scheduler -u redis://localhost:6379

# $ make start-flask-native
# starts *only* the flask app using a native python interpreter.
# assumes redis & worker are running
# web app is accessible on http://localhost:5000
start-flask-native:
	PYTHONPATH=src FLASK_DEBUG=true REDIS_HOST=localhost SIMPLE_SETTINGS=settings_common flask run
# ----



# $ make run-docker
# start the web app + its redis dependancies all within docker
# web app is accessible on http://localhost:5000
start-all-docker:
	docker-compose up --build
	#docker up --build

# $ make clean
# remove permanently all docker containers and their state
clean:
	docker-compose down

build:
	docker-compose build

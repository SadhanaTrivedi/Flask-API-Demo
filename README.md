The app consists of a Flask web API which makes it possible to obtain details about a given company from a third party provider (Clearbit)
and expose the obtained details to app clients.    
The app uses a worker process so that the 3rd party requests are not blocking. Redis is used to 1) fasciliate communnication
between the app and the worker  2) store results from Clearbit.

The app exposes two API endpoints:
1.   client sends a request for company details. The API handler doesn't wait for response
from Clearbit, it just creates a task to be completed by the worker process.
```json
POST /companies
{
	"name": "xyz",
	"domain": "xyz.co"
}
--> response confirms the task is received
```
A worker process must deal with making the request to Clearbit and store the results in a redis database.
2. A second endpoint `/companies/{name}`, which can receive a company name, and if the app has information about the company in redis, return it. 
```json
{
  "employee_count": <int>,
  "company_age": <int> 
}

```
The information to fetch from Clearbit and return as part of the response from the second API endpoint: 
* number of employees  in the company
* age of the company (based on founded date)

# Your task:
Mandatory requirements:
- Sign up to the clearbit API (https://clearbit.com/docs#api-reference)
- extend the `docker-compose.yml` file to include a redis container accessible on port 6379  (container should to be accessible from your host machine too)
- implement the above two endpoints + the logic to query Clearbit + store/retrieve data via redis
- ensure you follow best development practices
- api keys are not stored as plain text in the app code
- unit tests are written. You are free to use any testing library you choose to - the example tests can be changed.
- solution can be tested by us via 
    - `make test-docker`
    - `make start-all-docker` & making requests to the flask app

# Run / Develop tips
* There's a `docker-compose.yml` file which has container definitions for the flask app & worker process. With docker-compose you can quickly launch docker containers
* the flask app code bootstrap is already written. It uses the factory pattern to create the app given a config
* the `simple_settings` library is used to manage configuration - there are three prepared configurations - feel free to adjust them if needed
* to speed up development, you can
    * run the flask app (`web`) and `worker` natively (not in docker). This way code-changes you make will be available immediately without the need to rebuild the `web` & `worker` containers

        
## via CLI + text editor 
there's a `Makefile` with prepared convenience commands to start the app (either locally or within docker), 
execute tests (locally or within docker), start the app dependencies on docker, run all within docker.
## via PyCharm
* `$ make start-redis-docker` to start redis
* `$ make start-worker-native` to start the worker process
* to run the flask app
    * [add a Run configuration using "module"](https://stackoverflow.com/a/51268846/4509634)
    * module = `flask`
    * parameters = `run`
    * Environment variables
        * `REDIS_HOST=localhost`
        * `FLASK_DEBUG=1`
        * `SIMPLE_SETTINGS=settings_common`
* to run tests - with a unittest test runner, pass the `SIMPLE_SETTINGS=settings_common,settings_testing` env vars

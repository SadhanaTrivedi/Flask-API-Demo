from rq import Queue
from redis_adaptor import redis_client

# for the flask app to send tasks to the worker
task_queue = Queue(connection=redis_client)

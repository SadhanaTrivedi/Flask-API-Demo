from app.api import api_blueprint
from flask import current_app, request
from app.tasks.queue import task_queue
from worker.tasks import fetch_data_from_clearbit, \
    fetch_company_data_from_redis, fetch_company_details


@api_blueprint.route('/ping')
@api_blueprint.route('/')
def ping():
    return {"message": "pong", 'site_name': current_app.config.get('SITE_NAME')}


@api_blueprint.route('/companies', methods=['POST', 'GET'])
def get_companies_request():
    request_data = request.get_json()
    if not request_data:
        request_data = current_app.config.get('DEFAULT_CONFIG')
    worker_task = task_queue.enqueue(fetch_data_from_clearbit, request_data)
    fetch_company_details(worker_task.get_id())
    return {"response": "The task is recieved"}


@api_blueprint.route('/companies/<name>')
def get_company_details(name):
    return fetch_company_data_from_redis(name)

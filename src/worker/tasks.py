import logging
from datetime import datetime as dt
from simple_settings import settings
from redis_adaptor import redis_client
import json
import requests

logger = logging.getLogger('rq.worker')


def fetch_company_details(task) -> None:
    logger.info(f"received task {task}")


def fetch_data_from_clearbit(data) -> None:
    """Request to clearbit API"""
    try:
        key = settings.APP_KEY
        url = settings.URL
        response = requests.get(url, json=data, auth=(key, ''))
        status_code = response.status_code

        if status_code == 200:
            company_details = response.json()
            store_data_in_redis(company_details)
        else:
            logger.info(f"Response fron clearbit {status}")

    except Exception as error:
        logger.info(f"Error in API call {error}")


def store_data_in_redis(company_details: dict) -> None:
    """Store clearbit API details in Redis
    """
    logger.info(f"Store data in Redis")

    company_data = json.dumps(company_details)
    company_name = company_details['name'].lower()

    redis_client.set(company_name, company_data)


def fetch_company_data_from_redis(company_name: str) -> dict:
    """Return API response which was stored in Redis
    """
    logger.info(f"Company details request for company {company_name}")

    company_name = company_name.lower()
    try:
        company_data = redis_client.get(company_name)
        company_details = json.loads(company_data)
        company_age = dt.now().year - company_details['foundedYear']
        response["result"] = {"employee_count": company_details['metrics']['employees'],
                              "company_age": company_age
                              }
    except Exception as error:
        logger.info(f"Error in fetching details from redis {error}")
        response = {"error": "Data not found"}
    return response

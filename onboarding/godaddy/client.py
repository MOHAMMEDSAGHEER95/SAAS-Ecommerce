import json
import logging

import requests
from django.conf import settings
logger = logging.getLogger(__name__)


class GoDaddyClientHelper(object):
    BASE_URL = 'https://api.godaddy.com/v1'
    API_KEY = settings.GO_DADDY_API_KEY
    API_SECRET = settings.GO_DADDY_API_SECRET
    HEADER = "sso-key {}:{}"
    DOMAIN = settings.PUBLIC_DOMAIN_URL

    def __init__(self):
        self.HEADER = self.HEADER.format(self.API_KEY, self.API_SECRET)

    def make_api_request(self, url, data=None, method="GET", headers={}):
        print(url)
        headers = {"Authorization": self.HEADER,
                   "Content-Type": "application/json"}
        if method == "GET":
            logger.info("Request to GoDaddy: {}".format(url))
            response = requests.get(url, headers=headers)
        if method == "PATCH":
            response = requests.patch(url, data=data, headers=headers)
        else:
            logger.info("Request to GoDaddy: {}".format(json.dumps(data)))
            response = requests.post(url, data=data, headers=headers)
        return response

    def add_cname_to_dns(self, name):
        payload = json.dumps([
            {
                "data": "@",
                "name": name,
                "ttl": 3600,
                "type": "CNAME"
            }
        ])
        url = f"{self.BASE_URL}/domains/setyour.shop/records"
        response = self.make_api_request(url, payload, method='PATCH')

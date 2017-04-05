import requests
from requests_aws4auth import AWS4Auth


class Gateway:
    def __init__(self, session):
        creds = session.get_credentials()
        self.auth = AWS4Auth(
            creds.access_key,
            creds.secret_key,
            session.region_name,
            "execute-api",
            session_token=creds.token
        )
    def invoke(self, method, endpoint, data=None, json=None, params=None):
        method = getattr(requests, method)
        response = method(endpoint, data=data, params=params, json=json, auth=self.auth)
        response.raise_for_status()
        return response

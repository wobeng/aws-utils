import json

import boto3

from aws_utils.dynamodb import DynamoDb
from aws_utils.gateway import Gateway
from aws_utils.logs import Logs
from aws_utils.s3 import S3
from aws_utils.sqs import Sqs
from aws_utils.ssm import Ssm
from aws_utils.swf import Swf


def client(session=None, profile_name=None, region_name=None):
    aws = Aws(session, profile_name, region_name)
    return aws


class Aws:
    def __init__(self, session=None, profile_name=None, region_name=None):
        self.client = None
        self.session = session or boto3.session.Session(profile_name=profile_name, region_name=region_name)

    def __call__(self, service):
        return self.session.client(service)

    def invoke_lambda(self, function_name, payload):
        response = self.session.client('lambda').invoke(
            FunctionName=function_name,
            Payload=json.dumps(payload)
        )
        return response['Payload'].read().decode('utf-8')

    def var(self, name, default=None):
        return Ssm(self.session).parameter(name, default)

    @property
    def gateway(self):
        return Gateway(self.session)

    @property
    def dydb(self):
        return DynamoDb(self.session)

    @property
    def logs(self):
        return Logs(self.session)

    @property
    def s3(self):
        return S3(self.session)

    @property
    def sqs(self):
        return Ssm(self.session)

    @property
    def ssm(self):
        return Ssm(self.session)

    @property
    def swf(self):
        return Ssm(self.session)

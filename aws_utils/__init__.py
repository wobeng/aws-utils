import boto3
from pytz import UTC
from simplejson import dumps

from aws_utils.batch import Batch
from aws_utils.dynamodb.batch import DynamoDbBatch
from aws_utils.dynamodb.dynamodb import DynamoDb
from aws_utils.dynamodb.transaction import DynamoDbTransaction
from aws_utils.gateway import Gateway
from aws_utils.logs import Logs
from aws_utils.s3 import S3
from aws_utils.ses import Ses
from aws_utils.sf import Sf
from aws_utils.sns import Sns
from aws_utils.sqs import Sqs
from aws_utils.ssm import Ssm
from aws_utils.swf import Swf


def datetime_utc(dt=None):
    if not dt:
        dt = dt.datetime.utcnow()
    return dt.replace(tzinfo=UTC)


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
            Payload=dumps(payload)
        )
        response['Payload'] = response['Payload'].read().decode('utf-8')
        return response

    def var(self, name, default=None):
        return Ssm(self.session).parameter(name, default)

    @property
    def gateway(self):
        return Gateway(self.session)

    @property
    def batch(self):
        return Batch(self.session)

    @property
    def dydb(self):
        return DynamoDb(self.session)

    @property
    def dydb_transact(self):
        return DynamoDbTransaction(self.session)

    @property
    def dydb_batch(self):
        return DynamoDbBatch(self.session)

    @property
    def logs(self):
        return Logs(self.session)

    @property
    def s3(self):
        return S3(self.session)

    @property
    def sqs(self):
        return Sqs(self.session)

    @property
    def ssm(self):
        return Ssm(self.session)

    @property
    def swf(self):
        return Swf(self.session)

    @property
    def sf(self):
        return Sf(self.session)

    @property
    def ses(self):
        return Ses(self.session)

    @property
    def sns(self):
        return Sns(self.session)

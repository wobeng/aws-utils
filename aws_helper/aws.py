import boto3

from aws_gateway import Gateway
from aws_lambda import Lambda
from aws_log import Log
from aws_s3 import S3


class Aws:
    def __init__(self, session=None, profile_name=None, region_name=None):

        if session:
            self._session = session
        else:
            self._session = boto3.session.Session(profile_name=profile_name, region_name=region_name)

        self.aws_gateway = Gateway(self._session)
        self.aws_lambda = Lambda(self._session)
        self.aws_log = Log(self._session)
        self.aws_s3 = S3(self._session)

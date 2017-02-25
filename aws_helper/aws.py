import boto3

from aws_gateway import Gateway
from aws_lambda import Lambda
from aws_log import Log
from aws_s3 import S3


class Aws:
    def __init__(self, session=None, profile_name=None, region_name=None):

        if session:
            self.session = session
        else:
            self.session = boto3.session.Session(profile_name=profile_name, region_name=region_name)

        self.aws_gateway = Gateway(self.session)
        self.aws_lambda = Lambda(self.session)
        self.aws_log = Log(self.session)
        self.aws_s3 = S3(self.session)

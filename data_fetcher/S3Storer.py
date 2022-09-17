import datetime
import json

import dotenv
import pathlib
parent_path = pathlib.Path(__file__).parent.resolve().parent
dotenv.load_dotenv(parent_path.joinpath('.env'))
import os
import boto3


class S3Storer:
    DEFAULT_FILENAME = 'PUBLICATIONS_v2'
    BUCKET_NAME = 'dune-ml'

    def __init__(self, file_name: str):
        self.s3 = boto3.client('s3',
                               aws_access_key_id=os.environ['AWS_ACCESS_KEY'],
                               aws_secret_access_key=os.environ['AWS_SECRET_KEY'])
        self.file_name = file_name

    def store_json_inside_bucket(self, json_obj):
        self.s3.put_object(
            Body=json.dumps(json_obj),
            Bucket=self.BUCKET_NAME,
            Key='{}.json'.format(self.file_name)
        )

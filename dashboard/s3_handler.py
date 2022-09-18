import json
import dotenv
import pathlib
import boto3
import os

class S3Handler:
    def __init__(self):
        dotenv.load_dotenv(pathlib.Path(__file__).parent.parent.joinpath('.env'))
        self.s3 = boto3.client('s3', 
        aws_access_key_id=os.environ['AWS_ACCESS_KEY'], 
        aws_secret_access_key=os.environ['AWS_SECRET_KEY'])

    def read_object(self, key):
        obj = self.s3.get_object(Bucket='dune-ml', Key=key)
        result = obj['Body'].read().decode('utf-8')
        return json.loads(result)
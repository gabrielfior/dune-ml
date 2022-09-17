import json
import os
from datetime import date

import boto3
import pandas as pd
from dotenv import load_dotenv
from transformers import pipeline

from data_fetcher.S3Storer import S3Storer

load_dotenv()

def convert_lens_data_to_df(lens_data: dict) -> pd.DataFrame:
    content_list, created_list = [], []
    for item in lens_data:
        content_list.append(item['metadata']['content'])
        created_list.append(item['createdAt'])

    df = pd.DataFrame(content_list)
    df.rename(columns={0: "content"}, inplace=True)
    df['created_at'] = created_list
    df.created_at = pd.to_datetime(df.created_at)
    df['date'] = df.created_at.apply(lambda x: date(x.year, x.month, x.day))

    return df


def get_sentiment_data(df: pd.DataFrame) -> pd.DataFrame:
    model_path = "cardiffnlp/twitter-xlm-roberta-base-sentiment"
    sentiment_task = pipeline("sentiment-analysis", model=model_path, tokenizer=model_path, max_length=512,
                              truncation=True)
    df['sentiment_dict'] = df.content.apply(lambda x: sentiment_task(x))
    df['sentiment_label'] = df.sentiment_dict.apply(lambda x: x[0]['label'])
    df['sentiment_score'] = df.sentiment_dict.apply(lambda x: x[0]['score'])

    df.drop(columns=['sentiment_dict'], inplace=True)

    return df


def build_timeseries(df: pd.DataFrame) -> pd.Series:
    timeseries = df.groupby(by=["sentiment_label", "date"]).count()['content']
    return timeseries


if __name__ == "__main__":

    # NOTE: Script expects the file of S3 bucket as posts.json
    s3 = boto3.client('s3', aws_access_key_id=os.environ['AWS_ACCESS_KEY'],
                      aws_secret_access_key=os.environ['AWS_SECRET_KEY'])
    obj = s3.get_object(Bucket='dune-ml', Key='PUBLICATIONS_v3.json')
    result = obj['Body'].read().decode('utf-8')
    lens_data = json.loads(result)

    # Convert data into df
    df_lens = convert_lens_data_to_df(lens_data=lens_data)

    # Compute sentiment analysis
    df_lens_sentiment = get_sentiment_data(df=df_lens)
    timeseries = build_timeseries(df=df_lens_sentiment)

    # TODO: Change df to records
    df_lens_sentiment.to_csv("sentiment_v3.csv")
    # TODO: Inject dictionary to S3
    # s3storer = S3Storer(file_name="sentiment_data")
    # s3storer.store_json_inside_bucket(records)
    # TODO: Plot dataframe
    print("Run")

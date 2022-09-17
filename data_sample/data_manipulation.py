import json

import pandas as pd
from transformers import pipeline


def convert_lens_data_to_df(lens_data: dict) -> pd.DataFrame:
    items = lens_data['data']['explorePublications']['items']
    content_list, created_list = [], []
    for item in items:
        content_list.append(item['metadata']['content'])
        created_list.append(item['createdAt'])

    df = pd.DataFrame(content_list)
    df.rename(columns={0: "content"}, inplace=True)
    df['created_at'] = created_list
    df.created_at = pd.to_datetime(df.created_at)

    return df


def get_sentiment_data(df: pd.DataFrame) -> pd.DataFrame:
    model_path = "cardiffnlp/twitter-xlm-roberta-base-sentiment"
    sentiment_task = pipeline("sentiment-analysis", model=model_path, tokenizer=model_path)
    df['sentiment_dict'] = df.content.apply(lambda x: sentiment_task(x))
    df['sentiment_label'] = df.sentiment_dict.apply(lambda x: x[0]['label'])
    df['sentiment_score'] = df.sentiment_dict.apply(lambda x: x[0]['score'])

    df.drop(columns=['sentiment_dict'], inplace=True)

    return df


if __name__ == "__main__":

    with open('posts.json') as f:
        lens_data = json.load(f)

    df_lens = convert_lens_data_to_df(lens_data=lens_data)
    df_lens_sentiment = get_sentiment_data(df=df_lens)

    print("Run")

import json

import pandas as pd
from transformers import pipeline

model_path = "cardiffnlp/twitter-xlm-roberta-base-sentiment"
sentiment_task = pipeline("sentiment-analysis", model=model_path, tokenizer=model_path)

if __name__ == "__main__":

    with open('posts.json') as f:
        lens_data = json.load(f)

    items = lens_data['data']['explorePublications']['items']
    content_list, created_list = [], []
    for item in items:
        content_list.append(item['metadata']['content'])
        created_list.append(item['createdAt'])

    df = pd.DataFrame(content_list)
    df.rename(columns={0: "content"}, inplace=True)
    df['created_at'] = created_list
    df.created_at = pd.to_datetime(df.created_at)

    sentiment_list = list(map(sentiment_task, content_list))

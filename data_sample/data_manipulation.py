import json
from transformers import pipeline

model_path = "cardiffnlp/twitter-xlm-roberta-base-sentiment"
sentiment_task = pipeline("sentiment-analysis", model=model_path, tokenizer=model_path)

if __name__ == "__main__":

    with open('posts.json') as f:
        d = json.load(f)
        print(d)

    items = d['data']['explorePublications']['items']
    content = []
    for item in items:
        content.append(item['metadata']['content'])

    sentiment_list = list(map(sentiment_task, content))

    print("Run")

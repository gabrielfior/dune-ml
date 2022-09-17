import json
import os

import boto3
from bertopic import BERTopic
from sklearn.feature_extraction import text
from dotenv import load_dotenv

load_dotenv()

from data_sample.data_manipulation import convert_lens_data_to_df


def plot_figures(created_at: list, posts: list, topic_model: BERTopic, topics) -> None:
    topics_over_time = topic_model.topics_over_time(posts, topics, created_at, nr_bins=20)
    fig = topic_model.visualize_topics_over_time(topics_over_time, top_n_topics=10)
    fig.show('browser')

    fig_2 = topic_model.visualize_topics()
    fig_2.show('browser')

    fig_3 = topic_model.visualize_barchart()
    fig_3.show('browser')


if __name__ == "__main__":

    # Example https://stackoverflow.com/questions/40995251/reading-an-json-file-from-s3-using-python-boto3
    s3 = boto3.client('s3', aws_access_key_id=os.environ['AWS_ACCESS_KEY'],
                      aws_secret_access_key=os.environ['AWS_SECRET_KEY'])
    obj = s3.get_object(Bucket='dune-ml', Key='PUBLICATIONS.json')
    result = obj['Body'].read().decode('utf-8')
    lens_data = json.loads(result)

    # Convert data into df
    df_lens = convert_lens_data_to_df(lens_data=lens_data)
    stop = text.ENGLISH_STOP_WORDS
    df_lens.content = df_lens.content.apply(
        lambda words: ' '.join(word.lower() for word in words.split() if word not in stop))
    posts = df_lens.content.to_list()
    created_at = df_lens.created_at.to_list()

    topic_model = BERTopic(verbose=True, n_gram_range=(1, 3), min_topic_size=7)
    topics, probs = topic_model.fit_transform(posts)
    plot_figures(created_at=created_at, posts=posts, topic_model=topic_model, topics=topics)

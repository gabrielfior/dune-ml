import json

import pandas as pd
from bertopic import BERTopic

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
    # NOTE: Script expects the file of S3 bucket as posts.json
    with open('posts.json') as f:
        lens_data = json.load(f)

    # Convert data into df
    df_lens = convert_lens_data_to_df(lens_data=lens_data)
    posts = df_lens.content.to_list()[:500]
    created_at = df_lens.created_at.to_list()[:500]

    topic_model = BERTopic(verbose=True, n_gram_range=(1, 3), min_topic_size=7)
    topics, probs = topic_model.fit_transform(posts)
    plot_figures(created_at=created_at, posts=posts, topic_model=topic_model, topics=topics)

    print(topics)

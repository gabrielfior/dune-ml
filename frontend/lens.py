# This file has logic for displaying data from Lens API.
import boto3
import json
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import spacy
import streamlit as st
import os
from spacytextblob.spacytextblob import SpacyTextBlob
import pandas as pd
from io import BytesIO

def define_sentiment(polarity):
    if polarity < -0.3:
        return 'negative'
    elif polarity > 0.3:
        return 'positive'
    return 'neutral'

def extract_sentiment_from_content(nlp, content):
    doc = nlp(content)
    polarity = doc._.blob.polarity
    sentiment = define_sentiment(polarity)
    return sentiment

@st.experimental_memo(ttl=300)
def get_df_with_sentiment():
    nlp=spacy.load('xx_ent_wiki_sm')
    nlp.add_pipe('spacytextblob')

    # fetch publications from aws s3
    s3 = boto3.client('s3', aws_access_key_id=os.environ['AWS_ACCESS_KEY'],
                  aws_secret_access_key=os.environ['AWS_SECRET_KEY'])
    obj = s3.get_object(Bucket='dune-ml', Key='PUBLICATIONS.json')
    result = obj['Body'].read().decode('utf-8')
    lens_data = json.loads(result)
    df = pd.DataFrame(lens_data)
    #df = df.dropna()
    df['createdAt'] = pd.to_datetime(df['createdAt'])
    df['content'] = df['metadata'].apply(lambda x: x['content'])
    df['doc'] = df['content'].apply(nlp)
    df['sentiment'] = df['doc'].apply(lambda x: define_sentiment(x._.blob.polarity))
    
    df['is_positive'] = df['sentiment'] == 'positive'
    df['is_negative'] = df['sentiment'] == 'negative'
    df['is_neutral'] = df['sentiment'] == 'neutral'
    df['no_category'] = 1
    return df


def display(tab):
    tab.write('dune')

    df = get_df_with_sentiment()
    #print(df.head())

    # plotting
    grouped_data = df.groupby([pd.Grouper(key='createdAt', axis=0, freq='h')])[['is_negative','is_positive','is_neutral',
                                                              'no_category']].sum()
    #print(grouped_data.head())
    fig, ax = plt.subplots(figsize=(16,9))
    sns.lineplot(data=grouped_data, linewidth=2.5,ax=ax,  palette=['red', 'green','blue','black'])
    ax.xaxis.set_major_locator(plt.MaxNLocator(7))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y %H:%M'))
    ax.grid(True)
    fig.autofmt_xdate()
    #ax.legend(bbox_to_anchor=(1.04, 1), loc="upper left")
    #tab.pyplot(fig)

    buf = BytesIO()
    fig.savefig(buf, format="png")
    tab.image(buf)

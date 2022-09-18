# This file has logic for displaying data from Lens API.
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import streamlit as st
from spacytextblob.spacytextblob import SpacyTextBlob
import pandas as pd
from wordcloud import WordCloud
from io import BytesIO
from sklearn.feature_extraction import text
from s3_handler import S3Handler

@st.experimental_memo(ttl=300)
def get_df_with_sentiment():
    
    # fetch publications from aws s3
    s3_handler = S3Handler()
    lens_data = s3_handler.read_object('sentiment_publications_v2.json')
    df = pd.DataFrame(lens_data, columns=['createdAt','content','is_negative','is_positive','is_neutral','no_category'])
    df['createdAt'] = pd.to_datetime(df['createdAt'])
    return df    

def get_wordcloud_from_content(df, key, wordcloud_color):
    pos_words = df[df[key]]['content'].values
    stop_words = text.ENGLISH_STOP_WORDS.union(['https','http','com'])
    wc = WordCloud(background_color="white", max_words=500, colormap=wordcloud_color, stopwords=stop_words)    
    wc.generate_from_text(' '.join(pos_words))
    #print ('oi', 'https' in all_words)
    return wc

def plot_wordcloud(tab,df, key, title, wordcloud_color='Greens'):
    wc_pos = get_wordcloud_from_content(df, key=key, wordcloud_color=wordcloud_color)
    
    fig1, ax1 = plt.subplots(figsize=(16,9))
    ax1.imshow(wc_pos, interpolation='bilinear')
    ax1.set_title(title)
    ax1.set_axis_off()

    buf2 = BytesIO()
    fig1.savefig(buf2, format="png")
    tab.image(buf2)

def display(tab):

    tab.subheader('Sentiment analysis')
    
    tab.markdown('We used the excellent [spacy package](https://spacy.io/) for sentiment classification of Lens publications.')
    
    tab.markdown('Having the sentiment of each publication, we are able to plot the temporal evolution each sentiment (pos, neg, neutral).')
    
    df = get_df_with_sentiment()
    df.rename(columns={'no_category':'total'}, inplace=True)
        
    # plotting
    grouped_data = df.groupby([pd.Grouper(key='createdAt', axis=0, freq='h')])[['is_negative','is_positive','is_neutral',
                                                              'total']].sum()
    
    fig, ax = plt.subplots(figsize=(16,9))
    sns.lineplot(data=grouped_data, linewidth=2.5,ax=ax,  palette=['red', 'green','blue','black'])
    ax.xaxis.set_major_locator(plt.MaxNLocator(7))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y %H:%M'))
    ax.set_xlabel('Datetime')
    ax.set_ylabel('Number of publications')
    ax.grid(True)
    fig.autofmt_xdate()

    buf = BytesIO()
    fig.savefig(buf, format="png")
    tab.image(buf)

    # Wordcloud
    plot_wordcloud(tab,df,  'is_positive', title='Positive words', wordcloud_color='Greens')
    plot_wordcloud(tab,df,  'is_negative', title='Negative words', wordcloud_color='Reds')
    plot_wordcloud(tab,df,  'is_neutral', title='Neutral words', wordcloud_color='Blues')
# This file has logic for displaying data from Dune API.
import streamlit as st
import pandas as pd
from s3_handler import S3Handler
import matplotlib.dates as mdates
from io import BytesIO
import prophet
from prophet.plot import plot_plotly
import matplotlib.pyplot as plt

@st.experimental_memo(ttl=300)
def get_df_wallets():
    # fetch s3 data
    s3_handler = S3Handler()
    wallets_data = s3_handler.read_object('DUNE_wallets_per_day.json')
    return pd.DataFrame(wallets_data)
    

def display(tab):
    
    tab.subheader('Temporal evolution - Number of wallets that own a Lens Profile')
    
    tab.write('More and more people are joining Lens every day. We wanted to have a way to visualize the predicted growth, hence we used a [modular regression model](https://facebook.github.io/prophet/) for this task.')
    
    tab.markdown('Data source: [@niftytable Dune query](https://dune.com/queries/781918)')



    df = get_df_wallets()
    df['datetime'] = pd.to_datetime(df['day'])

    m = prophet.Prophet()
    df = df.rename(columns={'datetime':'ds','count':'y'})
    m.fit(df)
    future = m.make_future_dataframe(periods=30)
    forecast = m.predict(future)

    fig, ax = plt.subplots(figsize=(16,9))
    ax.xaxis.set_major_locator(plt.MaxNLocator(7))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y %H:%M'))
    ax.grid(True)
    fig.autofmt_xdate()
    #ax.legend(bbox_to_anchor=(1.04, 1), loc="upper left")
    fig1 = plot_plotly(m, forecast, xlabel='Datetime', ylabel='Number of wallets')    
    tab.plotly_chart(fig1)
    
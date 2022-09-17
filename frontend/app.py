import streamlit as st
st.set_page_config(layout="wide", page_title='Dune & Lens dashboard', initial_sidebar_state='expanded')
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pathlib
import dotenv
dotenv.load_dotenv(pathlib.Path(__file__).parent.parent.joinpath('.env'))
import dune
import lens
import info

st.title('Dune & Lens dashboard')

tab1, tab2, tab3 = st.tabs(["Dune", "Lens","Info"])

dune.display(tab1)


lens.display(tab2)


info.display(tab3)
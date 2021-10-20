import streamlit as st
import pandas as pd
import numpy as np
st.set_page_config(layout="wide")

"""
# My first app
Here's our first attempt at using data to create a table:
Start: streamlit run streamlitapp.py
"""

st.title('Uber pickups in NYC')

filename = st.text_input('Enter a file path:')
try:
    with open(filename) as input:
        #       df_test = pd.DataFrame(input)
        df_test = pd.read_csv(filename)
        st.text(df_test)

        df_test['yearMonth'] = df_test['DateTime'].str[:7]

        df_plot = df_test['yearMonth'].value_counts()
        col1, col2 = st.columns((1,2))
        with col1:
            chart1 = st.line_chart(df_plot)

        with col2:
            chart2 = st.line_chart(df_plot)

except FileNotFoundError:
    st.error('File not found.')

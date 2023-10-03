import streamlit as st
import preprocess
import re
import stats
import matplotlib.pyplot as plt
import numpy as np

st.sidebar.title('Whatsapp Chat Analyzer')

uploaded_file = st.sidebar.file_uploader('Choose a file')

if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode('utf-8')
    
    df = preprocess.preprocess(data)
    
    user_list = df['User'].unique().tolist()
    # st.dataframe(df)
    user_list.remove('Group Notification')
    user_list.sort()
    user_list.insert(0, "Overall")
    
    selected_user = st.sidebar.selectbox(
        "Show analysis with respect to", user_list
    )

    st.title("Whatsapp Chat Analysis for " + selected_user)
    
    if st.sidebar.button("Show Analysis"):
        num_messages, num_words, media_ommited, links = stats.fetch_stats(selected_user, df)

        col1, col2, col3, col4 = st.beta_columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)
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
    data = bytes_data.decode(encoding='utf-8')
    
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

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)

        with col2:
            st.header("Total No. of Words")
            st.title(num_words)

        with col3:
            st.header("Media Shared")
            st.title(media_ommited)

        with col4:
            st.header("Total Links Shared")
            st.title(links)

        if selected_user == 'Overall':
            st.title("Most Busy Users")
            busy_count, new_df = stats.fetch_busy_user(df)
            fig, ax  = plt.subplots()
            col1, col2 = st.columns(2)

            with col1:
                ax.bar(busy_count.index, busy_count.values, color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)

        st.title('Word Cloud')
        df_image = stats.create_world_cloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_image)
        st.pyplot(fig)

        most_common_df = stats.get_common_words(selected_user, df)
        fig, ax = plt.subplots()
        ax.barh(most_common_df[0], most_common_df[1])
        plt.xticks(rotation='vertical')
        st.title('Most Common words')
        st.pyplot(fig)

        emoji_df = stats.get_emoji_stats(selected_user, df)
        emoji_df.columns = ['Emoji', 'Count']

        st.title('Emoji Analysis')
        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)
        with col2:
            emoji_count = list(emoji_df['Count'])
            per_list = [(i/sum(emoji_count))*100 for i in emoji_count]
            emoji_df['Percentage use'] = np.array(per_list)
            st.dataframe(emoji_df)
        
        st.title('Monthly Timeline')
        time = stats.month_time_line(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(time['Time'], time['Message'], color='green')
        plt.xticks(rotation='vertical')
        plt.tight_layout()
        st.pyplot(fig)

        st.title("Activity Map")
        col1, col2 = st.columns(2)

        with col1:
            st.header("Most Busy Day")
            busy_day = stats.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='purple')
            plt.xticks(rotation='vertical')
            plt.tight_layout()
            st.pyplot(fig)

        with col2:
            st.header("Most Busy Month")
            busy_month = stats.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='purple')
            plt.xticks(rotation='vertical')
            plt.tight_layout()
            st.pyplot(fig)
            
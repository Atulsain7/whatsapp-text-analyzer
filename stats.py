import pandas as pd
import emoji
from urlextract import URLExtract
import collections
from wordcloud import WordCloud

extract = URLExtract()

def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['User']==selected_user] 

    num_messages = df.shape[0]

    words = []
    for message in df['Message']:
        words.extend(message.split())
    
    media_ommited = df[df['Message'] == '<Media omitted>']

    links = []
    for message in df['Message']:
        links.append(extract.find_urls(message))
    
    return num_messages, len(words), media_ommited.shape[0], len(links)

def fetch_busy_user(df):
    df = df[df['User'] != 'Group Notification']
    count = df['User'].value_counts().head()
    new_df = pd.DataFrame((df['User'].value_counts()/df.shape[0])*100)
    return count, new_df

def create_world_cloud(selected_user, df):
    pass
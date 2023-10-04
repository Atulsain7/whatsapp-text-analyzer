import pandas as pd
import emoji
from urlextract import URLExtract
from collections import Counter
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
    if selected_user != "Overall":
        df = df[df['User'] == selected_user]

    wc = WordCloud(width=500, height=500, 
                   min_font_size=10, background_color='white', font_path="TiroDevanagariHindi-Regular.ttf")
    df_wc = wc.generate(df['Message'].str.cat(sep=' '))
    return df_wc

def get_emoji_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['User']==selected_user]
    
    emojis = []
    for message in df['Message']:
        emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df

def get_common_words(selected_user, df):
    file = open('stop_hinglish.txt', 'r')
    stop_words = file.read()
    stop_words = stop_words.split('\n')

    if selected_user != 'Overall':
        df = df[df['User']==selected_user]

    tmp = df[(df['User']!='Group Notification')|
             (df['User']!='<Media omitted>')]
    
    words = []

    for message in tmp['Message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common = pd.DataFrame(Counter(words).most_common(20))
    return most_common

def month_time_line(select_user, df):
    if select_user != 'Overall':
        df = df[df['User'] == select_user] 

    temp = df.groupby(['Year', 'Month', 'Month Name']).count()['Message'].reset_index()

    time = []
    for i in range(temp.shape[0]):
        time.append(str(temp['Month'][i]) + "-" + str(temp['Year'][i]))

    temp['Time'] = time
    return temp

def week_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]
    return df['Day Name'].value_counts()

def month_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]
    return df['Month Name'].value_counts()

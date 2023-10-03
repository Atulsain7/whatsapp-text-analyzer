import re
import pandas as pd
from app import data


def get_time_and_date(text):
    date, time= text.split(',')
    date = date.replace(',', "")
    text = date.strip() + " " + time.strip()
    return text

def get_string(text):
    pass

def preprocess(data):
    pattern = 'd{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    df = pd.DataFrame({
        'user_messages': messages,
        'message_date': dates
    })

    df['message_date'] = df['message_date'].apply(lambda text: get_time_and_date(text))
    df.rename(columns={'message_date': 'date'}, inplace=True)

    users = []
    messages = []

    for message in df['user_messages']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('Group Notification')
            messages.append(entry[0])
    df['User'] = users
    df['message'] = messages
    df['message'] = df['message'].apply(lambda text: get_string(text))
    df.drop(columns=['user_messages'], axis=1)
    return df


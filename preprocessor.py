import re
import pandas as pd
def preprocess(data):
    pattern = r'\d{1,2}/\d{1,2}/\d{2},\s*\d{1,2}:\d{2}\s*(?:AM|PM|am|pm)\s*-\s*'

    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)
    clean_dates = [date.replace('\u202f', ' ') for date in dates]

    df = pd.DataFrame({'user_message': messages, 'message_date': clean_dates})

    df['message_date'] = df['message_date'].str.replace(' - .*', '', regex=True)

    # Rename the 'message_date' column to 'date'

    df.rename(columns={'message_date': 'msg_date'}, inplace=True)

    df['msg_date'] = pd.to_datetime(df['msg_date'], format='%m/%d/%y, %I:%M %p', errors='coerce')

    # Drop unnecessary columns
    df = df[['user_message', 'msg_date']]

    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('notification')
            messages.append(entry[0])
    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    df['year'] = df['msg_date'].dt.year
    df['month_num'] = df['msg_date'].dt.month
    df['m_date'] = df['msg_date'].dt.date
    df['month'] = df['msg_date'].dt.month_name()
    df['day'] = df['msg_date'].dt.day
    df['day_name'] = df['msg_date'].dt.day_name()
    df['hour'] = df['msg_date'].dt.hour
    df['minute'] = df['msg_date'].dt.minute

    return df
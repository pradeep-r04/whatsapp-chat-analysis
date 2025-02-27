from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import emoji


extract = URLExtract()
import matplotlib.pyplot as plt
def fetch_stat(selected_user, df):
    if selected_user != 'Overall':
        df =df[df['user'] == selected_user]

    num_messages = df.shape[0]
    words = []
    for message in df['message']:
        words.extend(message.split())

    # fetch num of media msgs
    no_media_msg = df[df['message'] == '<Media omitted>\n'].shape[0]

    # fetch links
    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))
    return num_messages, len(words), no_media_msg, len(links)

def most_busy_user(df):
    x = df['user'].value_counts().head()
    df  = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(columns={'count': 'percentage'})
    return x, df

def create_wordcloud(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    wc = WordCloud(width = 500, height=500, min_font_size=10, background_color='white')
    df_wc = wc.generate(df['message'].str.cat(sep = ""))
    return df_wc

def most_common_words(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    words = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)


    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    most_common_df.columns = ['Words', 'Count']
    return most_common_df


def emoji_analysis(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if emoji.is_emoji(c)])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    emoji_df.columns = ['Emojis', 'Count']
    return emoji_df

def timeline_analysis(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline

def daily_timeline(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    daily_timeline = df.groupby('m_date').count()['message'].reset_index()

    return daily_timeline

def weekly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()


def month_activity(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()
from urlextract import URLExtract
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji
import seaborn as sns

extract = URLExtract()


def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    num_messages = df.shape[0]
    words = []
    for message in df['message']:
        words.extend(message.split())
    # number of media shared
    num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]
    links = []
    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))

    return num_messages, len(words), num_media_messages, len(links)


def most_busy_users(df):
    x = df['user'].value_counts().head()
    df = round(df['user'].value_counts() / df.shape[0] * 100, 2).reset_index().rename(
        columns={'index': 'name', 'user': 'percent'})
    return x, df


def create_wordcloud(selected_user, df):
    f = open('hinglish.txt', 'r')
    stop_words = f.read()
    temp = df[df['user'] != 'group_notification']
    df = df[df['message'] != '<Media omitted>\n']
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    def remove_stop_words(message):
        t = []
        for word in message.lower().split():
            if word not in stop_words:
                t.append(word)
        return " ".join(t)

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    # temp['message'] = temp['message'].apply(remove_stop_words)
    df_wc = wc.generate(df['message'].str.cat(sep=" "))
    return df_wc


def most_common_words(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']
    f = open('hinglish.txt', 'r')
    stop_words = f.read()
    words = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    return_df = pd.DataFrame(Counter(words).most_common(20))
    return return_df


def emoji_helper(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    emojiss = []

    for message in df['message']:
        emojis = emoji.distinct_emoji_list(message)
        emojiss.extend([emoji.demojize(is_emoji) for is_emoji in emojis])
    emoji_icons = []
    for message in emojiss:
        emoji_icons.append(emoji.emojize(message))
    emoji_df = pd.DataFrame(Counter(emoji_icons).most_common(len(Counter(emoji_icons))))
    return emoji_df


def monthly_timeline(selected_user, df):
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
    daily_timelines = df.groupby('onlydate').count()['message'].reset_index()
    return daily_timelines


def week_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    return df['dayname'].value_counts()


def month_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    return df['month'].value_counts()

def activity_heatmap(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    heat_map=df.pivot_table(index='dayname', columns='period', values='message', aggfunc='count').fillna(0)
    return heat_map
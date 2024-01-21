  
import matplotlib

from lib.chatVisualizer.chat_Script import month_activity_map, week_activity_map
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import seaborn as sns
import matplotlib.pyplot as plt

def set_white_background(ax):
    ax.set_facecolor('white')

def plot_buzy_users(user, save_location):
    sns.set_theme(style="whitegrid")
    sns.set_palette('viridis')
    fig, ax = plt.subplots(figsize=(8, 6))
    set_white_background(ax)
    ax.bar(user.index, user.values, color='orange')
    plt.xticks(rotation='vertical')
    for label in ax.get_xticklabels() + ax.get_yticklabels():
        label.set_color('black')
    ax.tick_params(axis='both', colors='black')
    plt.savefig(f'{save_location}buzy_users.png', bbox_inches='tight')
    plt.close()

def plot_word_cloud(word_cloud_df, save_location):
    sns.set_theme(style="whitegrid")
    sns.set_palette('viridis')
    fig, ax = plt.subplots()
    set_white_background(ax)
    ax.imshow(word_cloud_df)
    plt.savefig(f'{save_location}chat_word_cloud.png', bbox_inches='tight')
    plt.close()

def plot_busy_month(selected_user, df, save_location):
    sns.set_theme(style="whitegrid")
    sns.set_palette('viridis')
    busy_month = month_activity_map(selected_user, df)
    fig, ax = plt.subplots(figsize=(8, 6))
    set_white_background(ax)
    sns.barplot(x=busy_month.index, y=busy_month.values, color='red')
    plt.xticks(rotation='vertical')
    ax.set_facecolor('white')
    ax.set_xlabel('Month', color='black')
    ax.set_ylabel('Activity', color='black')
    ax.set_title('Most Busy Month', color='black')
    ax.tick_params(axis='both', colors='black')
    plt.savefig(f'{save_location}buzy_month.png', bbox_inches='tight')
    plt.close()

def plot_busy_day(selected_user, df, save_location):
    sns.set_theme(style="whitegrid")
    sns.set_palette('viridis')
    busy_day = week_activity_map(selected_user, df)
    fig, ax = plt.subplots(figsize=(8, 6))
    set_white_background(ax)
    sns.barplot(x=busy_day.index, y=busy_day.values, color='yellow')
    plt.xticks(rotation=45)
    ax.set_facecolor('white')
    ax.set_xlabel('Day', color='black')
    ax.set_ylabel('Activity', color='black')
    ax.set_title('Most Busy Day', color='black')
    ax.tick_params(axis='both', colors='black')
    plt.savefig(f'{save_location}buzy_day.png', bbox_inches='tight')
    plt.close()

def plot_monthly_timeline(timeline, save_location):
    sns.set_theme(style="whitegrid")
    colors = sns.set_palette('viridis')
    fig, ax = plt.subplots(figsize=(8, 6))
    set_white_background(ax)
    sns.lineplot(data=timeline, x='time', y='message', color="red")
    plt.xticks(rotation=45)
    ax.set_xlabel('Time', color='black')
    ax.set_ylabel('Message', color='black')
    ax.set_title('Monthly Timeline', color='black')
    ax.tick_params(axis='both', colors='black')
    plt.savefig(f'{save_location}monthly_timeline.png', bbox_inches='tight')

def plot_daily_timeline(daily_timeline, save_location):
    sns.set_theme(style="whitegrid")
    colors = sns.color_palette('viridis')
    fig, ax = plt.subplots(figsize=(8, 6))
    set_white_background(ax)
    sns.lineplot(data=daily_timeline, x='only_date', y='message', color="red")
    plt.xticks(rotation=45)
    ax.set_facecolor('white')
    ax.set_xlabel('Date', color='black')
    ax.set_ylabel('Message', color='black')
    ax.set_title('Daily Timeline', color='black')
    ax.tick_params(axis='both', color='black')
    plt.savefig(f'{save_location}daily_timeline.png', bbox_inches='tight')

def plot_most_common_words(most_common_df, save_location):
    sns.set_theme(style="whitegrid")
    colors = sns.set_palette('viridis')
    fig, ax = plt.subplots(figsize=(8, 6))
    set_white_background(ax)
    ax.barh(most_common_df[0], most_common_df[1], color=colors)
    ax.set_facecolor('white')
    ax.set_xlabel('Count', color='black')
    ax.set_ylabel('Words', color='black')
    ax.set_title('Most Common Words', color='black')
    ax.tick_params(axis='both', colors='black')
    ax.invert_yaxis()
    plt.savefig(f'{save_location}common_words.png', bbox_inches='tight')

def plot_emoji_pie_chart(emoji_df, save_location):
    sns.set_theme(style="whitegrid")
    fig, ax = plt.subplots(figsize=(8, 6))
    set_white_background(ax)
    ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct='%1.1f%%', colors=['white'] * len(emoji_df[0]))
    plt.setp(ax.pie(emoji_df[1].head(), labels=emoji_df[0].head())[1], color='white')
    ax.set_title('Emoji Distribution', color='black')
    plt.savefig(f'{save_location}emoji.png', bbox_inches='tight', transparent=True)
    plt.close()

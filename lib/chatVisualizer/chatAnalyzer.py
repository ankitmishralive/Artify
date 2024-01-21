# Assuming chat_preprocessor and chat_Visualization are modules in the lib package
from lib.chatVisualizer.chat_Visualization import plot_busy_day, plot_busy_month, plot_buzy_users, plot_daily_timeline, plot_emoji_pie_chart, plot_monthly_timeline, plot_most_common_words, plot_word_cloud
from lib.chatVisualizer.chat_preprocessor import preprocess
from lib.chatVisualizer.chat_Script import create_wordcloud,  fetch_busy_users, fetch_stats,  monthly_timeline,daily_timeline, most_common_words
import pandas as pd 
# Import other necessary functions and classes



def user_Selection(chat_location):
    with open(chat_location, 'rb') as file:
        bytes_data = file.read()
        data = bytes_data.decode("utf-8")
    # bytes_data = chat_location.getvalue()
    # data = bytes_data.decode("utf-8") 
        
    # print("Raw Data:", data)
    df,df_ios = preprocess(data)
    # print("Processed Dataframe:", df)
    # print("Processed Dataframe Shape:", df.shape)
    # print("Processed Dataframe Head:", df.head())
    user_list = df['user'].unique().tolist()
    user_list.sort()
    user_list.insert(0, "Overall")  
    if 'group_notification' in user_list:
         user_list.remove('group_notification')
   
    data={
            "user_list" : user_list,
            "text" : "Visualize",
           
        }
    return data





def Analyze_Chat(chat_location,selected_user,drop_location):
    # print(chat_location)
    # with open(chat_location, 'rb') as file:
    #     bytes_data = file.read()
    #     print("Bytes Data (Length):", len(bytes_data))
    #     print("Bytes Data (Preview):", bytes_data[:100])  # Print the first 100 characters as a preview
    #     data = bytes_data.decode("utf-8")
    #     print("Decoded Data (Length):", len(data))
    #     print("Decoded Data (Preview):", data[:100])  # Print the first 100 characters of the decoded data



    with open(chat_location, 'rb') as file:
        bytes_data = file.read()
        data = bytes_data.decode("utf-8")
    # bytes_data = chat_location.getvalue()
    # data = bytes_data.decode("utf-8") 
    print("Selected User :--------- ",selected_user)
    print("Raw Data:", data)
    df,df_ios = preprocess(data)
    # print("Processed Dataframe:", df)
    # print("Processed Dataframe Shape:", df.shape)
    # print("Processed Dataframe Head:", df.head())
    # user_list = df['user'].unique().tolist()
    # user_list.remove('group_notification')  
    # user_list.sort()

    # user_list.insert(0, "Overall")  

    # selected_user = "Overall"
    # print("Selected User :--------- ",selected_user)

    num_messages, words, media_messages, links = fetch_stats(selected_user, df)
    # print(num_messages)
    # print(words)
    # print(media_messages)
    # print(links)

 


    # Buzy Users in Group ( Only for Group )

    user,user_contro_percent_dict = fetch_busy_users(df)
    plot_buzy_users(user,drop_location)
    # All_user_contribution_percent_dict = new_df.set_index('user')['percent'].to_dict()
    # Convert 'name' and 'percent' columns to dictionary
    
    # print("new DF--- ",new_df)
    # print("---All User--: ",All_user_contribution_percent_dict)

    #  Word Cloud 

    word_cloud_df=create_wordcloud(selected_user, df)
    plot_word_cloud(word_cloud_df,drop_location)


    # Most Buzy Day & Most Buzy Month Side by Side 
    print("------------Most Buzy Day & Month----------------")
    print("User : ",selected_user)
    print("DataFrame :",df)


    plot_busy_month(selected_user,df,drop_location)
    plot_busy_day(selected_user,df,drop_location)



    # Monthly Time Line 
    timeline = monthly_timeline(selected_user,df)
    plot_monthly_timeline(timeline,drop_location)

    # Daily Time Line 

    dailytimeline = daily_timeline(selected_user, df)
    plot_daily_timeline(dailytimeline,drop_location)


    # Most Common Words 
    most_common_df = most_common_words(selected_user,df)
    plot_most_common_words(most_common_df,drop_location)


    # Emoji 
    # emoji_df = emoji_helper(selected_user,df)
    # plot_emoji_pie_chart(emoji_df,drop_location)
  


      

    if selected_user =="Overall":

        analytical_data ={
            "num_messages" : num_messages,
            'words':words,
            'media_messages':media_messages,
            'links':links,
            'user_contro_percent_dict':user_contro_percent_dict
        }

        return analytical_data
    else:
        analytical_data ={
            "num_messages" : num_messages,
            'words':words,
            'media_messages':media_messages,
            'links':links
        }

        return analytical_data


def Summarize():
    pass

    
    # Rest of your code...

# Add other imports and functions as needed

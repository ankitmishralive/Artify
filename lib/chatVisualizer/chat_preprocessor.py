import pandas as pd
import re



# --- below one is working properly for 1 format --------------------

# def preprocess(data):
#     datp1 = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
#     datp2 = '^(\d{1,2}\/\d{1,2}\/\d{1,2}, \d{1,2}:d{1,2} \w\w)'
#     pattern = datp1 or datp2
#     #pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s' or '^(\d{1,2}\/\d{1,2}\/\d{1,2}, \d{1,2}:d{1,2} \w\w)'
#     messages = re.split(pattern, data)[1:]
#     dates = re.findall(pattern, data)
#     df = pd.DataFrame({'user_message': messages, 'message_date': dates})
#     # Converting Message Date Type...
#     # dm= "%d/%m/%Y, %H:%M - "
#     # md = "%m/%d/%Y, %H:%M - "
#     # od = "%m/%d/%y, %H:%M - "
#     df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%Y, %H:%M - ')
#     #df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%Y, %H:%M - 'or' %m/%d/%Y, %H:%M - ')
#     df.rename(columns={'message_date': 'date'}, inplace=True)
#     # Separate users & Messages
#     users = []
#     messages = []
#     for message in df['user_message']:

#         entry = re.split('([\w\W]+?):\s', message)  # regex for name aur jbhtl : yeah nahi aata vpo regex hai
#         if entry[1:]:  # user name
#             users.append(entry[1])
#             messages.append(" ".join(entry[2:]))
#            # messages.append(entry[2])
#         else:
#             users.append('group_notification')
#             messages.append(entry[0])

#     df['user'] = users
#     df['message'] = messages
#     df.drop(columns=['user_message'], inplace=True)
#     df['year'] = df['date'].dt.year
#     df['month_num'] = df['date'].dt.month
#     df['month'] =  df['date'].dt.month_name()
#     df['day'] = df['date'].dt.day
#     df['day_name']=df['date'].dt.day_name()

#     df['hour'] = df['date'].dt.hour
#     df['minute'] = df['date'].dt.minute

#     df['only_date'] = df['date'].dt.date

#     return df



# import pandas as pd
# import re

# def preprocess(data):
#     datp1 = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
#     datp2 = '^(\d{1,2}\/\d{1,2}\/\d{1,2}, \d{1,2}:\d{1,2} \w\w)'
#     datp3 = "\[\d{1,2}/\d{1,2}/\d{2,4}, \d{2}:\d{2}:\d{2} [APMapm]{2}\] \w+: .*"


#     pattern =  datp1 or  datp2 or datp3


   

#     messages = re.split(pattern, data)[1:]
#     dates = re.findall(pattern, data)
    
#     df = pd.DataFrame({'user_message': messages, 'message_date': dates})
    
#     # Converting Message Date Type...
#     df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%Y, %H:%M - ', errors='coerce')
#     df.rename(columns={'message_date': 'date'}, inplace=True)
    
#     # Separate users & Messages
#     users = []
#     messages = []
    
#     for message in df['user_message']:
#         entry = re.split('([\w\W]+?):\s', message)
#         if entry[1:]:  # user name
#             users.append(entry[1])
#             messages.append(" ".join(entry[2:]))
#         else:
#             users.append('group_notification')
#             messages.append(entry[0])

#     df['user'] = users
#     df['message'] = messages
#     df.drop(columns=['user_message'], inplace=True)
    
#     df['year'] = df['date'].dt.year
#     df['month_num'] = df['date'].dt.month
#     df['month'] = df['date'].dt.month_name()
#     df['day'] = df['date'].dt.day
#     df['day_name'] = df['date'].dt.day_name()

#     df['hour'] = df['date'].dt.hour
#     df['minute'] = df['date'].dt.minute

#     df['only_date'] = df['date'].dt.date

#     return df




import pandas as pd

def preprocess(data):
    messages = []
    dates = []
    is_ios = False

    for line in data.split('\n'):
        if line.strip() == "":
            continue

        parts = line.split(" - ", 1)
        if len(parts) > 1:
            date_str, message = parts
            dates.append(pd.to_datetime(date_str.strip(), errors='coerce'))
            messages.append(message)
        elif line.startswith("["):
            is_ios = True
            date_str, message = line.split("] ", 1)
            dates.append(pd.to_datetime(date_str[1:].strip(), format='%d/%m/%y, %I:%M:%S %p', errors='coerce'))
            messages.append(message)

        # elif line.startswith("["):
        #     is_ios = True
        #     date_str, message = line.split("] ", 1)
        #     dates.append(pd.to_datetime(date_str[1:].strip(), format='%d/%m/%y, %I:%M:%S%p', errors='coerce'))
        #     messages.append(message)
        else:
            # Handle the case where a message starts without a timestamp (continuation of the previous message)
            messages[-1] += " " + line

    df = pd.DataFrame({'user_message': messages, 'message_date': dates})

    # Converting Message Date Type...
    df['message_date'] = pd.to_datetime(df['message_date'], errors='coerce')
    df.rename(columns={'message_date': 'date'}, inplace=True)

    # Separate users & Messages
    users = []
    messages = []

    for message in df['user_message']:
        entry = message.split(': ', 1)
        if len(entry) > 1:
            users.append(entry[0])
            messages.append(entry[1])
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()

    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    df['only_date'] = df['date'].dt.date

    # Add braces to text in a for loop
   # Add braces to text in a for loop
    for i in range(len(df)):
        df.loc[i, 'message'] = f"{{{df.loc[i, 'message']}}}"

    # Remove braces from text in a for loop
    for i in range(len(df)):
        df.loc[i, 'message'] = df.loc[i, 'message'].strip("{}")


    return df, is_ios





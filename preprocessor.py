import pandas as pd
import re

def preprocess(data):
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s?[ap]m\s-\s'

    messages = re.split(pattern,data)[1:]

    dates = re.findall(pattern,data)

    dates = [item.replace('\u202f', ' ') for item in dates]

    dates = [item.replace(' - ', '') for item in dates]

    df = pd.DataFrame({'user_message': messages, 'message_date': dates})

# Convert 'message_date' to datetime without stripping 'am/pm'
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%Y, %I:%M %p')

# Rename column
    df.rename(columns={'message_date': 'date'}, inplace=True)
    df['date'] = df['date'].dt.strftime('%Y-%m-%d %I:%M:%S %p')

    users = []
    messages = []


    for message in df['user_message']:
       entry = re.split('([\w\W]+?):\s',message)
       if entry[1:]:
         users.append(entry[1])
         messages.append(entry[2])
       else:
         users.append('group_notification')
         messages.append(entry[0])

    df['user'] =users
    df['message'] = messages

    df.drop(columns=['user_message'],inplace=True)

    df['date'] = pd.to_datetime(df['date'])

# Extract the year
    df['year'] = df['date'].dt.year

    df['month'] = df['date'].dt.month_name()
    df['only_date']=df['date'].dt.date
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['month_num'] = df['date'].dt.month
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    df['time_of_day'] = df['date'].dt.strftime('%p')


    # Create the period list based on the hour and time of day (AM/PM)
    period = []
    for hour, time_of_day in zip(df['hour'], df['time_of_day']):
     if hour == 0:
        period.append(f"12-01 {time_of_day}")
     elif hour == 12:
        period.append(f"12-01 {time_of_day}")
     elif hour < 12:
        period.append(f"{hour:02}-{hour+1:02} {time_of_day}")
     else:
        period.append(f"{hour-12:02}-{hour-11:02} {time_of_day}")

# Add the period column to the DataFrame
    df['period'] = period

# Create a sort key for time of day (AM before PM) and hour
    df['time_sort'] = df['time_of_day'].apply(lambda x: 0 if x == 'AM' else 1)
    df['hour_sort'] = df['hour'] % 12  # Convert to 12-hour format for proper sorting

# Sort the DataFrame by time of day and hour
    df = df.sort_values(by=['time_sort', 'hour_sort'])

    return df


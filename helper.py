from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import re
import string
import emoji
import joblib
import sklearn



extractor = URLExtract()

def fetch_stats(selected_user, df):


   if selected_user != 'Overall':
      df = df[df['user'] == selected_user]


   
   num_messages = df.shape[0]
   # fetch number of words
   words = []
   for message in df['message']:
    words.extend(message.split())

   # fetch number of  media messages

   number_media = df[df['message'] == '<Media omitted>\n'].shape[0]

   # fetch number of links

   link = []

   for message in df['message']:
     link.extend(extractor.find_urls(message))
    



   return num_messages, len(words) ,number_media,len(link)


def most_busy_users(df):
    
    x = df['user'].value_counts().head()

    
    df = df[~df['user'].isin(['Meta AI', 'group_notification'])]

    df_percentage = (df['user'].value_counts(normalize=True) * 100).round(2).reset_index()
    df_percentage.columns = ['name', 'percent']

    return x, df_percentage

def create_worldcloud(selected_user,df):
       
   f = open('stop_hinglish.txt','r')
   stop_words = f.read()

   if selected_user != 'Overall':
      df = df[df['user'] == selected_user]


   temp=df[df['user'] != 'group_notification']
   temp = temp[temp['message'] != '<Media omitted>\n']

   def remove_stop_words(message):
         words = []
         message = message.translate(str.maketrans('', '', string.punctuation))
         for word in message.lower().split():
            if word not in stop_words and not re.search(r'\d', word):
               words.append(word)
         
         return " ".join(words)

   wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')
   temp['message'] = temp['message'].apply(remove_stop_words)
   df_wc = wc.generate(temp['message'].str.cat(sep=" "))
   return df_wc


def most_common_words(selected_user,df):
      
       f = open('stop_hinglish.txt','r')
       stop_words = f.read()

       if selected_user != 'Overall':
        df = df[df['user'] == selected_user]


       temp=df[df['user'] != 'group_notification']
       temp = temp[temp['message'] != '<Media omitted>\n']
       words = []
       for message in temp['message']:
         message = message.translate(str.maketrans('', '', string.punctuation))
         for word in message.lower().split():
            if word not in stop_words and not re.search(r'\d', word):
              words.append(word)

    
       most_common_df = pd.DataFrame(Counter(words).most_common(20))
       return most_common_df


def emoji_helper(selected_user,df):

      if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

      
      emojis = []
      for message in df['message']:
         emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

      emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
  
      
      return emoji_df

def monthly_timeline(selected_user,df):

     
     if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

     
     timeline = df.groupby(['year','month_num','month']).count()['message'].reset_index()

     time = []
     for i in range(timeline.shape[0]):
      time.append(timeline['month'][i]+"-"+str(timeline['year'][i]))

     timeline['time'] = time
      
     return timeline


def daily_timeline(selected_user,df):

     
     if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

     
     daily_timeline = df.groupby('only_date').count()['message'].reset_index()

     
      
     return daily_timeline

     
def week_activity_map(selected_user,df):
   if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

   return df['day_name'].value_counts()

def month_activity_map(selected_user,df):
   if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

   return df['month'].value_counts()


def activity_heatmap(selected_user,df):
      if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

      pivot_table = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)
      # Reorder the columns to ensure AM comes before PM
      sorted_columns = sorted(pivot_table.columns, key=lambda x: (x[-2:], int(x.split('-')[0])))
      pivot_table = pivot_table[sorted_columns]

      return pivot_table


import re
import joblib
from collections import Counter

def topic_modeling(selected_user, df):
    # Load the model and vectorizer
    model = joblib.load('model.pkl')  # Replace with your model file
    vectorizer = joblib.load('vectorizer.pkl')
    
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    def clean_text(text):
        # Remove numbers
        text = re.sub(r'\d+', '', text)
        # Remove links
        text = re.sub(r'http\S+|www\S+', '', text)
        # Remove emojis (This is a basic regex for emojis, might not cover all cases)
        text = re.sub(r'[^\w\s]', '', text)
        # Remove extra whitespace
        text = text.strip()  # Optional: to remove leading and trailing whitespace
        return text

    # Apply the clean_text function to the 'message' column
    df['cleaned_message'] = df['message'].apply(clean_text)
    
    new_data = df['cleaned_message']

    # Step 1: Vectorize the new input data
    new_vectorized = vectorizer.transform(new_data)

    # Step 2: Make predictions
    predictions = model.predict(new_vectorized)

    # Step 3: Output the predictions and count occurrences
    topic_counts = Counter()
    for text, prediction in zip(new_data, predictions):
        topic_counts[prediction] += 1  # Increment the count for the predicted topic

   
    for topic, count in topic_counts.most_common(4):  # Get the top 4 most common topics
        print(f"{topic}: {count}")

    return topic_counts.most_common(4)  # Return the most common topics and counts


      

      

import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
import seaborn as sns

# Set page configuration
st.set_page_config(page_title="WhatsApp Chat Analyzer", layout="wide")


st.sidebar.title("WhatsApp Chat Analyzer")
# Custom CSS for styling
st.markdown(
    """
    <style>
    body {
        background-color: #f0f4f7;
        color: #333;
    }
    .sidebar .sidebar-content {
        background-color: #ffffff;
    }
    h1, h2, h3 {
        font-family: 'Arial', sans-serif;
    }
   .stMetric {
        background-color: #e3f2fd;
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 10px;
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    # Fetch unique users
    user_list = df['user'].unique().tolist()
    user_list = [user for user in user_list if user not in ['Meta AI', 'group_notification']]
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)

    if st.sidebar.button("Show Analysis"):
        num_messages, words, num_media_messages, links = helper.fetch_stats(selected_user, df)

        st.title("Top Statistics")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.subheader(num_messages)
        with col2:
            st.header("Total Words")
            st.subheader(words)
        with col3:
            st.header("Media Shared")
            st.subheader(num_media_messages)
        with col4:
            st.header("Links Shared")
            st.subheader(links)


         # Assuming `selected_user` and `df` are defined somewhere in your Streamlit app
        topic_modeling = helper.topic_modeling(selected_user, df)

   

        st.title("Most Discussed Topics:")
        col1 = st.columns(1)

        with col1[0]:  # Access the first column
    # Display the topics in the first column
         
         for topic, _ in topic_modeling:
          st.subheader(topic)

        # Monthly timeline
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(timeline['time'], timeline['message'], color='green', marker='o')
        plt.xticks(rotation='vertical')
        plt.grid()
        st.pyplot(fig)

        # Daily timeline
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
        plt.xticks(rotation='vertical')
        plt.grid()
        st.pyplot(fig)

        # Activity map
        with st.expander("Activity Map", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                st.header("Most Busy Day")
                busy_day = helper.week_activity_map(selected_user, df)
                fig, ax = plt.subplots()
                ax.bar(busy_day.index, busy_day.values, color='purple')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                st.header("Most Busy Month")
                busy_month = helper.month_activity_map(selected_user, df)
                fig, ax = plt.subplots()
                ax.bar(busy_month.index, busy_month.values, color='orange')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

        # Week-Time Heatmap
        st.title("Week - Time Heatmap")
        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        plt.yticks(rotation='horizontal')
        ax = sns.heatmap(user_heatmap, cmap="YlGnBu")
        st.pyplot(fig)

        # Most Busy Users
        if selected_user == 'Overall':
            st.title('Most Busy Users')
            x, new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()
            ax.bar(x.index, x.values, color='red')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
            st.dataframe(new_df)

       


        # Word Cloud
        st.title("Word Cloud")
        df_wc = helper.create_worldcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # Most Common Words
        most_common_df = helper.most_common_words(selected_user, df)
        fig, ax = plt.subplots()
        ax.barh(most_common_df[0], most_common_df[1])
        plt.xticks(rotation='vertical')
        st.title('Most Common Words')
        st.pyplot(fig)

        # Emoji Analysis
        emoji_df = helper.emoji_helper(selected_user, df)
        st.title("Emoji Analysis")
        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)

        with col2:
            fig, ax = plt.subplots()
            ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct="%0.2f%%")
            st.pyplot(fig)

      



# Add footer at the bottom of the page
footer = """
    <footer class="footer">
        <div class="footer-text">
            <p>Copyright &copy; 2024 by AbuBakar Shahzad | All Rights Reserved</p>
        </div>
    </footer>
    <style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background: rgb(14, 17, 23);
        color: white;
        text-align: center;
        padding: 10px;
    }
     .footer::before {
        content: "";
        display: block;
        height: 2px;
        width: 100%;
        background-color: rgb(38, 39, 48);
        margin-bottom: 20px;
    }
    .footer-text p {
        margin-top: 15px;
    }
    .footer-text {
        font-family: 'Arial', sans-serif;
    }
    </style>
    """
st.markdown(footer, unsafe_allow_html=True)

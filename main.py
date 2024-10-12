import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt

st.sidebar.title("WhatsApp Chat Analyzer!")
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    # st.dataframe(df)
    user_list = df['user'].unique().tolist()
    user_list.remove('notification')
    user_list.sort()
    user_list.insert(0, "Overall")
    selected_user = st.sidebar.selectbox("Show Analysis wrt", user_list)

    if st.sidebar.button("Show Analysis."):

        num_messages, words, no_media_msg, links =  helper.fetch_stat(selected_user, df)
        st.title("Top Statistics:")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)

        with col2:
            st.header("Total Words")
            st.title(words)

        with col3:
            st.header("Total Media Files Shared")
            st.title(no_media_msg)

        with col4:
            st.header("Total Links Shared")
            st.title(links)

        #Monthly timeline
        st.title("Monthly Timeline")
        timeline = helper.timeline_analysis(selected_user, df)
        fig, ax = plt.subplots()
        plt.plot(timeline['time'], timeline['message'], color='red')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Daily Timeline
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        daily_timeline = daily_timeline.dropna()
        fig, ax = plt.subplots()
        plt.plot(daily_timeline['m_date'],daily_timeline['message'], color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Activity manager
        st.title("Activity Map")
        col1, col2 = st.columns(2)

        with col1:
            st.header("Most Busy Day")
            busy_day = helper.weekly_timeline(selected_user, df)

            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values)
            st.pyplot(fig)
        with col2:
            st.header("Most Busy Month")
            busy_month = helper.month_activity(selected_user, df)

            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        if selected_user == 'Overall':
            st.title('Most Busy Users')
            x, new_df = helper.most_busy_user(df)
            fig, ax = plt.subplots()
            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values)
                plt.xticks(rotation = 'vertical')
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)

        # wordcloud
        st.title("Word Cloud")
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # most common words
        st.title("Most Common Words")
        most_common_df = helper.most_common_words(selected_user, df)

        fig, ax = plt.subplots()
        ax.barh(most_common_df['Words'], most_common_df['Count'])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        st.dataframe(most_common_df)

        # emoji analysis
        st.title("Emoji Analysis.")
        emoji_df = helper.emoji_analysis(selected_user, df)
        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig, ax = plt.subplots()
            ax.pie(emoji_df['Count'].head(10), labels=emoji_df['Emojis'].head(10),autopct="%0.2f")
            st.pyplot(fig)



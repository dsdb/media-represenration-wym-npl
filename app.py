import streamlit as st
import pandas as pd
#import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import media_represntation


def main():    

    # Add logo
    logo_image = 'logo\onlinekhabar.png'
    st.image(logo_image, use_column_width=True)

    st.title("Media Representation Dashboard")

    # Static list of categories
    categories = [' ','economy', 'lifestyle', 'sports']

     # Select a category
    selected_category = st.selectbox("Select a Category", categories)
    st.write("Selected Category:", selected_category)
   
   # Process the news content
    visualization_btn = st.button("Generate visualization")
    if visualization_btn:
        media_represntation.process_news_content()          
        st.write("Processed data for visualization")

    # Process the data and generate sentiment chart    
    if selected_category in media_represntation.proccessed_df:
        sentiment_result = media_represntation.proccessed_df[selected_category]           
        sentiment_chart = plt.figure()
        sns.barplot(data=sentiment_result, x="sentiment", y="sentiment_count", palette='Set2')
        plt.title(f"Sentiment Analysis for {selected_category} Category")
        plt.xlabel("Sentiment")
        plt.ylabel("Count")
        st.pyplot(sentiment_chart)
        
        # Process the data and generate keyword chart
        keyword_result = media_represntation.proccessed_df[selected_category]                     
        keyword_chart = plt.figure()
        sns.barplot(data=keyword_result, x="keyword_present", y="keyword_count", palette='Set1')
        plt.title(f"Keyword Representation for {selected_category} Category")
        plt.xlabel("Keyword")
        plt.ylabel("Count")
        st.pyplot(keyword_chart)

    else:
        st.write(f"No data available for the selected category: {selected_category}")


if __name__ == "__main__":
    main()

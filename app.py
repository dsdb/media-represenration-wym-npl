import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import media_representation
from media_representation import news_df, news_dict
from wordcloud import WordCloud



def main():    

    # Add logo
    logo_image = 'logo/onlinekhabar.png'
    st.image(logo_image, use_column_width=True)

    st.title("Media Representation Dashboard")

    # Static list of categories
    categories = [' ','economy', 'lifestyle', 'sports']

     # Select a category
    selected_category = st.selectbox("Select a Category", categories)
    st.write("Selected Category:", selected_category)
   

    def generate_visualtion(category):        
        # Load data and process based on selected category
        news_df, news_dict = media_representation.process_news_content()      
        # Process the data and generate sentiment chart    
        if category in media_representation.proccessed_df:
            sentiment_result = media_representation.proccessed_df[category]           
            sentiment_chart = plt.figure()
            sns.barplot(data=sentiment_result, x="sentiment", y="sentiment_count", palette='Set2')
            plt.title(f"Sentiment Analysis for {category} Category")
            plt.xlabel("Sentiment")
            plt.ylabel("Count")
            st.pyplot(sentiment_chart)

            positive_text = ' '.join(news_dict[selected_category][news_dict[selected_category]['sentiment'] == 'positive']['preprocessed_content'])
            # Postive sentiment word cloud
            positive_word_cloud = WordCloud(width=400, height=400, background_color='white').generate(positive_text)            
            
            negative_text = ' '.join(news_dict[selected_category][news_dict[selected_category]['sentiment'] == 'negative']['preprocessed_content'])
            # Negative sentiment word cloud
            negative_word_cloud = WordCloud(width=400, height=400, background_color='white').generate(negative_text)

            #Display word clouds 
            st.title('Sentiment-Based Word Clouds')
            st.subheader('Positive Sentiment')
            st.image(positive_word_cloud.to_array(), use_column_width=True)

            st.subheader('Negative Sentiment')
            st.image(negative_word_cloud.to_array(), use_column_width=True)

                
            # Process the data and generate keyword chart
            keyword_result = media_representation.proccessed_df[category]                     
            keyword_chart = plt.figure()
            sns.barplot(data=keyword_result, x="keyword_present", y="keyword_count", palette='Set1')
            plt.title(f"Keyword Representation for {category} Category")
            plt.xlabel("Keyword")
            plt.ylabel("Count")
            st.pyplot(keyword_chart)
            st.write("Processed data for visualization")

            # keyword_text = ' '.join(news_dict[selected_category][news_dict[selected_category]['keyword_present']]['preprocessed_content'])
           
            # # Keyword word cloud
            # keyword_word_cloud = WordCloud(width=400, height=400, background_color='white').generate(keyword_text)

            # st.text_input('keyword Presence Word Cloud')
            # st.image(keyword_word_cloud.to_array(), use_column_width=True)
            
   # Process the news content    
    if st.button("Generate visualization"):
        generate_visualtion(selected_category) 
    else:
        st.write(f"No data available for the selected category: {selected_category}")


if __name__ == "__main__":
    main()

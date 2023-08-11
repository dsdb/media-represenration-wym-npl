import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import media_represntation


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
   
   # Process the news content    
    if st.button("Generate visualization"):
        generate_visualtion(selected_category)     

    def generate_visualtion(category):        
        # Load data and process based on selected category
        media_represntation.process_news_content()      
        # Process the data and generate sentiment chart    
        if category in media_represntation.proccessed_df:
            sentiment_result = media_represntation.proccessed_df[category]           
            sentiment_chart = plt.figure()
            sns.barplot(data=sentiment_result, x="sentiment", y="sentiment_count", palette='Set2')
            plt.title(f"Sentiment Analysis for {category} Category")
            plt.xlabel("Sentiment")
            plt.ylabel("Count")
            st.pyplot(sentiment_chart)
            
            # Process the data and generate keyword chart
            keyword_result = media_represntation.proccessed_df[category]                     
            keyword_chart = plt.figure()
            sns.barplot(data=keyword_result, x="keyword_present", y="keyword_count", palette='Set1')
            plt.title(f"Keyword Representation for {category} Category")
            plt.xlabel("Keyword")
            plt.ylabel("Count")
            st.pyplot(keyword_chart)
            st.write("Processed data for visualization")
        else:
            st.write(f"No data available for the selected category: {category}")


if __name__ == "__main__":
    main()

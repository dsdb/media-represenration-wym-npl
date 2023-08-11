# Import import packages
import pandas as pd
import spacy
import os
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import re
from bs4 import BeautifulSoup
import unicodedata
import emoji
import seaborn as sns
import plotly.express as px
import matplotlib.pyplot as plt


# load spacy model and sentiment analyzer
#model_path = "model\en_core_web_sm\en_core_web_sm-3.6.0"
model_path = "model/en_core_web_sm/en_core_web_sm-3.6.0"
nlp_spacy = spacy.load(model_path)
nlp_sia = SentimentIntensityAnalyzer()


# Expose datafrane and Dictionary
news_df = None
news_dict = None

# List of news categories and their respecive CSV files
category_files = {
    #'political': 'data\Political\onlinekhabar_political_uptopageno209_data.csv',
    'economy': 'data\Economy\onlinekhabar_economy_uptopageno209_data.csv',
    'lifestyle': 'data\Lifestyle\onlinekhabar_lifestyle_uptopageno209_data.csv',
    'sports': 'data\Sports\onlinekhabar_sports_uptopageno209_data.csv',
    #'travel': 'data\Travel\onlinekhabar_travel_uptopageno209_data.csv'
}

# Dictionary to hold processed dataframe for each category
proccessed_df = {}


# Load NLTK resources
nltk_data_path = os.path.join(os.getcwd(), 'nltk_data')
os.environ['NLTK_DATA'] = nltk_data_path

nltk_corpus = ['punkt','stopwords','wordnet','gutenburg','inaugural','webtext', 'vader_lexicon']

for corpus in nltk_corpus:
    nltk.download(corpus)

# Text Preprocessing
def preprocess_text(text):    

    # Text Cleaning and Tokenization
    text = re.sub(r'\s+', ' ', text)  
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\d+', ' ', text)
    text = text.strip()
    tokens = word_tokenize(text)
    
    # Lowercasing
    tokens = [token.lower() for token in tokens]
    
    # Stopword Removal
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]
    
    # Lemmatization
    lemmatizer = WordNetLemmatizer() 
    tokens = [lemmatizer.lemmatize(token) for token in tokens]
    
    # Word Replacements
    replacements = {'u.s.': 'united states', 'govt': 'government'}
    tokens = [replacements.get(token, token) for token in tokens]
    
    # Remove consecutitive repetitive words
    token = [token for i , token in enumerate(tokens) if i== 0 or token != tokens[1 -1]]
    
    # Combine tokens back to text
    preprocessed_text = ' '.join(tokens)
    return preprocessed_text

# Keywords and entities
keywords = ['Women', 'women', 'Female', 'female', 'youth', 'youths', 'Male', 'male', 'minority', 
            'marginal','marginalized groups', 'province 2', 'province 5', 'Koshi', 'Madesh', 'Bagmati',
              'Gandaki', 'Lumbini', 'Karnali', 'Sudupaschim', 'Bantar','Chamar', 'Harijan','Dhobi','Dom','Dusadh','Pasawan', 'Pasi',
              'Halkhor','Khatwe', 'Musahar', 'Tatma', 'Tatwa',]

# Entity Recognition
def analyze_entities(text):
    news_content = nlp_spacy(text)
    # extract recognized entities
    recognized_entities = [ent.text.lower() for ent in news_content.ents]
    # Check if keywords or entities are present
    keyword_present = any(keyword in recognized_entities for keyword in keywords)
    return keyword_present

# Sentiment analysis
def analyze_sentiment(text):
    sentiment_scores = nlp_sia.polarity_scores(text)
    sentiment = 'positive' if sentiment_scores['compound'] > 0 else 'negative'
    return sentiment

# Process each news category content
def process_news_content():
    # Process data for each category
    for category, filename in category_files.items():   
        filtered_data = None
        category_data_df  = pd.read_csv(filename)
        # Apply the preprocessing and filter out unknwon records
        filtered_data = category_data_df[(category_data_df['title'] != 'Unknwon title') & 
                                (category_data_df['date']  != 'Date not found') &
                                (category_data_df['content'] != 'Content not found') &
                                (category_data_df['URL'] != 'Unknown URL') &
                                (category_data_df['category'] != 'Unknwon category')]

        filtered_data['preprocessed_content'] = filtered_data['content'].apply(preprocess_text)
        filtered_data['keyword_present'] = filtered_data['preprocessed_content'].apply(analyze_entities)
        filtered_data['sentiment'] = filtered_data['preprocessed_content'].apply(analyze_sentiment)

        # Count sentiment occurance
        sentiment_counts = filtered_data['sentiment'].value_counts().reset_index()
        sentiment_counts.columns = ['sentiment', 'sentiment_count']
        filtered_data = filtered_data.merge(sentiment_counts, on='sentiment', how='left')

        # Count keyword occurance
        keyword_counts = filtered_data['keyword_present'].value_counts().reset_index()
        keyword_counts.columns = ['keyword_present', 'keyword_count']
        filtered_data = filtered_data.merge(keyword_counts, on='keyword_present', how='left')

        #filtered_data.head()

        #Store processed Dataframe in the dictionary
        proccessed_df[category] = filtered_data        

    News_all_data = pd.concat(proccessed_df.values(), ignore_index=True)

    return News_all_data, proccessed_df

# Visualization of news data
def visaul_representation(df):    
# Bar chart for total positive/negative sentiment by category
    sentiment_chart = px.bar(df, x='category', color='sentiment',
    title='Total positive/Negative Sentiment by Category',
    labels={'category': 'News Category', 'sentiment': 'Sentiment'})
    

# Bar chart for total keyword presence by category
    keyword_chart = px.bar(df, x='category', color='keyword_present',
    title='Total Keyword Presence by Category',
    labels={'category': 'News Category', 'keyword_present': 'Keyword Present'},
    category_orders={'keyword_present': [True, False]})
    
# Create a table for total entity count by category
    entity_table = df.groupby('category')['keyword_present'].sum().reset_index    
    
# Display the dashboard
    sentiment_chart.show()
    keyword_chart.show()
    print(entity_table)


# Main  Function
def main():
    
   news_df, mews_dict = process_news_content()    
   visaul_representation(news_df)


if __name__ == "__main__":
    main()















**Media Representation Dashboard**

This experimental work aims to analyze and visualize news articles's from different 
news categories, representing women, youth, marginal groups from Province 2 and Province 5, 
evaluting sentiment and keyword representation using Python, Streamlit and data analysis libraries.


**Table of Contents**
* Installation
* NLTK 
* Spacy
* Usgae
* License


**Installation**
. Clone this repository to your local system:
   git clone https://github.com/dsdb/media-represenration-wym-npl.git

. Navigate to the project directory:
   cd media-represenration-wym-npl

. Install the required packages using pip:
   pip install -r requirement.txt

**NLTK**
  This project utilizes NLTK for text preprocessing. If you haven't already,
  need to download the NLTK data. You can do this by running the following command:
  python -m nltk.download.all


**Spacy**
  Spacy is used for named entity recognition and sentiment analysis. You'll need to install
  the English language model as follows:
  python -m spacy download en_core_web_sm



**Usage**
. To process the news data and generate visualization, runs the media_representation.py script:
   python media_representation.py

. This script will process the news data, generate sentiment and keyword representation visualizations,
   and display the results in your local browser.

. For interactive experience, you can also use the streamlit app to explore the visualizations:
   streamlit run app.py

. The Streamlit app will open in your web browser. Select a category from the dropdown to view sentiment and keywords
   representing charts

**License**
  This project is licensed under the **MIT License**



 

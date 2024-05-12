from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import re

def remove_urls(text):
    url_pattern = re.compile(r'https?://\S+|www\.\S+')
    return url_pattern.sub(r'', text)
def remove_html(text):
    html_pattern = re.compile('<.*?>')
    return html_pattern.sub(r'', text)
def get_sentiment(comments):
    d=[]
    pos,neg,neu=0,0,0
    for i in comments:
        if not i:continue
        tokens=word_tokenize(i.lower())
        filtered_tokens = [token for token in tokens if token not in stopwords.words('english')]
        processed_text=[token for token in filtered_tokens if token.isalpha()]
        lemmatizer = WordNetLemmatizer()
        lemmatized_tokens = [lemmatizer.lemmatize(token) for token in processed_text]
        processed_text = ' '.join(lemmatized_tokens)
        processed_text=remove_urls(processed_text)
        processed_text=remove_html(processed_text)
        processed_text = ' '.join(lemmatized_tokens)
        analyzer = SentimentIntensityAnalyzer()
        scores = analyzer.polarity_scores(processed_text)
       
        if scores['compound']>=0.05:
            pos+=1
        elif scores['compound']<0.05 and scores['compound']>=-0.05:
            neu+=1
        else:
            neg+=1
    return pos,neg,neu
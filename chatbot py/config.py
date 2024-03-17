import pandas as pd
import nltk
from nltk.corpus import stopwords, wordnet as wn
from nltk.stem import WordNetLemmatizer, PorterStemmer
from nltk.tokenize import word_tokenize
from spellchecker import SpellChecker
from sklearn.feature_extraction.text import TfidfVectorizer
import string

# Download necessary NLTK datasets
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')
nltk.download('vader_lexicon')

# Initialize necessary objects
stop_words = set(stopwords.words('english'))
spell = SpellChecker()
lemmatizer = WordNetLemmatizer()
stemmer = PorterStemmer()
tfidf_vectorizer = TfidfVectorizer()

intents_df = None   # DataFrame to store intents and keywords
tfidf_matrix = None # TF-IDF matrix for keyword analysis

def preprocess_text(text):
    text_no_punctuation = text.translate(str.maketrans('', '', string.punctuation))
    tokens = word_tokenize(text_no_punctuation.lower())
    corrected_tokens = [spell.correction(token) for token in tokens if token.isalpha()]
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in corrected_tokens]
    stemmed_tokens = [stemmer.stem(token) for token in lemmatized_tokens]
    return ' '.join(stemmed_tokens)

def preprocess_keywords(keywords):
    preprocessed = []
    for keyword in keywords.split(', '):
        preprocessed.append(preprocess_text(keyword))
    return ' '.join(set(preprocessed))

# Initialize the intents DataFrame and TF-IDF matrix. This will add depth to the keywords and allow for spelling, lemmatization, and stemming corrections
def initialize():
    global intents_df, tfidf_matrix
    intents_df = pd.read_csv('intent.csv')
    intents_df['processed_keywords'] = intents_df['keywords'].apply(preprocess_keywords)
    tfidf_matrix = tfidf_vectorizer.fit_transform(intents_df['processed_keywords'])


initialize()

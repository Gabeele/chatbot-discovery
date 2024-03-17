import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer, PorterStemmer
from nltk.tokenize import word_tokenize
from spellchecker import SpellChecker
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from config import spell, lemmatizer, stemmer, tfidf_vectorizer, intents_df, tfidf_matrix

# This class will be used to process user queries and determine their intent while holding nessessary information about the user
class Query:
    def __init__(self, text, user_id):
        self.text = text
        self.user_id = user_id
        self.intent = None
        self.processed_text = None

    def preprocess_text(self, text):
        text_no_punctuation = text.translate(str.maketrans('', '', string.punctuation))
        tokens = word_tokenize(text_no_punctuation.lower())
        corrected_tokens = [spell.correction(token) for token in tokens if token.isalpha()]
        lemmatized_tokens = [lemmatizer.lemmatize(token) for token in corrected_tokens]
        stemmed_tokens = [stemmer.stem(token) for token in lemmatized_tokens]
        self.processed_text = ' '.join(stemmed_tokens)
        return self.processed_text

    def determine_intent(self):
        processed_input = self.preprocess_text(self.text)
        user_input_vector = tfidf_vectorizer.transform([processed_input])
        cosine_similarities = cosine_similarity(user_input_vector, tfidf_matrix)
        max_similarity_index = cosine_similarities.argmax()
        self.intent = intents_df.iloc[max_similarity_index]['intent']
        return self.intent

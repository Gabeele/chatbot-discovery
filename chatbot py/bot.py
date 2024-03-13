
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.sentiment import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json

# Download necessary NLTK datasets
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')
nltk.download('vader_lexicon')


def initialize():
    
    # Initialize the stopwords
    stop_words = set(stopwords.words('english'))

    # Load the intents file
    intents_df = pd.read_csv('intent.csv')
    intents_df.head()



def preprocess_input(user_input):

    lemmatizer = WordNetLemmatizer()
    tokens = nltk.word_tokenize(user_input.lower())
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in tokens if token.isalpha() and token not in stop_words]
    return ' '.join(lemmatized_tokens)

def classify_response(response):

    sia = SentimentIntensityAnalyzer()
    score = sia.polarity_scores(response)
    return 'yes' if score['compound'] > 0 else 'no'

def request():
    maintenance_request = {}
    
    print("Entering maintenance request sequence...")
    emergency_response = input("Is this an emergency issue? (Fire, flooding, etc.) Yes/No: ").strip().lower()
    emergency = classify_response(emergency_response)
    if emergency == 'yes':
        print("Please call 911 or the emergency maintenance line immediately.")
        return
    maintenance_request["emergency"] = emergency
    
    maintenance_request["issue_description"] = input("What is the issue? Please explain in as much detail as possible: ").strip()
    
    issue_duration_response = input("How long has the issue been occurring? ").strip()
    # Assuming you want to keep this input as is, without classification
    maintenance_request["issue_duration"] = issue_duration_response
    
    first_time_reporting_response = input("Is this the first time reporting the issue? Yes/No: ").strip().lower()
    first_time_reporting = classify_response(first_time_reporting_response)
    maintenance_request["first_time_reporting"] = first_time_reporting
    
    self_fix_attempt_response = input("Have you attempted to fix the issue yourself? Yes/No: ").strip().lower()
    self_fix_attempt = classify_response(self_fix_attempt_response)
    maintenance_request["self_fix_attempt"] = self_fix_attempt
    
    severity_rating = input("What would you rate the severity of the issue? (1-10): ").strip()
    # Assuming this input is a direct numeric response
    maintenance_request["severity_rating"] = severity_rating
    
    urgency_rating = input("What would you rate the urgency of the issue? (1-10): ").strip()
    # Assuming this input is also a direct numeric response
    maintenance_request["urgency_rating"] = urgency_rating
    
    photo_attachment_response = input("Would you like to attach a photo? Yes/No: ").strip().lower()
    photo_attachment = classify_response(photo_attachment_response)
    if photo_attachment == 'yes':
        maintenance_request["photo_attached"] = "Simulated photo attachment"
    else:
        maintenance_request["photo_attached"] = "No photo attached"
    
    repair_schedule = input("What are dates and times best for you to have someone come and fix the issue? ").strip()
    # Assuming you want to keep this input as is, without classification
    maintenance_request["repair_schedule"] = repair_schedule
    
    prior_notice_required_response = input("Do you require prior notice before someone comes to fix the issue? Yes/No: ").strip().lower()
    prior_notice_required = classify_response(prior_notice_required_response)
    maintenance_request["prior_notice_required"] = prior_notice_required
    
    additional_details = input("Is there anything else you would like to add? ").strip()
    # Assuming you want to keep this input as is, without classification
    maintenance_request["additional_details"] = additional_details
    
    print("\nPlease review your maintenance request:")
    for key, value in maintenance_request.items():
        print(f"{key.replace('_', ' ').capitalize()}: {value}")
    
    correct_info_response = input("Is the above information correct? Yes/No: ").strip().lower()
    correct_info = classify_response(correct_info_response)
    if correct_info == 'yes':
        import json
        maintenance_request_json = json.dumps(maintenance_request, indent=4)
        print("Your maintenance request has been submitted. Thank you.")
        print(maintenance_request_json)
    else:
        print("Please start over and correct the necessary information.")

def generate_response(user_input):

    processed_input = preprocess_input(user_input)

    identified_intent = None
    for _, row in intents_df.iterrows():
        if row['keywords'].lower() in processed_input:
            identified_intent = row['intent']
            break
        
    print(identified_intent)

    if identified_intent == "maintenance":
        request()
        return "Thank you!"
    elif identified_intent == "greeting":
        return "Hello! How can I help you today?"
    elif identified_intent:
        return "Intent identified: " + identified_intent
    else:
        return "Sorry, I didn't understand that. Can you try rephrasing?"
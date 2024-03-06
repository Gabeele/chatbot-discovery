import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.sentiment import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json

def classify_response(response):
    """
    Classify the response as 'yes' or 'no' based on sentiment analysis.
    This is a simplistic approach and might need adjustments for better accuracy.
    """
    sia = SentimentIntensityAnalyzer()
    score = sia.polarity_scores(response)
    # Basic classification based on compound score; you might need to adjust the thresholds
    if score['compound'] > 0:
        return 'yes'
    else:
        return 'no'

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


# Download necessary NLTK datasets
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')
nltk.download('vader_lexicon')

# Initialize the stopwords
stop_words = set(stopwords.words('english'))

def preprocess_input(user_input):
    lemmatizer = WordNetLemmatizer()
    # Tokenize and lower case
    tokens = nltk.word_tokenize(user_input.lower())
    # Remove stopwords and punctuation, and lemmatize
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in tokens if token.isalpha() and token not in stop_words]
    return ' '.join(lemmatized_tokens)

def generate_response(user_input, corpus, tfidf_vectorizer, tfidf_matrix):
    user_input = preprocess_input(user_input)
    if not user_input:  # Check if user_input is empty after preprocessing
        return "I'm not sure how to respond to that."
    user_input_vector = tfidf_vectorizer.transform([user_input])
    similarities = cosine_similarity(user_input_vector, tfidf_matrix)
    max_similarity = similarities.max()
    if max_similarity < 0.1:  # Similarity threshold
        return "I'm not sure I understand. Could you rephrase?"
    max_similarity_index = similarities.argmax()
    return corpus[max_similarity_index]

corpus = [
    'Hello! How can I assist you today?',
    'I’m doing well, thank you! How can I assist you?',
    'My name is ChatBot, your virtual assistant. How can I help you?',
    'Why did the chicken cross the road? To get to the other side!',
    'Goodbye! Feel free to return if you have more questions.',
    'Currently, I can’t provide real-time weather updates. Please check a reliable weather service.',
    'For restaurant recommendations, I suggest checking out local review sites like Yelp or Google Reviews.',
    'You can contact customer support by emailing support@example.com or calling 1-800-123-4567.',
    'I’m not updated with the latest news, but checking a news website or app can provide you with the latest information.',
    'The meaning of life is a philosophical question concerning the significance of life or existence in general. It has been debated throughout history.',
    # New responses for expanded interactions
    'Okay, let me check that for you.',
    'What would you like me to check on?'
    'Could you specify a bit more?',
    'Is there anything else I can help you with?',
    'Glad I could help! Have a great day!',
    'I’m not sure I understand. Could you provide more details?',
    'That’s an interesting question. While I don’t have a personal opinion, many believe...',
]
corpus += [
    # Maintenance requests and responses
    'To report a maintenance issue, please provide me with the details of the problem.',
    'What type of maintenance issue are you experiencing? Plumbing, electrical, HVAC, or something else?',
    'Please describe the maintenance issue in as much detail as possible.',
    'Have you experienced this issue before, or is this the first time?',
    'Could you tell me the location of the issue within your apartment?',
    'For emergency maintenance requests, please call our 24/7 maintenance hotline at 1-800-555-1234 immediately.',
    'I have logged your maintenance request. Our maintenance team will contact you within 24 hours to schedule a repair.',
    'If you have any photos of the issue, please email them to maintenance@example.com with your apartment number in the subject line.',
    'Is there a preferred time for our maintenance team to visit your apartment for the repair?',
    'Thank you for reporting the maintenance issue. Your comfort and safety are our top priorities.',
    'If you have reported a maintenance issue, would you like a follow-up call to ensure everything is resolved to your satisfaction?',
    'Please provide your contact details so our maintenance team can reach out to you directly.',
    'If this is an update to an existing maintenance request, could you please provide the previous request number or details?',
    'Are there any additional details or specific requests you would like to add about the maintenance issue?',
    'Rest assured, all maintenance requests are treated with urgency. We appreciate your patience as we work to resolve your issue.',
    'For non-urgent maintenance requests, please note our team addresses these during regular business hours, Monday to Friday, 9 AM to 5 PM.',
    'Your maintenance request has been successfully submitted. Would you like assistance with anything else today?'
]

tfidf_vectorizer = TfidfVectorizer(ngram_range=(1, 2))
tfidf_matrix = tfidf_vectorizer.fit_transform(corpus)

print("Chatbot: Hello! How can I assist you?")

# Chatbot interaction loop
while True:
    user_input = input("User: ").strip()
    if user_input.lower() == 'goodbye':
        print("Chatbot: Goodbye!")
        break

    if "maintenance" in user_input.lower() or "repair" in user_input.lower():
        request()  
    else:
        response = generate_response(user_input, corpus, tfidf_vectorizer, tfidf_matrix)
        print("Chatbot:", response)


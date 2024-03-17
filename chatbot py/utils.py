from spellchecker import SpellChecker
from dateparser import parse as parse_date
import nltk
from nltk.tokenize import word_tokenize

affirmative_responses = ["yes", "y", "yeah", "yep", "yup", "sure", "ok", "okay", "yee", "aye", "correct", "affirmative", "Yes", "Y", "YEAH", "YEP", "YUP", "SURE", "OK", "OKAY", "YEE", "AYE", "CORRECT", "AFFIRMATIVE"]
negative_responses = ["no", "n", "nah", "nope", "nop", "nay", "negative", "noooo", "No", "N", "NO", "NOPE", "NAY", "NEGATIVE"]

spell = SpellChecker()

def correct_spelling(text):
    """
    Corrects the spelling of the input text.
    """
    corrected_text = " ".join(spell.correction(word) for word in text.split())
    return corrected_text

def normalize_yes_no(text):
    """
    Classifies text as 'yes', 'no', or None using a combination of predefined responses and NLTK features.
    """
    # Basic normalization and tokenization
    normalized_text = text.lower().strip()
    tokens = word_tokenize(normalized_text)
    
    if normalized_text in affirmative_responses:
        return "yes"
    elif normalized_text in negative_responses:
        return "no"
    
    for token in tokens:
        if token in affirmative_responses:
            return "yes"
        elif token in negative_responses:
            return "no"
    
    
    return None

def parse_scale(value, min_scale=1, max_scale=10):
    """
    Asks the user for a scale input within a specific range, repeating the question until a valid response is given.
    """
    if(value.isdigit() and min_scale <= int(value) <= max_scale):
        return value
    else:
        return None
    
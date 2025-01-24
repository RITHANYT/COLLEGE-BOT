"""import numpy as np
import random
from sklearn.metrics.pairwise import cosine_similarity
import train  # Ensure train.py is in the same directory for preprocess_text

# Load the trained model
model = np.load('model.npy', allow_pickle=True).item()

def find_response(user_input):
    
    preprocessed_input = train.preprocess_text(user_input)
    user_vector = model['vectorizer'].transform([preprocessed_input]).toarray()

    # Compute similarity with all patterns
    scores = [cosine_similarity(user_vector, [pattern])[0][0] for pattern in model['patterns']]

    # Find the best match
    max_score = max(scores)
    if max_score >= 0.7:  # Threshold for a good match
        best_match_index = scores.index(max_score)
        tag = model['tags'].inverse_transform([best_match_index])[0]
        return random.choice(model['responses'][tag])
    else:
        return "I'm sorry, I didn't understand that. Can you please rephrase?"

def process_text(user_input):
    return find_response(user_input)


"""
import json
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics.pairwise import cosine_similarity
import random
import requests
from bs4 import BeautifulSoup

def preprocess_text(text):
    """
    Preprocesses the text by removing non-alphanumeric characters and converting to lowercase.
    """
    return ''.join([char.lower() for char in text if char.isalnum() or char.isspace()])

# Load intents from the JSON file
with open('College-Chat-Bot-main - Copy/originalintents.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

tags = []
patterns = []
responses = {}

for intent in data['intents']:
    tags.append(intent['tag'])
    responses[intent['tag']] = intent['responses']
    for pattern in intent['patterns']:
        patterns.append(pattern)

# Preprocess patterns
preprocessed_patterns = [preprocess_text(p) for p in patterns]

# Convert text to feature vectors
vectorizer = CountVectorizer().fit(preprocessed_patterns)
X = vectorizer.transform(preprocessed_patterns).toarray()

# Encode tags
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(tags)

# Function to fetch information from the college website
def fetch_college_info():
    url = 'https://www.bitsathy.ac.in'
    
    try:
        response = requests.get(url)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Example: Extract the main header or any useful section. 
            # This needs to be customized based on actual structure of the website.
            
            # Trying to extract the main header information
            main_header = soup.find('h1')  # Look for an <h1> tag, change as needed
            
            if main_header:
                return f"Main Header: {main_header.get_text(strip=True)}"
            
            # You can extract other content based on the structure of the site
            # For example, finding a paragraph or div that contains general information
            general_info = soup.find('p')  # Example: Look for the first <p> tag
            if general_info:
                return general_info.get_text(strip=True)
            
            return "Couldn't find the specific information on the website."
        else:
            return "The college website is currently unavailable. Please try again later."
    
    except Exception as e:
        return f"An error occurred while fetching college information: {str(e)}"

# Function to find the best response
def find_response(user_input):
    """
    Finds the best response for the user's input using cosine similarity.
    """
    preprocessed_input = preprocess_text(user_input)
    user_vector = vectorizer.transform([preprocessed_input]).toarray()

    # Compute similarity with all patterns
    scores = [cosine_similarity(user_vector, [pattern])[0][0] for pattern in X]

    # Find the best match
    max_score = max(scores)
    if max_score >= 0.8:  # Threshold for a good match
        best_match_index = scores.index(max_score)
        tag = label_encoder.inverse_transform([best_match_index])[0]
        return random.choice(responses[tag])

    # Check for web scraping keywords
    elif any(keyword in user_input.lower() for keyword in ["college", "info", "website"]):
        return fetch_college_info()

    # Fallback response
    return "I'm sorry ,I'm unable to reach that.Can you say again?"

# Example usage
if __name__ == "__main__":
    print("Chatbot is ready! (Type 'quit' to exit)")
    while True:
        user_message = input("You: ")
        if user_message.lower() == "quit":
            print("Chatbot: Goodbye!")
            break
        response = find_response(user_message)
        print(f"Chatbot: {response}")

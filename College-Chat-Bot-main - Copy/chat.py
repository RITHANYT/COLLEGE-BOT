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
from sentence_transformers import SentenceTransformer, util

# Load intents
with open('originalintents.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Preprocess text
def preprocess_text(text):
    return ''.join([char.lower() for char in text if char.isalnum() or char.isspace()])

# Load Sentence Transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Fetch college info
def fetch_college_info():
    url = 'https://www.bitsathy.ac.in'
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            announcements = soup.select('.announcement-class')  # Replace with actual class
            if announcements:
                return "\n".join([a.get_text(strip=True) for a in announcements])
            return "No announcements found."
        return "The college website is currently unavailable."
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Find response
def find_response(user_input):
    user_embedding = model.encode([preprocess_text(user_input)])
    pattern_embeddings = model.encode(preprocessed_patterns)
    similarities = util.cos_sim(user_embedding, pattern_embeddings)
    best_match_index = similarities.argmax()
    if similarities[0][best_match_index] >= 0.8:
        tag = label_encoder.inverse_transform([best_match_index])[0]
        return random.choice(responses[tag])
    return fetch_college_info()

# Main loop
if __name__ == "__main__":
    print("Chatbot is ready! (Type 'quit' to exit)")
    while True:
        user_message = input("You: ")
        if user_message.lower() == "quit":
            print("Chatbot: Goodbye!")
            break
        response = find_response(user_message)
        print(f"Chatbot: {response}")
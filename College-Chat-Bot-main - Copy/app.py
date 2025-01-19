"""from flask import Flask, render_template, request, jsonify
import random
import json
import os

app = Flask(__name__)

# Load intents from JSON file
with open('College-Chat-Bot-main - Copy/originalintents.json', 'r',encoding='UTF-8') as file:
    intents = json.load(file)

# Function to process user input and generate a bot response
def respond_to_message(message):
    for intent in intents['intents']:
        if any(pattern.lower() in message.lower() for pattern in intent['patterns']):
            return random.choice(intent['responses'])
    return "Sorry, I didn't understand that."

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chatbot', methods=['POST'])
def chatbot():
    data = request.get_json()
    message = data.get('message')
    
    if not message:
        return jsonify({'error': 'No message received'}), 400
    
    # Process the message and get a response
    response = respond_to_message(message)
    return jsonify({'message': response})

if __name__ == '__main__':
    app.run(debug=True)
"""""
import train
from flask import Flask, render_template, request, jsonify
import random
import json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import spacy
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

# Load spaCy model for embeddings
nlp = spacy.load("en_core_web_sm")

# Load the trained model
model = np.load('model.npy', allow_pickle=True).item()

# Function to preprocess text
def preprocess_text(text):
    return ''.join([char.lower() for char in text if char.isalnum() or char.isspace()])

# Get response based on similarity
def respond_to_message(message):
    preprocessed_input = train.preprocess_text(message)
    user_vector = model['vectorizer'].transform([preprocessed_input]).toarray()

    # Compute similarity with all patterns (use 'patterns' instead of 'embeddings')
    scores = [cosine_similarity(user_vector, [pattern])[0][0] for pattern in model['patterns']]

    # Find the best match
    max_score = max(scores)
    if max_score >= 0.7:  # Adjust the threshold for matching
        best_match_index = scores.index(max_score)
        tag = model['tags'].inverse_transform([best_match_index])[0]
        return random.choice(model['responses'][tag])
    else:
        return "I'm sorry, I didn't understand that. Can you please rephrase?"

# Scrape college events dynamically
def scrape_college_events():
    url = "https://www.bitsathy.ac.in"  # Replace with the correct URL
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        events = []
        for event in soup.select('.event-class'):  # Update CSS selector
            title = event.find('h3').text.strip()
            date = event.find('span', class_='date-class').text.strip()
            events.append(f"{title} on {date}")
        return "\n".join(events) if events else "No upcoming events found."
    else:
        return "Unable to fetch events at the moment. Please try again later."

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chatbot', methods=['POST'])
def chatbot():
    data = request.get_json()
    message = data.get('message')

    if not message:
        return jsonify({'error': 'No message received'}), 400

    # Handle dynamic queries
    if "event" in message.lower():
        response = scrape_college_events()
    else:
        # Get response from static model
        response = respond_to_message(message)

    return jsonify({'message': response})

if __name__ == '__main__':
    app.run(debug=True)

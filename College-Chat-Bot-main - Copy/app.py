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



"""
from flask import Flask, render_template, request, jsonify
import random
import json
import os
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Load intents from JSON file
with open('College-Chat-Bot-main - Copy/originalintents.json', 'r',encoding='UTF-8') as file:
    intents = json.load(file)

# Function to fetch information from the college website
def fetch_college_info():
    url = 'https://www.bitsathy.ac.in'

    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Example: Adjust this based on the website's actual structure.
            header = soup.find('h1')  # Replace 'h1' with the actual tag or class
            if header:
                return header.get_text(strip=True)

            # Alternative: Extract paragraphs or specific content.
            general_info = soup.find('p')  # Replace with appropriate tag/class.
            if general_info:
                return general_info.get_text(strip=True)
            
            # Fallback if no content is found.
            return "Couldn't find specific information on the website. Please check the website structure."
        else:
            return "The college website is currently unavailable. Please try again later."
    except Exception as e:
        return f"An error occurred while fetching college information: {str(e)}"

# Function to process user input and generate a bot response
def respond_to_message(message):
    for intent in intents['intents']:
        if any(pattern.lower() in message.lower() for pattern in intent['patterns']):
            return random.choice(intent['responses'])
    # If no intent matches, fetch dynamic information
    return fetch_college_info()

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

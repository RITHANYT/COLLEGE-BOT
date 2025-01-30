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

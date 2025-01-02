# College-Chat-Bot
My team and I have created an exciting mini project using NLP (Natural Language Processing) and web scraping techniques to gather information about our college, Sona. This project aims to make the information about our college more appealing and accessible.
# NLP Chatbot with Web Scraping
This project implements a chatbot using Natural Language Processing (NLP) techniques and web scraping. The chatbot is designed to provide responses based on pre-defined patterns and can fetch information from the web using web scraping. The code is written in Python and Flask framework is used for creating a web interface.
# Dependencies Installation
1.Clone the repository:
git clone https://github.com/DHANUSHGCse/College-Chat-Bot/
2.Install the required Python packages:
pip install -r requirements.txt
# Usage
1.Run the Flask application:
python app.py
2.Access the chatbot interface in your web browser:
http://localhost:5000
3.Start interacting with the chatbot by entering messages in the input field.
# Understanding the Code
app.py: This file contains the Flask application code that handles the HTTP requests and renders the chatbot interface.
chat.py: This module processes the user's input, utilizes the NLP model, and returns a response based on predefined patterns and web scraping.
train.py: This module is responsible for training the NLP model using intents defined in the intents.json file.
intents.json: This file contains the predefined intents, patterns, and responses used for training the NLP model.
model.npy: This file stores the trained NLP model for generating responses.
index.html: This HTML template file defines the structure and layout of the chatbot interface.
# Contributing
Feel free to contribute to this project by submitting bug reports, feature requests, or pull requests. We welcome and appreciate any improvements or enhancements you can bring to the codebase.

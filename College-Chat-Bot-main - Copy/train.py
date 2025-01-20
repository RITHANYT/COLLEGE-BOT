"""import json
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics.pairwise import cosine_similarity

def preprocess_text(text):
   
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

# Save the model
model = {
    'vectorizer': vectorizer,
    'patterns': X,
    'tags': label_encoder,
    'responses': responses
}

np.save('model.npy', model)
print("Model training complete. Saved to model.npy.")



"""
import json
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import LabelEncoder

def preprocess_text(text):
    return ''.join([char.lower() for char in text if char.isalnum() or char.isspace()])

# Load intents from the JSON file
with open('originalintents.json', 'r', encoding='utf-8') as file:
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

# Save the model
model = {
    'vectorizer': vectorizer,
    'patterns': X,
    'tags': label_encoder,
    'responses': responses
}

np.save('model.npy', model)
print("Model training complete. Saved to model.npy.")

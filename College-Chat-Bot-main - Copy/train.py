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
import spacy
import json
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import LabelEncoder

# Load spaCy model for text embeddings
nlp = spacy.load("en_core_web_sm")

def preprocess_text(text):
    """
    Preprocesses text by removing special characters and converting to lowercase.
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

vectorizer = CountVectorizer().fit(preprocessed_patterns)
X = vectorizer.transform(preprocessed_patterns).toarray()

# Convert text to embeddings using spaCy
def get_embeddings(texts):
    embeddings = []
    for text in texts:
        doc = nlp(text)
        # Ensure the vector is of the correct shape (300 dimensions for en_core_web_sm)
        if doc.vector is not None and doc.vector.size == 300:  # Check for valid vector size
            embeddings.append(doc.vector)
        else:
            # If no valid vector is found, append a zero vector (300 dimensions)
            embeddings.append(np.zeros(300))  # Or handle this differently if needed
    return np.array(embeddings)

# Replace the previous X with embeddings
X = get_embeddings(preprocessed_patterns)

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

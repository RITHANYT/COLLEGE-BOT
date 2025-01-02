import numpy as np
import random
from sklearn.metrics.pairwise import cosine_similarity
import train  # Ensure train.py is in the same directory for preprocess_text

# Load the trained model
model = np.load('model.npy', allow_pickle=True).item()

def find_response(user_input):
    """
    Finds the best response for the user's input based on cosine similarity.
    """
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

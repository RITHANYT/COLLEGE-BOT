import numpy as np

# Load the file
model = np.load('bert_model.npy', allow_pickle=True).item()

# Print available keys in the model
print(model.keys())  # This will show what keys are stored in the file

import numpy as np

def decode_predictions(predictions):
  return np.argmax(predictions, axis=1)

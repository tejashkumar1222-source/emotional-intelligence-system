import numpy as np
from scipy.stats import entropy

def compute_uncertainty(probs):
    confidence = np.max(probs, axis=1)
    ent = entropy(probs.T)

    uncertain_flag = ((confidence < 0.55) | (ent > 1.2)).astype(int)

    return confidence, uncertain_flag
import torch
import numpy as np
from transformers import DistilBertTokenizer, DistilBertModel

tokenizer = DistilBertTokenizer.from_pretrained('./local_model')
model = DistilBertModel.from_pretrained('./local_model')

def get_embeddings(texts):
    embs = []
    for t in texts:
        inputs = tokenizer(t, return_tensors="pt", truncation=True, padding=True)
        with torch.no_grad():
            outputs = model(**inputs)
        embs.append(outputs.last_hidden_state.mean(dim=1).squeeze().numpy())
    return np.array(embs)
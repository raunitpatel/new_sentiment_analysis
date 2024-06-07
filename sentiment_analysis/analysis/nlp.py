import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax
import numpy as np

def get_sentiment(df):
    pd.set_option('display.max_columns', None)
    MODEL = "cardiffnlp/twitter-roberta-base-sentiment"
    tokenizer = AutoTokenizer.from_pretrained(MODEL)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL)
    classes = ['negative', 'neutral', 'positive']
    
    # print(df.shape)
    
    pos_scores = []
    neg_scores = []
    neutral_scores = []
    labels = []

    for text in df['clean_text']: 
        # Tokenize text
        inputs = tokenizer(text, return_tensors="pt")

        # Forward pass through model
        outputs = model(**inputs)
        logits = outputs.logits

        # Softmax to get probabilities
        probs = softmax(logits.detach().numpy(), axis=1)[0]

        # Round scores to three decimal places using numpy
        neg_score = np.round(probs[0], 3)
        neutral_score = np.round(probs[1], 3)
        pos_score = np.round(probs[2], 3)
        
        # Append scores to lists
        neg_scores.append(neg_score)
        neutral_scores.append(neutral_score)
        pos_scores.append(pos_score)

        # Determine label based on maximum probability
        label = classes[probs.argmax()]
        labels.append(label)

    # Add new columns to DataFrame
    df['pos_score'] = pos_scores
    df['neg_score'] = neg_scores
    df['neutral_score'] = neutral_scores
    df['label'] = labels
    # print(df.head())

    return df




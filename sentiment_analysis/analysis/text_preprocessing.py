import re

def clean_text(df):
    
    df = df.dropna()
    df['clean_text'] = df['description'].apply(lambda x: re.sub(r'http\S+', '', x))
    df['clean_text'] = df['clean_text'].apply(lambda x: x.encode('ascii', 'ignore').decode('ascii'))
    df['clean_text'] = df['description'].apply(lambda x: re.sub(r'[^a-zA-Z\s]', '', x))
    df['clean_text'] = df['clean_text'].apply(lambda x: x.lower())
    df = df[df['clean_text'].str.strip() != '']

    
    return df

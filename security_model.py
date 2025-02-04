import pandas as pd
from sklearn.metrics import classification_report
import re


def extract_features(url):
    features = {}
    
    # Length of URL
    features['url_length'] = len(url)
    
    # Count of special characters
    features['special_chars'] = len(re.findall(r'[^a-zA-Z0-9]', url))
    
    # Count of digits
    features['digits'] = len(re.findall(r'\d', url))
    
    # Presence of suspicious words
    suspicious_words = ['login', 'bank', 'account', 'secure', 'update']
    features['suspicious_words'] = sum(word in url.lower() for word in suspicious_words)
    
    return features

# Load data
print("Loading data...")
df = pd.read_csv('malicious_phish.csv')

# Extract features
print("Extracting features...")
features_list = []
for url in df['url']:
    features_list.append(extract_features(url))



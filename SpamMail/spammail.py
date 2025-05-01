#spammail.py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score
import pickle

# Read file
df = pd.read_csv('emails_dataset.csv')

# Combine subject and body columns
df['text'] = df['subject'] + df['body']

# Target variable
X = df['text']
y = df['label']

# Vectorize with TF-IDF
# Seperate train and test datas
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

# Train the model
model = LogisticRegression()
model.fit(X_train_tfidf, y_train)
# Predict
y_pred = model.predict(X_test_tfidf)
# Performance
print(f'Accuracy: {classification_report(y_test, y_pred)}')
print(classification_report(y_test, y_pred))

# Save the model and vectorizer
with open('spam_model.pkl', 'wb') as model_file:
    pickle.dump(model, model_file)
with open('tfidf_vectorizer.pkl', 'wb') as vec_file:
    pickle.dump(vectorizer, vec_file)


from flask import Flask, render_template, request, redirect, url_for, flash
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import os
import numpy as np

app = Flask(__name__)
app.secret_key = '123989'  # Set a secret key for session management

# Initialize global variables for the model and vectorizer
clf = None
cv = None

def load_and_train_model():
    global clf, cv
    try:
        # Load data from CSV
        df = pd.read_csv("spam.csv", encoding="latin-1")
        df.drop(['Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4'], axis=1, inplace=True)
        
        # Handle NaN values
        df = df.dropna(subset=['message', 'class'])  # Drop rows where message or class is NaN

        # Features and Labels
        df['label'] = df['class'].map({'ham': 0, 'spam': 1})
        X = df['message']
        y = df['label']

        if X.empty or y.empty:
            raise ValueError("The training data is empty after cleaning.")

        # Extract Features with CountVectorizer
        cv = CountVectorizer()
        X = cv.fit_transform(X)  # Fit the Data

        # Naive Bayes Classifier
        clf = MultinomialNB()
        clf.fit(X, y)  # Train with all data
        print(f"Model trained with {len(df)} entries.")
    except Exception as e:
        print(f"Error loading or training model: {e}")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    global clf, cv
    if clf is None or cv is None:  # Load and train model if not loaded
        load_and_train_model()

    if request.method == 'POST':
        message = request.form['message']
        if message:
            data = [message]
            vect = cv.transform(data).toarray()
            my_prediction = clf.predict(vect)
            prediction_text = '1' if my_prediction[0] == 1 else '0'
            print(f"Prediction for '{message}': {prediction_text}")
            return render_template('index.html', prediction=my_prediction , mess=data)
        else:
            flash('Please enter a message to classify.', 'error')
            return redirect(url_for('home'))

@app.route('/add_data', methods=['GET', 'POST'])
def add_data():
    if request.method == 'POST':
        message = request.form['message']
        label = request.form['label']
        new_data = {'class': label, 'message': message}

        # Append the new data to the CSV file
        df = pd.DataFrame([new_data])
        df.to_csv("spam.csv", mode='a', header=not os.path.isfile("spam.csv"), index=False)

        # Retrain the model with the new data
        load_and_train_model()
        
        flash('New data added successfully and model retrained.', 'success')
        return redirect(url_for('home'))
    
    return render_template('add_data.html')

if __name__ == '__main__':
    app.run(debug=True)

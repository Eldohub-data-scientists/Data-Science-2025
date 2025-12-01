from flask import Flask, render_template, request

import joblib
from lime.lime_text import LimeTextExplainer
import numpy as np

# Initialize Flask app
app = Flask(__name__)

# Load trained model and vectorizer
model = joblib.load('fake_news_model.pkl')
vectorizer = joblib.load('vectorizer.pkl')

# Define class names
explainer = LimeTextExplainer(class_names=['FAKE', 'REAL'])


@app.route('/')
def home():
    return render_template('index.html', title="Fake News Detector")


@app.route('/about')
def about():
    return render_template('about.html', title="About Project", developer="Batch Hacket")


@app.route('/model')
def model_info():
    return render_template('model.html', title="Model Information")


@app.route('/predict', methods=['POST'])
def predict():
    # Get user input text
    text = request.form['text']
    if text=='':
        return render_template('error_notxt.html', title="About Project", developer="Batch Hacket")


    # Transform text into vector form
    vect = vectorizer.transform([text])

    # Make prediction
    prediction = model.predict(vect)[0]

    # Compute confidence safely
    if hasattr(model, "decision_function"):
        decision = model.decision_function(vect)
        confidence = float(abs(decision[0])) * 10
        confidence = round(min(confidence, 100), 2)
    elif hasattr(model, "predict_proba"):
        confidence = model.predict_proba(vect).max() * 100
        confidence = round(confidence, 2)
    else:
        confidence = 70.0  # fallback default

    # FIX: Wrap prediction for LIME
    def predict_proba_wrapped(texts):
        vectors = vectorizer.transform(texts)
        if hasattr(model, "predict_proba"):
            return model.predict_proba(vectors)
        else:
            # Convert decision_function outputs into pseudo-probabilities
            decision = model.decision_function(vectors)
            probs = 1 / (1 + np.exp(-decision))
            # Stack into 2D array [P(FAKE), P(REAL)]
            return np.vstack([1 - probs, probs]).T

    # Generate explanation
    explanation = explainer.explain_instance(
        text,
        predict_proba_wrapped,
        num_features=8
    )
    html_explanation = explanation.as_html()

    # Render result page
    return render_template(
        'result.html',
        prediction=prediction,
        confidence=confidence,
        text=text,
        explanation=html_explanation
    )


if __name__ == '__main__':
    app.run(debug=True)

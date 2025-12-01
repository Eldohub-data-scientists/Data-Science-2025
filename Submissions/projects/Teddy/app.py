# app.py
from flask import Flask, render_template, request, send_file
import joblib
import numpy as np
from lime.lime_text import LimeTextExplainer
from database import Prediction, init_db
from datetime import datetime, timezone  # ← FIXED: Use timezone
import logging
import json
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import load_model
import os

import io
import base64
from collections import Counter
import re

# === FIX 1: FORCE NON-GUI BACKEND ===
import matplotlib
matplotlib.use('Agg')  # ← MUST BE BEFORE plt/seaborn!
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# === LOGGING: Reduce noise ===
logging.basicConfig(level=logging.INFO)
logging.getLogger('PIL').setLevel(logging.WARNING)  # Hide PIL debug

app = Flask(__name__)
session = init_db()

# === LOAD MODELS ===
tfidf_model = joblib.load('fake_news_model.pkl')
vectorizer = joblib.load('vectorizer.pkl')

lstm_model = load_model('lstm_model.h5')
with open('lstm_tokenizer.json') as f:
    tokenizer_data = json.load(f)
tokenizer = tf.keras.preprocessing.text.tokenizer_from_json(tokenizer_data)
max_len = 200

explainer = LimeTextExplainer(class_names=['FAKE', 'REAL'])


# SAFETY FILTER FOR SENSITIVE CONTENT
# -----------------------------
def is_sensitive(text):
    text_lower = text.lower()
    words = text.split()

    # 1. Too short (claims are usually short)
    if len(words) < 10:
        return True

    # 2. Explicit claim/relationship keywords
        claim_keywords = [
            " is ", " was ", " alias ", " alias of ", " also known as ",
            " real name ", " son of ", " daughter of ", " relative of ",
            " is the same as ", " same person as "
        ]
        if any(pattern in text_lower for pattern in claim_keywords):
            return True

        # 3. Detection of two یا more capitalized words (names)
        capitalized = [w for w in words if w[:1].isupper()]
        if len(capitalized) >= 2:
            return True

        # 4. Political or sensitive public keywords
        sensitive_terms = [
            "president", "minister", "government", "politician", "mp", "governor",
            "senator", "campaign", "party", "election"
        ]
        if any(term in text_lower for term in sensitive_terms):
            return True

    return False


# === ROUTES ===
@app.route('/')
def home():
    return render_template('index.html', title="Fake News Detector")

@app.route('/about')
def about():

    total_preds = session.query(Prediction).count()
    fake_preds  = session.query(Prediction).filter_by(label='FAKE').count()
    real_preds  = session.query(Prediction).filter_by(label='REAL').count()
    classic_cnt = session.query(Prediction).filter_by(model='CLASSIC').count()
    lstm_cnt    = session.query(Prediction).filter_by(model='LSTM').count()

    stats = {
        "total": total_preds,
        "fake": fake_preds,
        "real": real_preds,
        "classic": classic_cnt,
        "lstm": lstm_cnt,
    }

    return render_template(
        'about.html',
        title="About Us",
        developer="Batch Hacket",
        stats=stats,
        year=datetime.now(timezone.utc).year)

@app.route('/model')
def model_info():
    # Optional live model usage stats
    classic_cnt = session.query(Prediction).filter_by(model='CLASSIC').count()
    lstm_cnt    = session.query(Prediction).filter_by(model='LSTM').count()
    total_preds = classic_cnt + lstm_cnt

    model_stats = {
        "classic": classic_cnt,
        "lstm": lstm_cnt,
        "total": total_preds,
        "classic_pct": round(classic_cnt / total_preds * 100, 1) if total_preds else 0,
        "lstm_pct": round(lstm_cnt / total_preds * 100, 1) if total_preds else 0,
    }

    return render_template(
        'model.html',
        title="Model Info",
        model_stats=model_stats,
        year=datetime.now(timezone.utc).year
    )

@app.route('/predict', methods=['POST'])


def predict():
    text = request.form['text'].strip()
    model_type = request.form.get('model_type', 'classic')

    if not text:
        return render_template('error_notxt.html')
    
    # if is_sensitive(text):
    #     return render_template("warning.html", text=text)

    prediction = confidence = explanation_html = None

    if model_type == 'classic':
        vect = vectorizer.transform([text])
        raw_pred = tfidf_model.predict(vect)[0]
        prediction = 'FAKE' if str(raw_pred) == '0' else 'REAL'

        if hasattr(tfidf_model, "predict_proba"):
            proba = tfidf_model.predict_proba(vect)[0]
            confidence = round(proba[0] * 100, 2) if prediction == 'FAKE' else round(proba[1] * 100, 2)
        else:
            decision = tfidf_model.decision_function(vect)[0]
            prob = 1 / (1 + np.exp(-decision))
            confidence = round((1 - prob) * 100, 2) if prediction == 'FAKE' else round(prob * 100, 2)

        def wrapped(texts):
            vecs = vectorizer.transform(texts)
            if hasattr(tfidf_model, "predict_proba"):
                return tfidf_model.predict_proba(vecs)
            d = tfidf_model.decision_function(vecs)
            p = 1 / (1 + np.exp(-d))
            return np.hstack([1 - p, p])
        exp = explainer.explain_instance(text, wrapped, num_features=8)
        explanation_html = exp.as_html()

    else:
        seq = tokenizer.texts_to_sequences([text])
        padded = pad_sequences(seq, maxlen=max_len)
        prob = lstm_model.predict(padded, verbose=0)[0][0]
        prediction = 'FAKE' if prob < 0.5 else 'REAL'
        confidence = round((1 - prob) * 100, 2) if prediction == 'FAKE' else round(prob * 100, 2)

        def wrapped_lstm(texts):
            seqs = tokenizer.texts_to_sequences(texts)
            padded = pad_sequences(seqs, maxlen=max_len)
            preds = lstm_model.predict(padded, verbose=0)
            return np.hstack([1 - preds, preds])
        exp = explainer.explain_instance(text, wrapped_lstm, num_features=8)
        explanation_html = exp.as_html()

    record = Prediction(text=text, label=prediction, confidence=confidence, model=model_type.upper())
    session.add(record)
    session.commit()

    return render_template(
        'result.html',
        prediction=prediction,
        confidence=confidence,
        text=text,
        explanation=explanation_html,
        model_type=model_type.title()
    )


@app.route('/history')
def history():
    records = session.query(Prediction).order_by(Prediction.id.desc()).limit(50).all()
    for r in records:
        if r.timestamp.tzinfo is None:  # naive
            r.timestamp = r.timestamp.replace(tzinfo=timezone.utc)
            
    return render_template('history.html',
                           records=records,
                           title="History",
                           now=datetime.now(timezone.utc))  # ← FIXED: No deprecation

@app.route('/analysis')
def analysis():
    records = session.query(Prediction).order_by(Prediction.timestamp).all()
    if not records:
        return render_template('analysis.html', no_data=True, title="Analytics")

    df = pd.DataFrame([{
        'text': r.text,
        'label': r.label,
        'confidence': r.confidence,
        'model': r.model,
        'time': r.timestamp
    } for r in records])

    df['date'] = df['time'].dt.date
    df['is_fake'] = df['label'] == 'FAKE'

    # === 1. Predictions Over Time ===
    daily = df.groupby('date').size().reset_index(name='count')
    fig1 = px.line(daily, x='date', y='count', title='Predictions Over Time',
                   template='plotly_white')
    fig1.update_traces(line=dict(color='#3498db', width=3))
    fig1.update_layout(height=320, margin=dict(l=40, r=40, t=40, b=40))
    plot1 = fig1.to_html(include_plotlyjs='cdn', div_id="plot1")  # ← JS only here

    # === 2. REAL vs FAKE Pie ===
    plt.figure(figsize=(6,6))
    counts = df['label'].value_counts()
    if len(counts) == 0:
        plt.text(0.5, 0.5, 'No Data', ha='center', va='center', fontsize=16)
    else:
        plt.pie(counts, labels=counts.index, autopct='%1.1f%%',
                colors=['#27ae60', '#e74c3c'], startangle=90)
        plt.title('REAL vs FAKE Distribution', fontsize=14, pad=20)
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=150, bbox_inches='tight', facecolor='white')
    buf.seek(0)
    pie_img = base64.b64encode(buf.read()).decode()
    plt.close()

    # === 3. Confidence by Model (FIXED: hue + legend) ===
    plt.figure(figsize=(8,5))
    models_present = df['model'].unique()
    if len(models_present) == 0 or len(df) < 2:
        plt.text(0.5, 0.5, 'Insufficient Data', ha='center', va='center', fontsize=16)
        plt.title('Confidence Distribution by Model')
    else:
        df_filtered = df[df['model'].isin(models_present)]
        palette = ['#9b59b6' if m == 'CLASSIC' else '#e67e22' for m in models_present]
        sns.violinplot(data=df_filtered, x='model', y='confidence',
                       hue='model', palette=palette, inner='quartile', legend=False)  # ← FIXED
        plt.title('Confidence Distribution by Model')
        plt.ylabel('Confidence (%)')
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=150, bbox_inches='tight', facecolor='white')
    buf.seek(0)
    violin_img = base64.b64encode(buf.read()).decode()
    plt.close()

    # === 4. Model Usage Over Time ===
    model_time = df.groupby(['date', 'model']).size().unstack(fill_value=0).reset_index()
    for col in ['CLASSIC', 'LSTM']:
        if col not in model_time.columns:
            model_time[col] = 0
    model_time = model_time.melt(id_vars='date', var_name='model', value_name='count')
    model_time = model_time[model_time['count'] > 0]

    if not model_time.empty:
        fig2 = px.bar(model_time, x='date', y='count', color='model',
                      color_discrete_map={'CLASSIC': '#9b59b6', 'LSTM': '#e67e22'},
                      barmode='stack', title='Model Usage Over Time')
    else:
        fig2 = go.Figure().add_annotation(text="No Model Data Yet", xref="paper", yref="paper",
                                          x=0.5, y=0.5, showarrow=False)
        fig2.update_layout(title="Model Usage Over Time")
    fig2.update_layout(height=320, margin=dict(l=40, r=40, t=40, b=40))
    plot2 = fig2.to_html(include_plotlyjs=False, div_id="plot2")

    # === 5. Top Words in FAKE News ===
    fake_df = df[df['is_fake']]
    if len(fake_df) == 0:
        fig3 = go.Figure().add_annotation(text="No FAKE Predictions Yet", xref="paper", yref="paper",
                                          x=0.5, y=0.5, showarrow=False)
        fig3.update_layout(title="Top Words in FAKE News")
    else:
        words = re.findall(r'\b[a-z]{4,}\b', ' '.join(fake_df['text']).lower())
        word_df = pd.DataFrame(Counter(words).most_common(40), columns=['word', 'freq'])
        fig3 = px.treemap(word_df, path=['word'], values='freq',
                          color='freq', color_continuous_scale='Reds',
                          title='Top Words in FAKE News')
    fig3.update_layout(height=400, margin=dict(l=20, r=20, t=40, b=20))
    plot3 = fig3.to_html(include_plotlyjs=False, div_id="plot3")

    # === 6. Accuracy Trend ===
    df['high_conf'] = df['confidence'] > 80
    acc_daily = df.groupby('date')['high_conf'].mean().reset_index()
    acc_daily['accuracy'] = acc_daily['high_conf'] * 100
    if acc_daily.empty:
        fig4 = go.Figure().add_annotation(text="No Data Yet", xref="paper", yref="paper",
                                          x=0.5, y=0.5, showarrow=False)
        fig4.update_layout(title="Model Accuracy Trend")
    else:
        fig4 = px.line(acc_daily, x='date', y='accuracy',
                       title='Model Accuracy Trend (>80% Confidence)',
                       markers=True, template='plotly_white')
        fig4.add_hline(y=95, line_dash="dash", line_color="green", annotation_text="95% Target")
    fig4.update_layout(height=400, margin=dict(l=40, r=40, t=40, b=40))
    plot4 = fig4.to_html(include_plotlyjs=False, div_id="plot4")

    return render_template('analysis.html',
                           plot1=plot1, plot2=plot2, plot3=plot3, plot4=plot4,
                           pie_img=pie_img, violin_img=violin_img,
                           no_data=False, title="Advanced Analytics")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
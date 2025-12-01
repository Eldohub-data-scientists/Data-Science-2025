# train_lstm.py
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping
import json
import os

# ================================
# 1. Load & Combine Datasets (Same as train_model.py)
# ================================
print("Loading datasets...")
fake = pd.read_csv('fake.csv')
true = pd.read_csv('true.csv')

fake['label'] = 0  # FAKE
true['label'] = 1  # REAL

data = pd.concat([fake, true], axis=0).sample(frac=1, random_state=42).reset_index(drop=True)
print(f"Total samples: {len(data)}")

# ================================
# 2. Prepare text & labels
# ================================
texts = data['text'].astype(str).values
labels = data['label'].values

# ================================
# 3. Split (Same as train_model.py)
# ================================
X_train, X_test, y_train, y_test = train_test_split(
    texts, labels, test_size=0.2, random_state=42, stratify=labels
)
print(f"Train: {len(X_train)}, Test: {len(X_test)}")

# ================================
# 4. Tokenization
# ================================
MAX_WORDS = 20000
MAX_LEN = 300  # You can adjust based on your text length

print("Tokenizing...")
tokenizer = Tokenizer(num_words=MAX_WORDS, oov_token="<OOV>")
tokenizer.fit_on_texts(X_train)

X_train_seq = tokenizer.texts_to_sequences(X_train)
X_test_seq = tokenizer.texts_to_sequences(X_test)

X_train_pad = pad_sequences(X_train_seq, maxlen=MAX_LEN)
X_test_pad = pad_sequences(X_test_seq, maxlen=MAX_LEN)

# ================================
# 5. Build LSTM Model
# ================================
print("Building LSTM model...")
model = Sequential([
    Embedding(MAX_WORDS, 128, input_length=MAX_LEN),
    LSTM(64, dropout=0.5, recurrent_dropout=0.5, return_sequences=False),
    Dense(32, activation='relu'),
    Dropout(0.5),
    Dense(1, activation='sigmoid')
])

model.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=['accuracy']
)

# ================================
# 6. Train with Early Stopping
# ================================
early_stop = EarlyStopping(monitor='val_loss', patience=2, restore_best_weights=True)

print("Training LSTM...")
history = model.fit(
    X_train_pad, y_train,
    validation_data=(X_test_pad, y_test),
    epochs=10,
    batch_size=64,
    callbacks=[early_stop],
    verbose=1
)

# ================================
# 7. Evaluate
# ================================
from sklearn.metrics import classification_report

test_pred_proba = model.predict(X_test_pad, verbose=0)
test_pred = (test_pred_proba > 0.5).astype(int).flatten()

print("\n=== LSTM Classification Report ===")
print(classification_report(y_test, test_pred, target_names=['FAKE', 'REAL']))

# ================================
# 8. Save Model + Tokenizer
# ================================
print("Saving LSTM model and tokenizer...")
model.save('lstm_model.h5')

# Save tokenizer config
tokenizer_config = tokenizer.to_json()
with open('lstm_tokenizer.json', 'w', encoding='utf-8') as f:
    json.dump(tokenizer_config, f)

print("LSTM model and tokenizer saved successfully!")
print("Files created:")
print("   - lstm_model.h5")
print("   - lstm_tokenizer.json")
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import classification_report
import joblib

# 1️⃣ Load your datasets
fake = pd.read_csv('fake.csv')
true = pd.read_csv('true.csv')

# 2️⃣ Combine them into one dataset
fake['label'] = 0  # 0 = FAKE
true['label'] = 1  # 1 = REAL
data = pd.concat([fake, true], axis=0).sample(frac=1).reset_index(drop=True)

# 3️⃣ Prepare text and labels
X = data['text']
y = data['label']

# 4️⃣ Split the dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 5️⃣ Vectorize text
vectorizer = TfidfVectorizer(stop_words='english', max_df=0.7)
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# 6️⃣ Train a Logistic Regression model with calibration
base_model = LogisticRegression(max_iter=200)
model = CalibratedClassifierCV(base_model, cv=5)  # <-- Calibration step
model.fit(X_train_vec, y_train)

# 7️⃣ Evaluate
preds = model.predict(X_test_vec)
print(classification_report(y_test, preds))

# 8️⃣ Save the model and vectorizer
joblib.dump(model, 'fake_news_model.pkl')
joblib.dump(vectorizer, 'vectorizer.pkl')

print(" Model and vectorizer saved successfully!")

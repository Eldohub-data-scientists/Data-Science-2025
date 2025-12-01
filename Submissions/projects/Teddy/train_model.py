import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import classification_report
import joblib
import os

# ==========================================
# 1. Load fake.csv → label = 0 (FAKE)
# ==========================================
print("Loading fake.csv ...")
fake = pd.read_csv("fake.csv", usecols=["title", "text"])
fake["text"] = fake["title"].fillna("") + " " + fake["text"].fillna("")
fake = fake[["text"]]
fake["label"] = 0
fake = fake[fake["text"].str.len() > 20]               # drop garbage rows
print(f"Fake news rows : {len(fake)}")

# ==========================================
# 2. Load true.csv → label = 1 (REAL)
# ==========================================
print("Loading true.csv ...")
true = pd.read_csv("true.csv", usecols=["title", "text"])
true["text"] = true["title"].fillna("") + " " + true["text"].fillna("")
true = true[["text"]]
true["label"] = 1
true = true[true["text"].str.len() > 20]
print(f"Real news rows : {len(true)}")

# ==========================================
# 3. (Optional) Load GDELT real news → label = 1
# ==========================================
gdelt = pd.DataFrame()
if os.path.exists("gdelt_news.csv") or os.path.exists("gdelt_large_dataset.csv"):
    print("Loading GDELT real news ...")
    gdelt = pd.read_csv("gdelt_news.csv" if os.path.exists("gdelt_news.csv") else "gdelt_large_dataset.csv")
    gdelt["text"] = gdelt["title"].fillna("") + " " + gdelt["content"].fillna("")
    gdelt = gdelt[["text"]].drop_duplicates()
    gdelt["label"] = 1
    gdelt = gdelt[gdelt["text"].str.len() > 20]
    print(f"GDELT rows     : {len(gdelt)}")
else:
    print("No GDELT file found → skipping (that's fine)")

# ==========================================
# 4. Combine everything
# ==========================================
data = pd.concat([fake, true, gdelt], ignore_index=True)
data = data.sample(frac=1, random_state=42).reset_index(drop=True)

print(f"\nTotal training samples: {len(data)}")
print(data["label"].value_counts())

# ==========================================
# 5. Train / Test split
# ==========================================
X_train, X_test, y_train, y_test = train_test_split(
    data["text"], data["label"], test_size=0.20, random_state=42, stratify=data["label"]
)

# ==========================================
# 6. Vectorize (this is where most people get 98–99% accuracy on this dataset)
# ==========================================
vectorizer = TfidfVectorizer(
    stop_words="english",
    max_features=100000,
    ngram_range=(1, 2),      # unigrams + bigrams = huge boost
    min_df=2,
    max_df=0.35
)

X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec  = vectorizer.transform(X_test)

# ==========================================
# 7. Train calibrated Logistic Regression (gives you probabilities)
# ==========================================
print("\nTraining the model (this takes 30–90 seconds)...")
base = LogisticRegression(max_iter=1000, C=3.0, solver="saga")
model = CalibratedClassifierCV(base, cv=3, method="sigmoid")
model.fit(X_train_vec, y_train)

# ==========================================
# 8. Evaluate
# ==========================================
preds = model.predict(X_test_vec)
print("\n" + classification_report(y_test, preds, target_names=["FAKE", "REAL"]))

# ==========================================
# 9. Save everything
# ==========================================
joblib.dump(model, "fake_news_model.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")

print("\nModel and vectorizer saved → ready for Flask/FastAPI/Streamlit!")
print("   → fake_news_model.pkl")
print("   → vectorizer.pkl")
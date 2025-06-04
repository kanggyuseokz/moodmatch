import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

# 1. 데이터 불러오기
df = pd.read_csv("backend/data/IMDB Dataset.csv")  # CSV 다운로드 후 동일 폴더에

# 2. 전처리 (라벨 숫자화)
df['sentiment'] = df['sentiment'].map({'positive': 1, 'negative': 0})

# 3. 훈련/테스트 분리
X_train, X_test, y_train, y_test = train_test_split(
    df['review'], df['sentiment'], test_size=0.2, random_state=42
)

# 4. 벡터화 (TF-IDF)
vectorizer = TfidfVectorizer(max_features=5000, stop_words='english')
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# 5. 모델 학습
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train_vec, y_train)

# 6. 평가 출력
y_pred = model.predict(X_test_vec)
print(classification_report(y_test, y_pred))

# 7. 모델 저장
with open("emotion_model.pkl", "wb") as f:
    pickle.dump(model, f)

with open("tfidf_vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)

print("✅ 모델과 벡터 저장 완료!")
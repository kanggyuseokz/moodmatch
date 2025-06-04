import pickle
import os

# 프로젝트 루트(backend/)를 기준으로 모델과 벡터라이저 경로 지정
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "model", "emotion_model.pkl")
VECTORIZER_PATH = os.path.join(BASE_DIR, "model", "tfidf_vectorizer.pkl")

# 학습된 모델과 벡터라이저 로드 (모듈 import 시 한 번만 수행됨)
with open(MODEL_PATH, "rb") as f:
    emotion_model = pickle.load(f)

with open(VECTORIZER_PATH, "rb") as f:
    tfidf_vectorizer = pickle.load(f)


def predict_emotion(text: str) -> str:
    """
    입력된 텍스트를 TF-IDF 벡터로 변환한 뒤,
    RandomForestClassifier 모델로 감정을 예측하여
    'positive' 또는 'negative' 문자열로 반환한다.
    """
    # 1. 1차 전처리: 텍스트를 리스트 형태로 만들어 벡터라이저에 전달
    texts = [text]
    X_vec = tfidf_vectorizer.transform(texts)

    # 2. 모델 예측 (0 또는 1)
    pred = emotion_model.predict(X_vec)[0]

    # 3. 숫자 라벨 → 문자열 라벨로 변환
    return "positive" if pred == 1 else "negative"

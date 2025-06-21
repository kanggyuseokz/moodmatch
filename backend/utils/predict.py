# backend/utils/predict.py
import pickle
import os

# --- 경로 설정 ---
# 이 파일의 상위 디렉토리인 backend/ 를 기준으로 경로를 잡습니다.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "model", "emotion_model.pkl")
VECTORIZER_PATH = os.path.join(BASE_DIR, "model", "tfidf_vectorizer.pkl")

# --- 모델 및 벡터라이저 로드 (앱 실행 시 1회) ---
try:
    with open(MODEL_PATH, "rb") as f:
        emotion_model = pickle.load(f)

    with open(VECTORIZER_PATH, "rb") as f:
        tfidf_vectorizer = pickle.load(f)
except FileNotFoundError:
    emotion_model = None
    tfidf_vectorizer = None
    print("Warning: Model or Vectorizer file not found. Prediction will not work.")

def predict_emotion(text: str) -> str:
    """
    입력 텍스트의 감정을 'positive' 또는 'negative'로 예측합니다.
    (추후 모델이 세분화되면 'joy', 'sadness' 등으로 변경 가능)
    """
    if not emotion_model or not tfidf_vectorizer:
        raise RuntimeError("Model is not loaded. Check model file paths.")

    # 텍스트를 벡터로 변환
    vectorized_text = tfidf_vectorizer.transform([text])
    
    # 감정 예측 (0 또는 1)
    prediction = emotion_model.predict(vectorized_text)[0]
    
    # 현재 모델은 positive/negative만 예측하므로, 임의로 세부 감정에 매핑합니다.
    # 이 부분은 추후 고도화된 모델로 교체되어야 합니다.
    if prediction == 1:
        # positive -> 'joy', 'romance', 'touching', 'excitement' 중 랜덤 선택
        import random
        return random.choice(['joy', 'romance', 'touching', 'excitement'])
    else:
        # negative -> 'sadness', 'anger', 'fear' 중 랜덤 선택
        import random
        return random.choice(['sadness', 'anger', 'fear'])
# backend/utils/predict.py
import pickle
import os

# --- 새로운 모델 경로 설정 ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "model", "multiclass_model.pkl")
VECTORIZER_PATH = os.path.join(BASE_DIR, "model", "multiclass_vectorizer.pkl")
LABEL_MAP_PATH = os.path.join(BASE_DIR, "model", "id_to_label.pkl")

# --- 모델, 벡터라이저, 그리고 '숫자-감정 번역표' 로드 ---
try:
    with open(MODEL_PATH, "rb") as f:
        emotion_model = pickle.load(f)
    with open(VECTORIZER_PATH, "rb") as f:
        tfidf_vectorizer = pickle.load(f)
    with open(LABEL_MAP_PATH, "rb") as f:
        id_to_label = pickle.load(f)
    print("✅ 다중 감정 분류 모델 및 관련 파일 로드 성공!")
except FileNotFoundError:
    emotion_model, tfidf_vectorizer, id_to_label = None, None, None
    print("Warning: Multiclass model files not found. Prediction will not work.")

def predict_emotion(text: str) -> str:
    """
    입력 텍스트의 감정을 'joy', 'sadness' 등 여러 감정 중 하나로 예측합니다.
    """
    if not all([emotion_model, tfidf_vectorizer, id_to_label]):
        raise RuntimeError("Model or related files are not loaded.")

    # 1. 텍스트 벡터화
    vectorized_text = tfidf_vectorizer.transform([text])
    
    # 2. 모델 예측 -> 결과는 0, 1, 2... 같은 숫자 ID
    predicted_id = emotion_model.predict(vectorized_text)[0]
    
    # 3. 숫자 ID를 실제 감정 문자열('joy', 'sadness' 등)으로 변환
    predicted_label = id_to_label.get(predicted_id, "unknown")
    
    return predicted_label
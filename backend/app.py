# backend/app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

from utils.predict import predict_emotion
from utils.recommend import recommend_movies_by_emotion

# .env 파일에서 환경변수 로드
load_dotenv()

app = Flask(__name__)
CORS(app)  # 개발 중 모든 도메인 허용

@app.route("/api/predict-emotion", methods=["POST"])
def predict_emotion_route():
    """
    사용자 텍스트를 받아 감정을 예측합니다.
    """
    data = request.get_json()
    if not data or "text" not in data or not data["text"].strip():
        return jsonify({"error": "Text is required."}), 400

    try:
        user_text = data["text"]
        emotion_label = predict_emotion(user_text)
        return jsonify({"emotion": emotion_label}), 200
    except Exception as e:
        # 모델 로딩 실패 등 서버 내부 오류 처리
        print(f"Error in predict_emotion_route: {e}")
        return jsonify({"error": "Could not process the request."}), 500


@app.route("/api/recommend-content", methods=["POST"])
def recommend_content_route():
    """
    감정 라벨을 받아 영화를 추천합니다.
    """
    data = request.get_json()
    if not data or "emotion" not in data:
        return jsonify({"error": "Emotion is required."}), 400

    try:
        emotion_label = data["emotion"]
        recommendations = recommend_movies_by_emotion(emotion_label, top_n=10)
        return jsonify({"recommendations": recommendations}), 200
    except Exception as e:
        # API 키 부재 등 서버 내부 오류 처리
        print(f"Error in recommend_content_route: {e}")
        return jsonify({"error": "Could not retrieve recommendations."}), 500

@app.route("/api/health")
def health_check():
    """서비스 상태 확인용 엔드포인트"""
    return "OK", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
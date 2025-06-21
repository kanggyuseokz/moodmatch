from flask import Flask, request, jsonify
from flask_cors import CORS
from utils.predict import predict_emotion
from utils.recommend import recommend_by_emotion
import os

app = Flask(__name__)

# 개발 환경에서는 모든 출처를 허용하고,
# 실제 배포 시에는 특정 프론트엔드 주소만 허용하는 것이 안전합니다.
# 예: CORS(app, resources={r"/api/*": {"origins": "http://your-frontend-domain.com"}})
CORS(app)

@app.route("/api/predict-emotion", methods=["POST"])
def predict_emotion_route():
    """
    POST 요청으로 JSON 형식 {'text': '사용자 입력 텍스트'} 를 받습니다.
    텍스트가 없으면 400 에러를 반환합니다.
    """
    data = request.get_json()
    if not data or "text" not in data or not data["text"].strip():
        return jsonify({"error": "Text is required."}), 400

    try:
        user_text = data["text"]
        emotion_label = predict_emotion(user_text)
        return jsonify({"emotion": emotion_label}), 200
    except Exception as e:
        # 예측 함수에서 오류 발생 시 서버가 중단되지 않도록 처리
        print(f"Error in predict_emotion_route: {e}")
        return jsonify({"error": "Could not process the emotion prediction."}), 500


@app.route("/api/recommend-content", methods=["POST"])
def recommend_content_route():
    """
    POST 요청으로 {'emotion': '감정'}를 받으면,
    해당 감정에 맞는 콘텐츠 리스트를 JSON으로 반환합니다.
    """
    data = request.get_json()
    if not data or "emotion" not in data:
        return jsonify({"error": "No emotion provided"}), 400

    try:
        emotion_label = data["emotion"]
        # 추천할 콘텐츠 개수 (기본값: 5개)
        top_n = data.get("top_n", 20)
        recs = recommend_by_emotion(emotion_label, top_n=top_n)
        return jsonify({"recommendations": recs}), 200
    except Exception as e:
        # 추천 함수에서 오류 발생 시 서버가 중단되지 않도록 처리
        print(f"Error in recommend_content_route: {e}")
        return jsonify({"error": "Could not retrieve recommendations."}), 500

if __name__ == "__main__":
    # 환경 변수에서 포트 번호를 가져오고, 없으면 5000번을 기본값으로 사용
    port = int(os.environ.get("PORT", 5000))
    # debug=True는 개발 중에만 사용하고, 실제 서비스 시에는 False로 변경해야 합니다.
    app.run(host="0.0.0.0", port=port, debug=True)
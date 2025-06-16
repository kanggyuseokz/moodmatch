from flask import Flask, request, jsonify
from flask_cors import CORS
from utils.predict import predict_emotion
from utils.recommend import recommend_by_emotion

app = Flask(__name__)
CORS(app)  # 모든 도메인에서의 요청 허용 (프론트엔드 개발 편의를 위해)


@app.route("/predict-emotion", methods=["POST"])
def predict_emotion_route():
    """
    POST 요청으로 JSON 형식 {'text': '사용자 입력 텍스트'} 를 받는다.
    텍스트가 없으면 400 에러 반환. 있으면 predict_emotion() 호출 후
    {'emotion': 'positive' or 'negative'} 형태로 반환.
    """
    data = request.get_json()
    if not data or "text" not in data:
        return jsonify({"error": "No text provided"}), 400

    user_text = data["text"]
    # 감정 예측 함수 호출
    emotion_label = predict_emotion(user_text)
    return jsonify({"emotion": emotion_label}), 200


@app.route("/recommend-content", methods=["POST"])
def recommend_content_route():
    data = request.get_json()
    if not data or "emotion" not in data:
        return jsonify({"error": "No emotion provided"}), 400

    emotion_label = data["emotion"]
    recs = recommend_by_emotion(emotion_label, top_n=5)
    return jsonify({"recommendations": recs}), 200

def recommend_content_route():
    """
    (나중에 구현)  
    POST 요청으로 {'emotion': 'positive' or 'negative'}를 받으면,
    미리 정의한 감정→장르 매핑에 따라 추천 콘텐츠 리스트를 JSON으로 반환.
    """
    data = request.get_json()
    if not data or "emotion" not in data:
        return jsonify({"error": "No emotion provided"}), 400

    # TODO: 감정(emotion) 기반 콘텐츠 추천 로직 구현
    emotion_label = data["emotion"]
    # 예시: 더미 응답 (추후 실제 로직으로 교체)
    recommendations = [
        {
            "title": "Sample Movie A",
            "genre": ["Drama"],
            "overview": "A heartfelt drama movie for you.",
            "vote_average": 8.5
        },
        {
            "title": "Sample Movie B",
            "genre": ["Comedy"],
            "overview": "A lighthearted comedy to lift your mood.",
            "vote_average": 7.9
        }
    ]
    return jsonify({"recommendations": recommendations}), 200


if __name__ == "__main__":
    # 개발 환경에서 5000 포트로 실행
    app.run(host="0.0.0.0", port=5000, debug=True)

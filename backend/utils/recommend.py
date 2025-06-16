# backend/utils/recommend.py

import os
import json
import pandas as pd

# ─── 1. 경로 설정 ─────────────────────────────────
# 이 파일(utils/)의 상위 디렉토리인 backend/까지 찾아서
# data 폴더 안의 tmdb_5000_movies.csv를 읽습니다.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "tmdb_5000_movies.csv")

# ─── 2. 감정→장르 매핑 ────────────────────────────
EMOTION_GENRE_MAP = {
    "positive": ["Comedy", "Romance", "Family"],
    "negative": ["Drama", "Music", "Healing"],
    
}

# ─── 3. CSV 로드 및 전처리 ─────────────────────────
def load_movie_data(csv_path: str) -> pd.DataFrame:
    """
    TMDB CSV 파일을 읽어서,
    genres 컬럼(JSON 문자열) → genre_list 컬럼(list of names)으로 변환한 DataFrame 반환
    """
    df = pd.read_csv(csv_path)
    # genres 칼럼: '[{"id": 18, "name": "Drama"}, ...]' 형태의 문자열
    df["genre_list"] = df["genres"].apply(
        lambda s: [g["name"] for g in json.loads(s)] if pd.notna(s) else []
    )
    return df

# 모듈 로드 시 한 번만 읽어놓습니다.
movie_df = load_movie_data(DATA_PATH)


# ─── 4. 추천 함수 ──────────────────────────────────
def recommend_by_emotion(emotion: str, top_n: int = 5) -> list[dict]:
    """
    감정(emotion)에 대응하는 장르 리스트를 꺼내,
    해당 장르 중 하나라도 포함된 영화를 vote_average 기준으로 정렬하여
    상위 top_n개를 리스트로 반환합니다.
    
    반환 예시:
    [
      {
        "title": "Movie A",
        "genre_list": ["Drama","Romance"],
        "overview": "...",
        "vote_average": 8.5,
        "release_date": "2019-05-01"
      },
      ...
    ]
    """
    genres = EMOTION_GENRE_MAP.get(emotion, [])
    if not genres:
        return []

    # 필터링: genre_list 중 하나라도 포함되는 영화들
    mask = movie_df["genre_list"].apply(lambda gl: any(g in gl for g in genres))
    candidates = movie_df[mask]

    # 평점 순 정렬 후 상위 N개 선택
    top = candidates.sort_values("vote_average", ascending=False).head(top_n)

    # dict 리스트로 변환
    results = []
    for _, row in top.iterrows():
        results.append({
            "title": row["title"],
            "genre_list": row["genre_list"],
            "overview": row["overview"],
            "vote_average": row["vote_average"],
            "release_date": row.get("release_date", "")
        })
    return results

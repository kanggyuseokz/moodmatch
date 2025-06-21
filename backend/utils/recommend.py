# backend/utils/recommend.py

import os
import json
import requests

# --- 1. 설정 로드 ---
# 이 파일의 상위 폴더인 backend/를 기준으로 config.json 경로를 설정합니다.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(BASE_DIR, "config.json")

# 설정 파일을 한 번만 읽어옵니다.
try:
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        config = json.load(f)
    EMOTION_GENRE_MAP = config.get('EMOTION_GENRE_MAP', {})
    GENRE_NAME_TO_ID = config.get('TMDB_GENRE_NAME_TO_ID', {})
except FileNotFoundError:
    print(f"Warning: Configuration file not found at {CONFIG_PATH}")
    EMOTION_GENRE_MAP = {}
    GENRE_NAME_TO_ID = {}


# --- 2. TMDB API 설정 ---
# .env 파일에 저장된 API 키를 불러옵니다.
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
API_BASE_URL = "https://api.themoviedb.org/3"
POSTER_BASE_URL = "https://image.tmdb.org/t/p/w500"


def recommend_by_emotion(emotion: str, top_n: int = 10) -> list:
    """
    주어진 감정에 따라 TMDB API를 호출하여 영화 목록을 추천합니다.

    Args:
        emotion (str): 'joy', 'sadness' 등 감정 키워드
        top_n (int): 추천할 영화의 최대 개수

    Returns:
        list: 추천 영화 정보가 담긴 딕셔너리의 리스트
    """
    # 1. API 키 존재 여부 확인
    if not TMDB_API_KEY:
        print("Error: TMDB_API_KEY environment variable is not set.")
        return []

    # 2. 감정에 해당하는 장르 ID 목록 조회
    target_genres_names = EMOTION_GENRE_MAP.get(emotion, {}).get("genres")
    if not target_genres_names:
        print(f"Warning: No genres found for emotion '{emotion}'.")
        return []

    # 장르 이름을 장르 ID로 변환합니다.
    genre_ids = [str(GENRE_NAME_TO_ID[name]) for name in target_genres_names if name in GENRE_NAME_TO_ID]
    if not genre_ids:
        print(f"Warning: No valid genre IDs found for genres: {target_genres_names}")
        return []

    # 3. TMDB API에 보낼 요청 파라미터 구성
    discover_url = f"{API_BASE_URL}/discover/movie"
    params = {
        'api_key': TMDB_API_KEY,
        'language': 'ko-KR',
        'sort_by': 'popularity.desc',  # 인기순으로 정렬
        'include_adult': False,
        'include_video': False,
        'with_genres': ",".join(genre_ids),  # 장르 ID들을 쉼표로 연결
        'vote_count.gte': 100,  # 최소 투표 수가 100개 이상인 영화만 필터링
        'page': 1
    }

    # 4. API 호출 및 예외 처리
    try:
        response = requests.get(discover_url, params=params)
        response.raise_for_status()  # 200 OK 상태 코드가 아닐 경우 예외 발생
        data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
        return []

    # 5. 결과 데이터를 프론트엔드에 맞게 가공
    results = []
    for movie in data.get('results', [])[:top_n]:
        # 포스터 경로가 있을 때만 전체 이미지 URL을 생성합니다.
        poster_url = f"{POSTER_BASE_URL}{movie.get('poster_path')}" if movie.get('poster_path') else None

        results.append({
            'id': movie.get('id'),
            'title': movie.get('title'),
            'overview': movie.get('overview'),
            'release_date': movie.get('release_date'),
            'vote_average': round(movie.get('vote_average', 0), 1),
            'poster_url': poster_url,
        })

    return results
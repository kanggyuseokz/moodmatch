<!-- prettier-ignore-start -->
<h1 align="center">MoodMatch</h1>
<p align="center">
  <em>감정 분석 기반 영화 추천 서비스</em>
</p>
<!-- prettier-ignore-end -->

---

<p align="center">
  <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/python-3.8%2B-blue" alt="Python"></a>
  <a href="https://reactjs.org/"><img src="https://img.shields.io/badge/react-17%2B-blue" alt="React"></a>
</p>

---

## 📖 Table of Contents

1. [소개](#소개)
2. [✨ 주요 기능](#-주요-기능)
3. [🛠 기술 스택](#-기술-스택)
4. [📂 프로젝트 구조](#-프로젝트-구조)
5. [🚀 설치 및 실행](#-설치-및-실행)
   - [백엔드](#backend)
   - [프론트엔드](#frontend)
6. [📝 API 엔드포인트](#-api-엔드포인트)

---

## 소개

**MoodMatch**는 사용자가 입력한 텍스트에서 감정을 분석한 뒤,  
그 감정에 어울리는 영화를 실시간으로 추천해 주는 웹 애플리케이션입니다.

- 🧠 **감정 분석**: `joy`, `sadness`, `anger`, `fear`, `love`, `surprise` 6가지 감정 분류
- 🎥 **영화 추천**: TMDB API 연동으로 감정별 장르 매핑
- 🌐 **웹 인터페이스**: React 기반 동적 UI
- ⭐ **별점 표시**: 숫자 평점을 ★★★★☆ 형태로 시각화

---

## ✨ 주요 기능

- **감정 분석**  
  사용자가 입력한 영어 문장을 TF-IDF + Random Forest 모델로 분류하여  
  `joy`, `sadness`, `anger`, `fear`, `love`, `surprise` 중 하나의 감정을 반환합니다.

- **영화 추천**  
  분석된 감정에 맞는 장르를 `config.json`에서 조회하여 TMDB API 호출 →  
  상위 N개(기본 10개) 영화 정보(제목, 개봉일, 평점, 줄거리, 포스터)를 가져옵니다.

- **카드 UI 출력**  
  추천 영화 목록을 카드 형태로 정렬하여  
  포스터, 제목, 별점, 개봉일, 줄거리를 한눈에 볼 수 있습니다.

- **시각적 별점**  
  TMDB 평점을 5점 만점 ★ 아이콘으로 변환하여 보여줍니다.

- **줄거리 요약**  
  긴 줄거리는 최대 3줄까지 자동 요약 처리로 깔끔하게 출력합니다.

---

## 🛠 기술 스택

| 분야         | 기술 / 라이브러리                                               |
| ------------ | --------------------------------------------------------------- |
| **Backend**  | Python 3.8+, Flask, Flask-CORS, scikit-learn, Requests, python-dotenv |
| **Frontend** | React 17+, Axios, React Icons, CSS                              |
| **API**      | TMDB (The Movie Database)                                       |

---

## 📂 프로젝트 구조

```
moodmatch/
├─ backend/
│  ├─ model/
│  │  ├─ multiclass_model.pkl       # 훈련된 감정 분류 모델 (Random Forest)
│  │  ├─ multiclass_vectorizer.pkl  # TF-IDF 벡터라이저
│  │  └─ id_to_label.pkl            # 숫자 ID → 감정 레이블 매핑
│  ├─ data/
│  │  ├─ train.txt
│  │  ├─ val.txt
│  │  └─ test.txt
│  ├─ utils/
│  │  ├─ predict.py                 # 감정 예측 로직
│  │  └─ recommend.py               # 영화 추천 로직
│  ├─ app.py                        # Flask 애플리케이션 진입점
│  ├─ train_multiclass_model.py     # 모델 학습 스크립트
│  ├─ config.json                   # 감정 → 장르 매핑 설정
│  ├─ requirements.txt              # Python 의존성 목록
│  └─ .env                          # 환경 변수 (TMDB_API_KEY)
├─ frontend/
│  ├─ src/
│  │  ├─ App.js                     # 메인 React 컴포넌트
│  │  ├─ StarRating.js              # 별점 시각화 컴포넌트
│  │  ├─ App.css
│  │  ├─ StarRating.css
│  │  └─ index.js
│  └─ package.json                  # Node.js 의존성
```

---

## 🚀 설치 및 실행

### Backend

1. **폴더 이동 & 가상환경 생성**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate      # Windows: .\venv\Scripts\activate
   ```
2. **의존성 설치**
   ```bash
   pip install -r requirements.txt
   ```
3. **환경 변수 설정**  
   `backend/.env` 파일을 만들고:
   ```env
   TMDB_API_KEY=여기에_발급받은_TMDB_API_키
   ```
4. **(선택) 모델 재학습**
   ```bash
   python train_multiclass_model.py
   ```
5. **서버 실행**
   ```bash
   python app.py
   ```

> http://localhost:5000 에서 백엔드가 동작합니다.  
> 개발 시 디버그 모드: `FLASK_DEBUG=true python app.py`

---

### Frontend

1. **폴더 이동**
   ```bash
   cd frontend
   ```
2. **의존성 설치**
   ```bash
   npm install
   ```
3. **개발 서버 실행**
   ```bash
   npm start
   ```

> http://localhost:3000 에서 앱이 자동 오픈됩니다.

---

## 📝 API 엔드포인트

| 메서드 | 경로                       | 요청 Body                                      | 설명                                              |
| ------ | -------------------------- | ---------------------------------------------- | ------------------------------------------------- |
| POST   | `/api/predict-emotion`     | `{ "text": "I feel so happy today" }`          | 감정 예측 (joy / sadness / anger / fear / love / surprise) |
| POST   | `/api/recommend-content`   | `{ "emotion": "joy", "top_n": 10 }`            | 감정 기반 영화 추천 (기본 top 10)                 |

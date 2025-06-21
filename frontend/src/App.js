import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

// 백엔드 API 주소
const API_URL = 'http://localhost:5001/api';

function App() {
  // --- State 정의 ---
  const [textInput, setTextInput] = useState(''); // 사용자가 입력한 텍스트
  const [isLoading, setIsLoading] = useState(false); // 로딩 상태
  const [error, setError] = useState(null); // 에러 메시지
  const [emotion, setEmotion] = useState(null); // 분석된 감정
  const [recommendations, setRecommendations] = useState([]); // 추천 영화 목록

  // --- 이벤트 핸들러 ---
  const handleSubmit = async () => {
    if (!textInput.trim()) {
      setError('감정을 나타내는 텍스트를 입력해주세요.');
      return;
    }

    // 초기화
    setIsLoading(true);
    setError(null);
    setEmotion(null);
    setRecommendations([]);

    try {
      // 1. 감정 예측 API 호출
      const predictResponse = await axios.post(`${API_URL}/predict-emotion`, {
        text: textInput,
      });
      
      const predictedEmotion = predictResponse.data.emotion;
      setEmotion(predictedEmotion);

      // 2. 예측된 감정으로 추천 API 호출
      const recommendResponse = await axios.post(`${API_URL}/recommend-content`, {
        emotion: predictedEmotion,
      });
      
      setRecommendations(recommendResponse.data.recommendations);

    } catch (err) {
      console.error("API Error:", err);
      setError('요청 처리 중 오류가 발생했습니다. 백엔드 서버가 실행 중인지 확인해주세요.');
    } finally {
      setIsLoading(false);
    }
  };

  // --- UI 렌더링 ---
  return (
    <div className="App">
      <header className="App-header">
        <h1>MoodMatch: 감정 기반 영화 추천</h1>
        <p>오늘의 기분을 글로 표현해보세요. 어울리는 영화를 추천해 드립니다.</p>
      </header>

      <main className="content-wrapper">
        <div className="input-section">
          <textarea
            value={textInput}
            onChange={(e) => setTextInput(e.target.value)}
            placeholder="예: 오늘 정말 신나는 하루였어! 하늘을 나는 기분이야."
            rows="4"
          />
          <button onClick={handleSubmit} disabled={isLoading}>
            {isLoading ? '분석 중...' : '영화 추천받기'}
          </button>
        </div>

        {error && <div className="error-message">{error}</div>}

        {emotion && (
          <div className="result-section">
            <h2>분석된 감정: <span>{emotion}</span></h2>
          </div>
        )}
        
        {recommendations.length > 0 && (
          <div className="recommendation-grid">
            {recommendations.map((movie) => (
              <div key={movie.id} className="movie-card">
                <img src={movie.poster_url} alt={`${movie.title} 포스터`} onError={(e) => { e.target.style.display = 'none'; }} />
                <div className="movie-details">
                  <h3>{movie.title}</h3>
                  <p className="movie-meta">평점: {movie.vote_average} | 개봉: {movie.release_date}</p>
                  <p className="movie-overview">{movie.overview}</p>
                </div>
              </div>
            ))}
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
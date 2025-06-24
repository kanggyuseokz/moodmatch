import React, { useState } from 'react';
import axios from 'axios';
import './App.css';
import StarRating from './StarRating'

// 백엔드 API 주소
const API_URL = 'http://localhost:5000/api';

function App() {
  const [textInput, setTextInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [emotion, setEmotion] = useState(null);
  const [recommendations, setRecommendations] = useState([]);

  const handleSubmit = async () => {
    if (!textInput.trim()) {
      setError('감정을 나타내는 텍스트를 입력해주세요.');
      return;
    }

    setIsLoading(true);
    setError(null);
    setEmotion(null);
    setRecommendations([]);

    try {
      const predictResponse = await axios.post(`${API_URL}/predict-emotion`, {
        text: textInput,
      });
      
      const predictedEmotion = predictResponse.data.emotion;
      setEmotion(predictedEmotion);

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

  // --- ❗️ 1. 엔터 키 처리를 위한 함수 추가 ---
  const handleKeyDown = (e) => {
    // Shift 키와 함께 엔터를 누르면 줄바꿈을 허용합니다.
    if (e.key === 'Enter' && e.shiftKey) {
      return;
    }
    
    // 로딩 중일 때는 아무것도 하지 않습니다.
    if (isLoading) {
      e.preventDefault();
      return;
    }

    // 엔터 키만 눌렸을 때
    if (e.key === 'Enter') {
      e.preventDefault(); // 텍스트창의 기본 엔터 동작(줄바꿈)을 막습니다.
      handleSubmit();     // 버튼 클릭과 동일한 함수를 호출합니다.
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>MoodMatch: 감정 기반 영화 추천</h1>
        <p>오늘의 기분을 글로 표현해보세요. 어울리는 영화를 추천해 드립니다.</p>
      </header>

      <main className="content-wrapper">
        <div className="input-section">
          {/* --- ❗️ 2. textarea에 onKeyDown 이벤트 연결 --- */}
          <textarea
            value={textInput}
            onChange={(e) => setTextInput(e.target.value)}
            onKeyDown={handleKeyDown} // 이 부분을 추가합니다.
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
                  <div className="movie-meta">
                    <div className="rating-line">
                      <StarRating rating={movie.vote_average} />
                      <span className="movie-rating-text">({movie.vote_average})</span>
                    </div>
                    <div className="release-date-line">
                      {movie.release_date}
                    </div>
                  </div>
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

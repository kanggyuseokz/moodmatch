import React from 'react';
import { FaStar, FaStarHalfAlt, FaRegStar } from 'react-icons/fa';
import './StarRating.css'; // 별점 스타일을 위한 CSS 파일

const StarRating = ({ rating }) => {
  // TMDB 평점(0~10)을 5점 만점으로 변환
  const ratingOutOf5 = rating / 2;

  // 5개의 별을 렌더링할 배열을 만듭니다.
  const stars = [];
  for (let i = 1; i <= 5; i++) {
    if (i <= ratingOutOf5) {
      // 꽉 찬 별
      stars.push(<FaStar key={i} />);
    } else if (i - 0.5 <= ratingOutOf5) {
      // 반만 찬 별
      stars.push(<FaStarHalfAlt key={i} />);
    } else {
      // 빈 별
      stars.push(<FaRegStar key={i} />);
    }
  }

  return <div className="star-rating-container">{stars}</div>;
};

export default StarRating;
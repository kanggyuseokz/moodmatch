import { render, screen } from '@testing-library/react';
import App from './App';

test('renders app header', () => {
  render(<App />);
  expect(screen.getByText(/MoodMatch/i)).toBeInTheDocument();
});

test('renders textarea and submit button', () => {
  render(<App />);
  expect(screen.getByRole('textbox')).toBeInTheDocument();
  expect(screen.getByRole('button', { name: /영화 추천받기/i })).toBeInTheDocument();
});

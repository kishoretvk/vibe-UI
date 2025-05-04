import React, { useContext } from 'react';
import { ThemeContext } from '../contexts/ThemeContext';
import styles from './ThemeToggle.module.css';

const ThemeToggle: React.FC = () => {
  const { theme, toggleTheme } = useContext(ThemeContext);

  return (
    <div className={styles.toggleContainer}>
      <button 
        onClick={toggleTheme}
        className={styles.toggleButton}
        aria-label={`Switch to ${theme === 'light' ? 'dark' : 'light'} mode`}
      >
        <span className={styles.toggleIcon}>
          {theme === 'light' ? '🌙' : '☀️'}
        </span>
        <span className={styles.toggleText}>
          {theme === 'light' ? 'Dark Mode' : 'Light Mode'}
        </span>
      </button>
    </div>
  );
};

export default ThemeToggle;

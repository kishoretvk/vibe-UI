import React, { createContext, useState, useEffect, useMemo, ReactNode, Dispatch, SetStateAction } from 'react';

type Theme = 'light' | 'dark';

interface IThemeContext {
  theme: Theme;
  toggleTheme: () => void;
}

const defaultState: IThemeContext = {
  theme: 'light', // Default to light theme
  toggleTheme: () => {},
};

export const ThemeContext = createContext<IThemeContext>(defaultState);

interface ThemeProviderProps {
  children: ReactNode;
}

export const ThemeProvider: React.FC<ThemeProviderProps> = ({ children }) => {
  // Initialize theme from localStorage or default to 'light'
  const [theme, setTheme] = useState<Theme>(() => {
    const storedTheme = localStorage.getItem('appTheme') as Theme | null;
    return storedTheme || 'light';
  });

  // Apply theme class to body and update localStorage on change
  useEffect(() => {
    const body = document.body;
    body.classList.remove('light-theme', 'dark-theme'); // Remove previous theme class
    body.classList.add(`${theme}-theme`); // Add current theme class
    localStorage.setItem('appTheme', theme); // Persist theme choice
  }, [theme]);

  const toggleTheme = () => {
    setTheme((prevTheme) => (prevTheme === 'light' ? 'dark' : 'light'));
  };

  const contextValue = useMemo(() => ({
    theme,
    toggleTheme,
  }), [theme]); // Only recreate value if theme changes

  return (
    <ThemeContext.Provider value={contextValue}>
      {children}
    </ThemeContext.Provider>
  );
};

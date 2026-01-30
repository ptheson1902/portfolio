import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { useTranslation } from 'react-i18next';
import { Role, Language, Theme, AnswerMode } from '../types';

interface AppContextType {
  role: Role;
  setRole: (role: Role) => void;
  language: Language;
  setLanguage: (lang: Language) => void;
  theme: Theme;
  setTheme: (theme: Theme) => void;
  answerMode: AnswerMode;
  setAnswerMode: (mode: AnswerMode) => void;
}

const AppContext = createContext<AppContextType | undefined>(undefined);

export const AppProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const { i18n } = useTranslation();
  const [role, setRole] = useState<Role>('fullstack');
  const [language, setLanguage] = useState<Language>('ja');
  const [theme, setTheme] = useState<Theme>('light');
  const [answerMode, setAnswerMode] = useState<AnswerMode>('single');

  useEffect(() => {
    const savedTheme = localStorage.getItem('theme') as Theme;
    const savedLang = localStorage.getItem('language') as Language;
    const savedRole = localStorage.getItem('role') as Role;
    const savedMode = localStorage.getItem('answerMode') as AnswerMode;

    if (savedTheme) {
      setTheme(savedTheme);
      document.documentElement.classList.toggle('dark', savedTheme === 'dark');
    }
    if (savedLang) {
      setLanguage(savedLang);
      i18n.changeLanguage(savedLang);
    }
    if (savedRole) setRole(savedRole);
    if (savedMode) setAnswerMode(savedMode);
  }, [i18n]);

  const handleSetTheme = (newTheme: Theme) => {
    setTheme(newTheme);
    localStorage.setItem('theme', newTheme);
    document.documentElement.classList.toggle('dark', newTheme === 'dark');
  };

  const handleSetLanguage = (newLang: Language) => {
    setLanguage(newLang);
    localStorage.setItem('language', newLang);
    i18n.changeLanguage(newLang);
  };

  const handleSetRole = (newRole: Role) => {
    setRole(newRole);
    localStorage.setItem('role', newRole);
  };

  const handleSetAnswerMode = (newMode: AnswerMode) => {
    setAnswerMode(newMode);
    localStorage.setItem('answerMode', newMode);
  };

  return (
    <AppContext.Provider
      value={{
        role,
        setRole: handleSetRole,
        language,
        setLanguage: handleSetLanguage,
        theme,
        setTheme: handleSetTheme,
        answerMode,
        setAnswerMode: handleSetAnswerMode,
      }}
    >
      {children}
    </AppContext.Provider>
  );
};

export const useApp = () => {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error('useApp must be used within an AppProvider');
  }
  return context;
};

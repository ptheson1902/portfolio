import React from 'react';
import { useTranslation } from 'react-i18next';
import { Sun, Moon, Globe, User, MessageSquare, Code, Briefcase } from 'lucide-react';
import { useApp } from '../context/AppContext';
import { Role, Language } from '../types';

interface HeaderProps {
  activeSection: string;
  onSectionChange: (section: string) => void;
}

export const Header: React.FC<HeaderProps> = ({ activeSection, onSectionChange }) => {
  const { t } = useTranslation();
  const { role, setRole, language, setLanguage, theme, setTheme } = useApp();

  const roles: { value: Role; icon: React.ReactNode }[] = [
    { value: 'leader', icon: <Briefcase className="w-4 h-4" /> },
    { value: 'brse', icon: <Globe className="w-4 h-4" /> },
    { value: 'fullstack', icon: <Code className="w-4 h-4" /> },
  ];

  const languages: Language[] = ['ja', 'vi', 'en'];

  const navItems = [
    { id: 'profile', label: t('nav.profile'), icon: <User className="w-4 h-4" /> },
    { id: 'skills', label: t('nav.skills'), icon: <Code className="w-4 h-4" /> },
    { id: 'projects', label: t('nav.projects'), icon: <Briefcase className="w-4 h-4" /> },
    { id: 'chat', label: t('nav.chat'), icon: <MessageSquare className="w-4 h-4" /> },
  ];

  return (
    <header className="sticky top-0 z-50 bg-white/80 dark:bg-dark-bg/80 backdrop-blur-lg border-b border-slate-200 dark:border-dark-border">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center space-x-2">
            <div className="w-10 h-10 bg-primary-600 rounded-xl flex items-center justify-center">
              <span className="text-white font-bold text-lg">PS</span>
            </div>
            <div className="hidden sm:block">
              <h1 className="font-bold text-lg text-slate-900 dark:text-slate-100">
                PHAM THE SON
              </h1>
              <p className="text-xs text-slate-500 dark:text-slate-400">
                {t(`role.${role}`)}
              </p>
            </div>
          </div>

          <nav className="hidden md:flex items-center space-x-1">
            {navItems.map((item) => (
              <button
                key={item.id}
                onClick={() => onSectionChange(item.id)}
                className={`nav-link flex items-center space-x-2 ${
                  activeSection === item.id ? 'active' : ''
                }`}
              >
                {item.icon}
                <span>{item.label}</span>
              </button>
            ))}
          </nav>

          <div className="flex items-center space-x-2">
            <div className="flex items-center bg-slate-100 dark:bg-slate-800 rounded-lg p-1">
              {roles.map((r) => (
                <button
                  key={r.value}
                  onClick={() => setRole(r.value)}
                  className={`p-2 rounded-md transition-all ${
                    role === r.value
                      ? 'bg-white dark:bg-slate-700 shadow-sm text-primary-600 dark:text-primary-400'
                      : 'text-slate-500 hover:text-slate-700 dark:hover:text-slate-300'
                  }`}
                  title={t(`role.${r.value}`)}
                >
                  {r.icon}
                </button>
              ))}
            </div>

            <select
              value={language}
              onChange={(e) => setLanguage(e.target.value as Language)}
              className="bg-slate-100 dark:bg-slate-800 border-0 rounded-lg px-3 py-2 text-sm font-medium text-slate-700 dark:text-slate-300 focus:ring-2 focus:ring-primary-500"
            >
              {languages.map((lang) => (
                <option key={lang} value={lang}>
                  {t(`language.${lang}`)}
                </option>
              ))}
            </select>

            <button
              onClick={() => setTheme(theme === 'light' ? 'dark' : 'light')}
              className="p-2 rounded-lg bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-700 transition-colors"
            >
              {theme === 'light' ? (
                <Moon className="w-5 h-5" />
              ) : (
                <Sun className="w-5 h-5" />
              )}
            </button>
          </div>
        </div>

        <nav className="md:hidden flex items-center justify-around py-2 border-t border-slate-200 dark:border-dark-border">
          {navItems.map((item) => (
            <button
              key={item.id}
              onClick={() => onSectionChange(item.id)}
              className={`flex flex-col items-center p-2 rounded-lg ${
                activeSection === item.id
                  ? 'text-primary-600 dark:text-primary-400'
                  : 'text-slate-500'
              }`}
            >
              {item.icon}
              <span className="text-xs mt-1">{item.label}</span>
            </button>
          ))}
        </nav>
      </div>
    </header>
  );
};

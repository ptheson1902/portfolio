import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { Key, LogOut, Pencil, X, Check } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

export const AdminBar: React.FC = () => {
  const { t } = useTranslation();
  const { isAuthenticated, isEditMode, login, logout, toggleEditMode } = useAuth();
  const [showLoginModal, setShowLoginModal] = useState(false);
  const [tokenInput, setTokenInput] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    const success = await login(tokenInput);
    if (success) {
      setShowLoginModal(false);
      setTokenInput('');
    } else {
      setError(t('admin.invalidToken'));
    }
    setLoading(false);
  };

  return (
    <>
      {/* Admin controls */}
      <div className="fixed bottom-4 right-4 flex items-center gap-2 z-50">
        {isAuthenticated ? (
          <>
            <button
              onClick={toggleEditMode}
              className={`p-3 rounded-full shadow-lg transition-colors ${
                isEditMode
                  ? 'bg-amber-500 hover:bg-amber-600 text-white'
                  : 'bg-primary-600 hover:bg-primary-700 text-white'
              }`}
              title={isEditMode ? t('admin.exitEdit') : t('admin.enterEdit')}
            >
              {isEditMode ? <Check className="w-5 h-5" /> : <Pencil className="w-5 h-5" />}
            </button>
            <button
              onClick={logout}
              className="p-3 bg-red-600 text-white rounded-full shadow-lg hover:bg-red-700 transition-colors"
              title={t('admin.logout')}
            >
              <LogOut className="w-5 h-5" />
            </button>
          </>
        ) : (
          <button
            onClick={() => setShowLoginModal(true)}
            className="p-3 bg-slate-800 dark:bg-slate-700 text-white rounded-full shadow-lg hover:bg-slate-700 dark:hover:bg-slate-600 transition-colors"
            title={t('admin.login')}
          >
            <Key className="w-5 h-5" />
          </button>
        )}
      </div>

      {/* Login Modal */}
      {showLoginModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <div className="bg-white dark:bg-dark-card rounded-xl shadow-2xl p-6 w-full max-w-md mx-4">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-bold text-slate-900 dark:text-slate-100">
                {t('admin.loginTitle')}
              </h2>
              <button
                onClick={() => setShowLoginModal(false)}
                className="p-1 hover:bg-slate-100 dark:hover:bg-slate-700 rounded"
              >
                <X className="w-5 h-5 text-slate-500" />
              </button>
            </div>

            <form onSubmit={handleLogin}>
              <div className="mb-4">
                <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">
                  {t('admin.tokenLabel')}
                </label>
                <input
                  type="password"
                  value={tokenInput}
                  onChange={(e) => setTokenInput(e.target.value)}
                  className="w-full px-4 py-2 border border-slate-300 dark:border-slate-600 rounded-lg bg-white dark:bg-dark-bg text-slate-900 dark:text-slate-100 focus:outline-none focus:ring-2 focus:ring-primary-500"
                  placeholder={t('admin.tokenPlaceholder')}
                  autoFocus
                />
              </div>

              {error && (
                <p className="text-red-500 text-sm mb-4">{error}</p>
              )}

              <button
                type="submit"
                disabled={loading || !tokenInput}
                className="w-full py-2 px-4 bg-primary-600 hover:bg-primary-700 disabled:bg-slate-400 text-white rounded-lg font-medium transition-colors"
              >
                {loading ? t('admin.verifying') : t('admin.verify')}
              </button>
            </form>
          </div>
        </div>
      )}
    </>
  );
};

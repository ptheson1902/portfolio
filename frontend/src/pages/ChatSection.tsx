import React from 'react';
import { useTranslation } from 'react-i18next';
import { ChatBox } from '../components/ChatBox';

export const ChatSection: React.FC = () => {
  const { t } = useTranslation();

  return (
    <div className="space-y-6">
      <h2 className="section-title">{t('chat.title')}</h2>
      <ChatBox />
    </div>
  );
};

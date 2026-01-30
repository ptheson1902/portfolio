import React from 'react';
import { useTranslation } from 'react-i18next';
import { motion } from 'framer-motion';
import { GraduationCap, Briefcase, MapPin, Languages, CheckCircle } from 'lucide-react';
import { useProfile } from '../hooks/useApi';

export const ProfileSection: React.FC = () => {
  const { t } = useTranslation();
  const { data, loading } = useProfile();

  if (loading || !data) {
    return (
      <div className="animate-pulse space-y-4">
        <div className="h-8 bg-slate-200 dark:bg-slate-700 rounded w-1/4" />
        <div className="card p-6 space-y-4">
          <div className="h-6 bg-slate-200 dark:bg-slate-700 rounded w-1/2" />
          <div className="h-4 bg-slate-200 dark:bg-slate-700 rounded w-3/4" />
          <div className="h-4 bg-slate-200 dark:bg-slate-700 rounded w-2/3" />
        </div>
      </div>
    );
  }

  const { profile, role_emphasis } = data;

  const infoItems = [
    { icon: <GraduationCap className="w-5 h-5" />, label: t('profile.school'), value: profile.school },
    { icon: <Briefcase className="w-5 h-5" />, label: t('profile.experience'), value: profile.work_experience },
    { icon: <MapPin className="w-5 h-5" />, label: t('profile.japanResidence'), value: profile.japan_residence },
    { icon: <Languages className="w-5 h-5" />, label: t('profile.japaneseLevel'), value: profile.japanese_level },
  ];

  return (
    <div className="space-y-6">
      <h2 className="section-title">{t('profile.title')}</h2>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="card p-6"
      >
        <div className="flex flex-col md:flex-row gap-6">
          <div className="flex-shrink-0">
            <img
              src="/images/avatar.png"
              alt={profile.name}
              className="w-28 h-28 rounded-2xl object-cover shadow-lg ring-2 ring-primary-500/20"
            />
          </div>

          <div className="flex-1">
            <h3 className="text-2xl font-bold text-slate-900 dark:text-slate-100 mb-1">
              {profile.name}
            </h3>
            <p className="text-slate-500 dark:text-slate-400 mb-4">
              {profile.name_kana}
            </p>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              {infoItems.map((item, index) => (
                <div key={index} className="flex items-center space-x-3">
                  <div className="text-primary-600 dark:text-primary-400">
                    {item.icon}
                  </div>
                  <div>
                    <p className="text-xs text-slate-500 dark:text-slate-400">
                      {item.label}
                    </p>
                    <p className="font-medium text-slate-900 dark:text-slate-100">
                      {item.value}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </motion.div>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        className="card p-6"
      >
        <h4 className="font-semibold text-lg text-slate-900 dark:text-slate-100 mb-4">
          {t('profile.emphasis')}
        </h4>
        <div className="flex flex-wrap gap-2">
          {role_emphasis.map((item, index) => (
            <motion.span
              key={index}
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: 0.1 + index * 0.05 }}
              className="inline-flex items-center space-x-1 px-3 py-1.5 bg-primary-100 dark:bg-primary-900/30 text-primary-800 dark:text-primary-300 rounded-full text-sm font-medium"
            >
              <CheckCircle className="w-4 h-4" />
              <span>{item}</span>
            </motion.span>
          ))}
        </div>
      </motion.div>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
        className="card p-6"
      >
        <h4 className="font-semibold text-lg text-slate-900 dark:text-slate-100 mb-4">
          {t('profile.selfPr')}
        </h4>
        <p className="text-slate-700 dark:text-slate-300 whitespace-pre-line leading-relaxed">
          {profile.self_pr}
        </p>
      </motion.div>
    </div>
  );
};

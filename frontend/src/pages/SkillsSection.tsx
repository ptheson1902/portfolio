import React from 'react';
import { useTranslation } from 'react-i18next';
import { motion } from 'framer-motion';
import { Code, Layers, Database, Cloud, Cpu } from 'lucide-react';
import { useSkills } from '../hooks/useApi';
import { SkillCard } from '../components/SkillCard';

export const SkillsSection: React.FC = () => {
  const { t } = useTranslation();
  const { data, loading } = useSkills();

  if (loading || !data) {
    return (
      <div className="animate-pulse space-y-4">
        <div className="h-8 bg-slate-200 dark:bg-slate-700 rounded w-1/4" />
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {[...Array(6)].map((_, i) => (
            <div key={i} className="card p-4 h-20" />
          ))}
        </div>
      </div>
    );
  }

  const categories = [
    { key: 'programming_languages', title: t('skills.programming'), icon: <Code className="w-5 h-5" />, data: data.programming_languages },
    { key: 'frameworks', title: t('skills.frameworks'), icon: <Layers className="w-5 h-5" />, data: data.frameworks },
    { key: 'databases', title: t('skills.databases'), icon: <Database className="w-5 h-5" />, data: data.databases },
    { key: 'cloud', title: t('skills.cloud'), icon: <Cloud className="w-5 h-5" />, data: data.cloud },
    { key: 'other', title: t('skills.other'), icon: <Cpu className="w-5 h-5" />, data: data.other },
  ];

  return (
    <div className="space-y-8">
      <h2 className="section-title">{t('skills.title')}</h2>

      {categories.map((category, catIndex) => (
        category.data.length > 0 && (
          <motion.div
            key={category.key}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: catIndex * 0.1 }}
          >
            <div className="flex items-center space-x-2 mb-4">
              <div className="text-primary-600 dark:text-primary-400">
                {category.icon}
              </div>
              <h3 className="font-semibold text-lg text-slate-900 dark:text-slate-100">
                {category.title}
              </h3>
            </div>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
              {category.data.map((skill, index) => (
                <SkillCard key={skill.name} skill={skill} index={index} />
              ))}
            </div>
          </motion.div>
        )
      ))}

      <div className="card p-4">
        <h4 className="font-medium text-sm text-slate-500 dark:text-slate-400 mb-3">
          {t('skills.level')}
        </h4>
        <div className="flex flex-wrap gap-4 text-xs">
          {[
            { level: 1, label: 'Beginner', color: 'bg-slate-300' },
            { level: 2, label: 'Basic', color: 'bg-amber-400' },
            { level: 3, label: 'Intermediate', color: 'bg-green-400' },
            { level: 4, label: 'Advanced', color: 'bg-blue-500' },
            { level: 5, label: 'Expert', color: 'bg-purple-500' },
          ].map((item) => (
            <div key={item.level} className="flex items-center space-x-2">
              <div className={`w-4 h-2 rounded-full ${item.color}`} />
              <span className="text-slate-600 dark:text-slate-400">{item.label}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

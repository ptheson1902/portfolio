import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { motion } from 'framer-motion';
import { Code, Layers, Database, Cloud, Cpu, Plus, X, Check } from 'lucide-react';
import { useSkills, useSkillsMutation } from '../hooks/useApi';
import { useAuth } from '../context/AuthContext';
import { SkillCard } from '../components/SkillCard';
import { SkillUpdate } from '../types';

export const SkillsSection: React.FC = () => {
  const { t } = useTranslation();
  const { isEditMode } = useAuth();
  const { data, loading, refetch } = useSkills();
  const { updateSkill, deleteSkill, createSkill } = useSkillsMutation();
  const [addingToCategory, setAddingToCategory] = useState<string | null>(null);
  const [newSkillName, setNewSkillName] = useState('');
  const [newSkillLevel, setNewSkillLevel] = useState(3);
  const [newSkillExperience, setNewSkillExperience] = useState('');

  const handleUpdate = async (id: number, data: SkillUpdate): Promise<boolean> => {
    const result = await updateSkill(id, data);
    if (result) {
      await refetch();
      return true;
    }
    return false;
  };

  const handleDelete = async (id: number): Promise<boolean> => {
    const success = await deleteSkill(id);
    if (success) {
      await refetch();
      return true;
    }
    return false;
  };

  const handleAddSkill = async (category: string) => {
    if (!newSkillName.trim()) return;

    const result = await createSkill({
      name: newSkillName,
      level: newSkillLevel,
      experience: newSkillExperience || '1 year',
      category: category,
    });

    if (result) {
      await refetch();
      setAddingToCategory(null);
      setNewSkillName('');
      setNewSkillLevel(3);
      setNewSkillExperience('');
    }
  };

  const levelColors = [
    'bg-slate-300',
    'bg-amber-400',
    'bg-green-400',
    'bg-blue-500',
    'bg-purple-500',
  ];

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
    { key: 'ai_ml', title: t('skills.other'), icon: <Cpu className="w-5 h-5" />, data: data.other },
  ];

  return (
    <div className="space-y-8">
      <h2 className="section-title">{t('skills.title')}</h2>

      {categories.map((category, catIndex) => (
        (category.data.length > 0 || isEditMode) && (
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
              {isEditMode && (
                <button
                  onClick={() => setAddingToCategory(category.key)}
                  className="ml-auto p-1.5 bg-primary-100 dark:bg-primary-900/30 text-primary-600 dark:text-primary-400 rounded hover:bg-primary-200 dark:hover:bg-primary-900/50"
                  title="Add skill"
                >
                  <Plus className="w-4 h-4" />
                </button>
              )}
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
              {category.data.map((skill, index) => (
                <SkillCard
                  key={skill.id}
                  skill={skill}
                  index={index}
                  onUpdate={handleUpdate}
                  onDelete={handleDelete}
                />
              ))}

              {addingToCategory === category.key && (
                <motion.div
                  initial={{ opacity: 0, scale: 0.95 }}
                  animate={{ opacity: 1, scale: 1 }}
                  className="card p-4 ring-2 ring-primary-500"
                >
                  <div className="space-y-3">
                    <input
                      type="text"
                      value={newSkillName}
                      onChange={(e) => setNewSkillName(e.target.value)}
                      className="w-full px-2 py-1 border border-slate-300 dark:border-slate-600 rounded bg-white dark:bg-dark-bg text-slate-900 dark:text-slate-100 font-semibold"
                      placeholder="Skill name"
                      autoFocus
                    />
                    <input
                      type="text"
                      value={newSkillExperience}
                      onChange={(e) => setNewSkillExperience(e.target.value)}
                      className="w-full px-2 py-1 border border-slate-300 dark:border-slate-600 rounded bg-white dark:bg-dark-bg text-slate-900 dark:text-slate-100 text-sm"
                      placeholder="Experience (e.g., 3 years)"
                    />
                    <div className="flex items-center space-x-1">
                      {[1, 2, 3, 4, 5].map((level) => (
                        <button
                          key={level}
                          onClick={() => setNewSkillLevel(level)}
                          className={`w-6 h-4 rounded-full transition-all ${
                            level <= newSkillLevel
                              ? levelColors[newSkillLevel - 1]
                              : 'bg-slate-200 dark:bg-slate-700'
                          } hover:opacity-80`}
                        />
                      ))}
                      <span className="ml-2 text-xs text-slate-500">Level {newSkillLevel}</span>
                    </div>
                    <div className="flex gap-2 pt-2">
                      <button
                        onClick={() => handleAddSkill(category.key)}
                        className="flex-1 flex items-center justify-center gap-1 px-3 py-1.5 bg-green-600 text-white rounded text-sm hover:bg-green-700"
                      >
                        <Check className="w-4 h-4" />
                        Add
                      </button>
                      <button
                        onClick={() => {
                          setAddingToCategory(null);
                          setNewSkillName('');
                          setNewSkillLevel(3);
                          setNewSkillExperience('');
                        }}
                        className="flex-1 flex items-center justify-center gap-1 px-3 py-1.5 bg-slate-500 text-white rounded text-sm hover:bg-slate-600"
                      >
                        <X className="w-4 h-4" />
                        Cancel
                      </button>
                    </div>
                  </div>
                </motion.div>
              )}
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

import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { motion } from 'framer-motion';
import { GraduationCap, Briefcase, MapPin, Languages, CheckCircle, Plane, School, Building2, Globe2, Plus, Pencil, Trash2, Check, X, FileSpreadsheet, FileText, Globe } from 'lucide-react';
import { useProfile, useProfileMutation } from '../hooks/useApi';
import { useApp } from '../context/AppContext';
import { useAuth } from '../context/AuthContext';
import { InlineEdit } from '../components/InlineEdit';

// Use environment variable for API URL, fallback to relative path for dev
const API_BASE_URL = import.meta.env.VITE_API_URL || '';

interface CareerItem {
  year: string;
  title: string;
  description: string;
  color: string;
  current?: boolean;
}

const CAREER_COLORS = [
  'bg-blue-500',
  'bg-amber-500',
  'bg-green-500',
  'bg-purple-500',
  'bg-primary-500',
  'bg-red-500',
  'bg-indigo-500',
];

export const ProfileSection: React.FC = () => {
  const { t } = useTranslation();
  const { language } = useApp();
  const { isEditMode } = useAuth();
  const { data, loading, refetch } = useProfile();
  const { updateProfile, updateSelfPr } = useProfileMutation();

  // Career timeline state (stored in localStorage for persistence)
  const [careerTimeline, setCareerTimeline] = useState<Record<string, CareerItem[]>>(() => {
    const saved = localStorage.getItem('careerTimeline');
    if (saved) {
      return JSON.parse(saved);
    }
    return {
      ja: [
        { year: '2017', title: '来日', description: 'ベトナムから日本へ', color: 'bg-blue-500' },
        { year: '2017-2019', title: '日本語学校', description: '2年間の日本語学習', color: 'bg-amber-500' },
        { year: '2019-2022', title: 'ECCコンピュータ専門学校', description: '3年間のIT教育', color: 'bg-green-500' },
        { year: '2022-2023', title: '日系IT企業', description: '1年間の実務経験', color: 'bg-purple-500' },
        { year: '2023-現在', title: 'ベトナム系IT企業', description: '日本向けプロジェクト担当（3年目）', color: 'bg-primary-500', current: true },
      ],
      vi: [
        { year: '2017', title: 'Sang Nhật', description: 'Từ Việt Nam đến Nhật Bản', color: 'bg-blue-500' },
        { year: '2017-2019', title: 'Trường tiếng Nhật', description: '2 năm học tiếng Nhật', color: 'bg-amber-500' },
        { year: '2019-2022', title: 'ECC Computer College', description: '3 năm đào tạo IT', color: 'bg-green-500' },
        { year: '2022-2023', title: 'Công ty IT Nhật', description: '1 năm kinh nghiệm thực tế', color: 'bg-purple-500' },
        { year: '2023-Nay', title: 'Công ty IT Việt Nam', description: 'Dự án cho Nhật Bản (năm thứ 3)', color: 'bg-primary-500', current: true },
      ],
      en: [
        { year: '2017', title: 'Came to Japan', description: 'From Vietnam to Japan', color: 'bg-blue-500' },
        { year: '2017-2019', title: 'Japanese Language School', description: '2 years of Japanese study', color: 'bg-amber-500' },
        { year: '2019-2022', title: 'ECC Computer College', description: '3 years of IT education', color: 'bg-green-500' },
        { year: '2022-2023', title: 'Japanese IT Company', description: '1 year practical experience', color: 'bg-purple-500' },
        { year: '2023-Present', title: 'Vietnamese IT Company', description: 'Japan-focused projects (3rd year)', color: 'bg-primary-500', current: true },
      ],
    };
  });

  const [editingCareerIndex, setEditingCareerIndex] = useState<number | null>(null);
  const [showAddCareer, setShowAddCareer] = useState(false);
  const [newCareer, setNewCareer] = useState({ year: '', title: '', description: '', color: 'bg-blue-500', current: false });

  const saveCareerTimeline = (newTimeline: Record<string, CareerItem[]>) => {
    setCareerTimeline(newTimeline);
    localStorage.setItem('careerTimeline', JSON.stringify(newTimeline));
  };

  const handleAddCareer = () => {
    if (!newCareer.year.trim() || !newCareer.title.trim()) return;

    const updatedTimeline = { ...careerTimeline };
    // Add to all languages
    ['ja', 'vi', 'en'].forEach(lang => {
      updatedTimeline[lang] = [...(updatedTimeline[lang] || []), { ...newCareer }];
    });
    saveCareerTimeline(updatedTimeline);
    setShowAddCareer(false);
    setNewCareer({ year: '', title: '', description: '', color: 'bg-blue-500', current: false });
  };

  const handleUpdateCareer = (index: number, field: keyof CareerItem, value: string | boolean) => {
    const updatedTimeline = { ...careerTimeline };
    if (updatedTimeline[language]) {
      updatedTimeline[language][index] = { ...updatedTimeline[language][index], [field]: value };
      saveCareerTimeline(updatedTimeline);
    }
  };

  const handleDeleteCareer = (index: number) => {
    if (!window.confirm('Delete this career entry?')) return;
    const updatedTimeline = { ...careerTimeline };
    ['ja', 'vi', 'en'].forEach(lang => {
      if (updatedTimeline[lang]) {
        updatedTimeline[lang] = updatedTimeline[lang].filter((_, i) => i !== index);
      }
    });
    saveCareerTimeline(updatedTimeline);
  };

  const handleUpdateProfile = async (field: string, value: string) => {
    const success = await updateProfile({ [field]: value });
    if (!success) {
      throw new Error('Failed to update profile');
    }
    await refetch();
  };

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
  const timeline = careerTimeline[language] || careerTimeline.ja;
  const careerTitle = { ja: '経歴', vi: 'Lịch sử nghề nghiệp', en: 'Career History' };

  const handleExport = (format: 'pdf' | 'html' | 'xlsx') => {
    const url = `${API_BASE_URL}/api/export/resume?lang=${language}&format=${format}`;
    if (format === 'html') {
      window.open(url, '_blank');
    } else {
      window.location.href = url;
    }
  };

  const getIcon = (index: number) => {
    const icons = [Plane, School, GraduationCap, Building2, Globe2];
    const IconComponent = icons[index % icons.length];
    return <IconComponent className="w-4 h-4" />;
  };

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
              {isEditMode ? (
                <InlineEdit
                  value={profile.name}
                  onSave={async (value) => handleUpdateProfile('name', value)}
                  className="text-2xl font-bold"
                />
              ) : (
                profile.name
              )}
            </h3>
            <p className="text-slate-500 dark:text-slate-400 mb-4">
              {isEditMode ? (
                <InlineEdit
                  value={profile.name_kana}
                  onSave={async (value) => handleUpdateProfile('name_kana', value)}
                />
              ) : (
                profile.name_kana
              )}
            </p>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div className="flex items-center space-x-3">
                <div className="text-primary-600 dark:text-primary-400">
                  <GraduationCap className="w-5 h-5" />
                </div>
                <div className="flex-1">
                  <p className="text-xs text-slate-500 dark:text-slate-400">
                    {t('profile.school')}
                  </p>
                  {isEditMode ? (
                    <InlineEdit
                      value={profile.school}
                      onSave={async (value) => handleUpdateProfile('school', value)}
                      className="font-medium"
                    />
                  ) : (
                    <p className="font-medium text-slate-900 dark:text-slate-100">
                      {profile.school}
                    </p>
                  )}
                </div>
              </div>

              <div className="flex items-center space-x-3">
                <div className="text-primary-600 dark:text-primary-400">
                  <Briefcase className="w-5 h-5" />
                </div>
                <div className="flex-1">
                  <p className="text-xs text-slate-500 dark:text-slate-400">
                    {t('profile.experience')}
                  </p>
                  {isEditMode ? (
                    <InlineEdit
                      value={profile.work_experience}
                      onSave={async (value) => handleUpdateProfile('work_experience', value)}
                      className="font-medium"
                    />
                  ) : (
                    <p className="font-medium text-slate-900 dark:text-slate-100">
                      {profile.work_experience}
                    </p>
                  )}
                </div>
              </div>

              <div className="flex items-center space-x-3">
                <div className="text-primary-600 dark:text-primary-400">
                  <MapPin className="w-5 h-5" />
                </div>
                <div className="flex-1">
                  <p className="text-xs text-slate-500 dark:text-slate-400">
                    {t('profile.japanResidence')}
                  </p>
                  {isEditMode ? (
                    <InlineEdit
                      value={profile.japan_residence}
                      onSave={async (value) => handleUpdateProfile('japan_residence', value)}
                      className="font-medium"
                    />
                  ) : (
                    <p className="font-medium text-slate-900 dark:text-slate-100">
                      {profile.japan_residence}
                    </p>
                  )}
                </div>
              </div>

              <div className="flex items-center space-x-3">
                <div className="text-primary-600 dark:text-primary-400">
                  <Languages className="w-5 h-5" />
                </div>
                <div className="flex-1">
                  <p className="text-xs text-slate-500 dark:text-slate-400">
                    {t('profile.japaneseLevel')}
                  </p>
                  {isEditMode ? (
                    <InlineEdit
                      value={profile.japanese_level}
                      onSave={async (value) => handleUpdateProfile('japanese_level', value)}
                      className="font-medium"
                    />
                  ) : (
                    <p className="font-medium text-slate-900 dark:text-slate-100">
                      {profile.japanese_level}
                    </p>
                  )}
                </div>
              </div>
            </div>

            {/* Export Buttons */}
            <div className="mt-6 pt-4 border-t border-slate-200 dark:border-slate-700">
              <p className="text-xs text-slate-500 dark:text-slate-400 mb-2">
                {language === 'ja' ? 'スキルシート' : language === 'vi' ? 'Bảng kỹ năng' : 'Skill Sheet'}
              </p>
              <div className="flex gap-2">
                <button
                  onClick={() => handleExport('xlsx')}
                  className="flex items-center gap-1.5 px-3 py-1.5 bg-emerald-100 dark:bg-emerald-900/30 text-emerald-700 dark:text-emerald-400 rounded-lg hover:bg-emerald-200 dark:hover:bg-emerald-900/50 transition-colors text-sm font-medium"
                >
                  <FileSpreadsheet className="w-4 h-4" />
                  XLSX
                </button>
                <button
                  onClick={() => handleExport('pdf')}
                  className="flex items-center gap-1.5 px-3 py-1.5 bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-400 rounded-lg hover:bg-green-200 dark:hover:bg-green-900/50 transition-colors text-sm font-medium"
                >
                  <FileText className="w-4 h-4" />
                  PDF
                </button>
                <button
                  onClick={() => handleExport('html')}
                  className="flex items-center gap-1.5 px-3 py-1.5 bg-purple-100 dark:bg-purple-900/30 text-purple-700 dark:text-purple-400 rounded-lg hover:bg-purple-200 dark:hover:bg-purple-900/50 transition-colors text-sm font-medium"
                >
                  <Globe className="w-4 h-4" />
                  HTML
                </button>
              </div>
            </div>
          </div>
        </div>
      </motion.div>

      {/* Career Timeline */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        className="card p-6"
      >
        <div className="flex items-center justify-between mb-6">
          <h4 className="font-semibold text-lg text-slate-900 dark:text-slate-100 flex items-center gap-2">
            <Briefcase className="w-5 h-5 text-primary-600" />
            {careerTitle[language] || careerTitle.ja}
          </h4>
          {isEditMode && (
            <button
              onClick={() => setShowAddCareer(true)}
              className="p-1.5 bg-primary-100 dark:bg-primary-900/30 text-primary-600 dark:text-primary-400 rounded hover:bg-primary-200 dark:hover:bg-primary-900/50"
              title="Add career entry"
            >
              <Plus className="w-4 h-4" />
            </button>
          )}
        </div>

        {/* Add Career Form */}
        {showAddCareer && (
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            className="mb-6 p-4 bg-slate-50 dark:bg-slate-800/50 rounded-lg border-2 border-primary-500"
          >
            <h5 className="font-medium text-slate-900 dark:text-slate-100 mb-3">Add Career Entry</h5>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              <input
                type="text"
                value={newCareer.year}
                onChange={(e) => setNewCareer({ ...newCareer, year: e.target.value })}
                className="px-3 py-2 border border-slate-300 dark:border-slate-600 rounded bg-white dark:bg-dark-bg text-slate-900 dark:text-slate-100"
                placeholder="Year (e.g., 2020-2021)"
              />
              <input
                type="text"
                value={newCareer.title}
                onChange={(e) => setNewCareer({ ...newCareer, title: e.target.value })}
                className="px-3 py-2 border border-slate-300 dark:border-slate-600 rounded bg-white dark:bg-dark-bg text-slate-900 dark:text-slate-100"
                placeholder="Title"
              />
              <input
                type="text"
                value={newCareer.description}
                onChange={(e) => setNewCareer({ ...newCareer, description: e.target.value })}
                className="px-3 py-2 border border-slate-300 dark:border-slate-600 rounded bg-white dark:bg-dark-bg text-slate-900 dark:text-slate-100 md:col-span-2"
                placeholder="Description"
              />
              <div className="flex items-center gap-2 md:col-span-2">
                <span className="text-sm text-slate-600 dark:text-slate-400">Color:</span>
                {CAREER_COLORS.map((color) => (
                  <button
                    key={color}
                    onClick={() => setNewCareer({ ...newCareer, color })}
                    className={`w-6 h-6 rounded-full ${color} ${newCareer.color === color ? 'ring-2 ring-offset-2 ring-slate-500' : ''}`}
                  />
                ))}
                <label className="flex items-center gap-1 ml-4">
                  <input
                    type="checkbox"
                    checked={newCareer.current}
                    onChange={(e) => setNewCareer({ ...newCareer, current: e.target.checked })}
                  />
                  <span className="text-sm text-slate-600 dark:text-slate-400">Current</span>
                </label>
              </div>
            </div>
            <div className="flex gap-2 mt-3">
              <button
                onClick={handleAddCareer}
                className="flex items-center gap-1 px-3 py-1.5 bg-green-600 text-white rounded text-sm hover:bg-green-700"
              >
                <Check className="w-4 h-4" />
                Add
              </button>
              <button
                onClick={() => setShowAddCareer(false)}
                className="flex items-center gap-1 px-3 py-1.5 bg-slate-500 text-white rounded text-sm hover:bg-slate-600"
              >
                <X className="w-4 h-4" />
                Cancel
              </button>
            </div>
          </motion.div>
        )}

        <div className="relative">
          {/* Timeline line */}
          <div className="absolute left-[19px] top-2 bottom-2 w-0.5 bg-gradient-to-b from-blue-500 via-green-500 to-primary-500" />

          <div className="space-y-4">
            {timeline.map((item, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.15 + index * 0.1 }}
                className={`relative flex gap-4 ${isEditMode ? 'group' : ''}`}
              >
                {/* Icon circle */}
                <div className={`relative z-10 w-10 h-10 rounded-full ${item.color} flex items-center justify-center text-white shadow-lg ${item.current ? 'ring-4 ring-primary-200 dark:ring-primary-800' : ''}`}>
                  {getIcon(index)}
                </div>

                {/* Content */}
                <div className={`flex-1 pb-4 ${index === timeline.length - 1 ? '' : 'border-b border-slate-100 dark:border-slate-800'}`}>
                  {editingCareerIndex === index ? (
                    <div className="space-y-2">
                      <input
                        type="text"
                        value={item.year}
                        onChange={(e) => handleUpdateCareer(index, 'year', e.target.value)}
                        className="px-2 py-1 text-xs border border-slate-300 dark:border-slate-600 rounded bg-white dark:bg-dark-bg"
                      />
                      <input
                        type="text"
                        value={item.title}
                        onChange={(e) => handleUpdateCareer(index, 'title', e.target.value)}
                        className="w-full px-2 py-1 border border-slate-300 dark:border-slate-600 rounded bg-white dark:bg-dark-bg font-semibold"
                      />
                      <input
                        type="text"
                        value={item.description}
                        onChange={(e) => handleUpdateCareer(index, 'description', e.target.value)}
                        className="w-full px-2 py-1 text-sm border border-slate-300 dark:border-slate-600 rounded bg-white dark:bg-dark-bg"
                      />
                      <div className="flex gap-2">
                        <button
                          onClick={() => setEditingCareerIndex(null)}
                          className="flex items-center gap-1 px-2 py-1 bg-green-600 text-white rounded text-xs"
                        >
                          <Check className="w-3 h-3" />
                          Done
                        </button>
                      </div>
                    </div>
                  ) : (
                    <>
                      <div className="flex flex-wrap items-center gap-2 mb-1">
                        <span className="text-xs font-semibold px-2 py-0.5 rounded-full bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400">
                          {item.year}
                        </span>
                        {item.current && (
                          <span className="text-xs font-semibold px-2 py-0.5 rounded-full bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-400 animate-pulse">
                            Current
                          </span>
                        )}
                        {isEditMode && (
                          <div className="flex gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                            <button
                              onClick={() => setEditingCareerIndex(index)}
                              className="p-1 bg-primary-100 dark:bg-primary-900/30 text-primary-600 dark:text-primary-400 rounded hover:bg-primary-200"
                            >
                              <Pencil className="w-3 h-3" />
                            </button>
                            <button
                              onClick={() => handleDeleteCareer(index)}
                              className="p-1 bg-red-100 dark:bg-red-900/30 text-red-600 dark:text-red-400 rounded hover:bg-red-200"
                            >
                              <Trash2 className="w-3 h-3" />
                            </button>
                          </div>
                        )}
                      </div>
                      <h5 className="font-semibold text-slate-900 dark:text-slate-100">
                        {item.title}
                      </h5>
                      <p className="text-sm text-slate-600 dark:text-slate-400">
                        {item.description}
                      </p>
                    </>
                  )}
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </motion.div>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
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
              transition={{ delay: 0.2 + index * 0.05 }}
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
        transition={{ delay: 0.3 }}
        className="card p-6"
      >
        <h4 className="font-semibold text-lg text-slate-900 dark:text-slate-100 mb-4">
          {t('profile.selfPr')}
        </h4>
        {isEditMode ? (
          <InlineEdit
            value={profile.self_pr}
            onSave={async (value) => {
              const success = await updateSelfPr(language, value);
              if (success) {
                await refetch();
              }
            }}
            multiline
            rows={6}
            className="text-slate-700 dark:text-slate-300 leading-relaxed"
            placeholder={t('profile.selfPrPlaceholder') || 'Enter self PR...'}
          />
        ) : (
          <p className="text-slate-700 dark:text-slate-300 whitespace-pre-line leading-relaxed">
            {profile.self_pr}
          </p>
        )}
      </motion.div>
    </div>
  );
};

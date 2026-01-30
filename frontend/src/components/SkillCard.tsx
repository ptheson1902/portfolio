import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Trash2, Pencil, Check, X } from 'lucide-react';
import { Skill, SkillUpdate } from '../types';
import { useAuth } from '../context/AuthContext';

interface SkillCardProps {
  skill: Skill;
  index: number;
  onUpdate?: (id: number, data: SkillUpdate) => Promise<boolean>;
  onDelete?: (id: number) => Promise<boolean>;
}

export const SkillCard: React.FC<SkillCardProps> = ({
  skill,
  index,
  onUpdate,
  onDelete
}) => {
  const { isEditMode } = useAuth();
  const [isEditing, setIsEditing] = useState(false);
  const [editName, setEditName] = useState(skill.name);
  const [editExperience, setEditExperience] = useState(skill.experience);
  const [editLevel, setEditLevel] = useState(skill.level);
  const [isSaving, setIsSaving] = useState(false);

  const levelColors = [
    'bg-slate-300',
    'bg-amber-400',
    'bg-green-400',
    'bg-blue-500',
    'bg-purple-500',
  ];

  const handleSave = async () => {
    if (!onUpdate) return;

    setIsSaving(true);
    const success = await onUpdate(skill.id, {
      name: editName !== skill.name ? editName : undefined,
      level: editLevel !== skill.level ? editLevel : undefined,
      experience: editExperience !== skill.experience ? editExperience : undefined,
    });

    if (success) {
      setIsEditing(false);
    }
    setIsSaving(false);
  };

  const handleCancel = () => {
    setEditName(skill.name);
    setEditExperience(skill.experience);
    setEditLevel(skill.level);
    setIsEditing(false);
  };

  const handleDelete = async () => {
    if (!onDelete) return;
    if (window.confirm(`Delete skill "${skill.name}"?`)) {
      await onDelete(skill.id);
    }
  };

  if (isEditMode && isEditing) {
    return (
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: index * 0.05 }}
        className="card p-4 ring-2 ring-primary-500"
      >
        <div className="space-y-3">
          <input
            type="text"
            value={editName}
            onChange={(e) => setEditName(e.target.value)}
            className="w-full px-2 py-1 border border-slate-300 dark:border-slate-600 rounded bg-white dark:bg-dark-bg text-slate-900 dark:text-slate-100 font-semibold"
            placeholder="Skill name"
          />
          <input
            type="text"
            value={editExperience}
            onChange={(e) => setEditExperience(e.target.value)}
            className="w-full px-2 py-1 border border-slate-300 dark:border-slate-600 rounded bg-white dark:bg-dark-bg text-slate-900 dark:text-slate-100 text-sm"
            placeholder="Experience (e.g., 3 years)"
          />
          <div className="flex items-center space-x-1">
            {[1, 2, 3, 4, 5].map((level) => (
              <button
                key={level}
                onClick={() => setEditLevel(level)}
                className={`w-6 h-4 rounded-full transition-all ${
                  level <= editLevel
                    ? levelColors[editLevel - 1]
                    : 'bg-slate-200 dark:bg-slate-700'
                } hover:opacity-80`}
              />
            ))}
            <span className="ml-2 text-xs text-slate-500">Level {editLevel}</span>
          </div>
          <div className="flex gap-2 pt-2">
            <button
              onClick={handleSave}
              disabled={isSaving}
              className="flex-1 flex items-center justify-center gap-1 px-3 py-1.5 bg-green-600 text-white rounded text-sm hover:bg-green-700 disabled:opacity-50"
            >
              <Check className="w-4 h-4" />
              Save
            </button>
            <button
              onClick={handleCancel}
              disabled={isSaving}
              className="flex-1 flex items-center justify-center gap-1 px-3 py-1.5 bg-slate-500 text-white rounded text-sm hover:bg-slate-600 disabled:opacity-50"
            >
              <X className="w-4 h-4" />
              Cancel
            </button>
          </div>
        </div>
      </motion.div>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.05 }}
      className={`card p-4 hover:shadow-md transition-shadow ${isEditMode ? 'group relative' : ''}`}
    >
      {isEditMode && (
        <div className="absolute top-2 right-2 flex gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
          <button
            onClick={() => setIsEditing(true)}
            className="p-1.5 bg-primary-100 dark:bg-primary-900/30 text-primary-600 dark:text-primary-400 rounded hover:bg-primary-200 dark:hover:bg-primary-900/50"
            title="Edit"
          >
            <Pencil className="w-3.5 h-3.5" />
          </button>
          <button
            onClick={handleDelete}
            className="p-1.5 bg-red-100 dark:bg-red-900/30 text-red-600 dark:text-red-400 rounded hover:bg-red-200 dark:hover:bg-red-900/50"
            title="Delete"
          >
            <Trash2 className="w-3.5 h-3.5" />
          </button>
        </div>
      )}
      <div className="flex items-center justify-between mb-2">
        <h4 className="font-semibold text-slate-900 dark:text-slate-100">
          {skill.name}
        </h4>
        <span className="text-sm text-slate-500 dark:text-slate-400">
          {skill.experience}
        </span>
      </div>
      <div className="flex items-center space-x-1">
        {[1, 2, 3, 4, 5].map((level) => (
          <div
            key={level}
            className={`w-6 h-2 rounded-full ${
              level <= skill.level
                ? levelColors[skill.level - 1]
                : 'bg-slate-200 dark:bg-slate-700'
            }`}
          />
        ))}
      </div>
    </motion.div>
  );
};

import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { useTranslation } from 'react-i18next';
import { ChevronDown, ChevronUp, Calendar, Users, Layers, Star, Pencil, Trash2, Check, X } from 'lucide-react';
import { Project, ProjectUpdate } from '../types';
import { useAuth } from '../context/AuthContext';
import { useApp } from '../context/AppContext';

interface ProjectCardProps {
  project: Project;
  index: number;
  isHighlighted: boolean;
  onUpdate?: (id: number, data: ProjectUpdate) => Promise<boolean>;
  onDelete?: (id: number) => Promise<boolean>;
}

export const ProjectCard: React.FC<ProjectCardProps> = ({
  project,
  index,
  isHighlighted,
  onUpdate,
  onDelete,
}) => {
  const { t } = useTranslation();
  const { isEditMode } = useAuth();
  const { language } = useApp();
  const [isExpanded, setIsExpanded] = useState(isHighlighted);
  const [isEditing, setIsEditing] = useState(false);
  const [editRole, setEditRole] = useState(project.role);
  const [editTeamSize, setEditTeamSize] = useState(project.team_size);
  const [editDescription, setEditDescription] = useState(project.description);
  const [editTechnologies, setEditTechnologies] = useState(project.technologies.join(', '));
  const [editStartDate, setEditStartDate] = useState(project.start_date);
  const [editEndDate, setEditEndDate] = useState(project.end_date || '');
  const [isSaving, setIsSaving] = useState(false);

  const handleDelete = async (e: React.MouseEvent) => {
    e.stopPropagation();
    if (!onDelete) return;
    if (window.confirm(`Delete project "${project.name}"?`)) {
      await onDelete(project.id);
    }
  };

  const handleEditClick = (e: React.MouseEvent) => {
    e.stopPropagation();
    setIsEditing(true);
    setIsExpanded(true);
  };

  const handleSave = async () => {
    if (!onUpdate) return;

    setIsSaving(true);
    const updateData: ProjectUpdate = {};

    if (editRole !== project.role) {
      updateData.role = editRole;
    }
    if (editTeamSize !== project.team_size) {
      updateData.team_size = editTeamSize;
    }
    if (editDescription !== project.description) {
      updateData.description = { ja: '', vi: '', en: '', [language]: editDescription };
    }
    const newTechnologies = editTechnologies.split(',').map(t => t.trim()).filter(Boolean);
    if (JSON.stringify(newTechnologies) !== JSON.stringify(project.technologies)) {
      updateData.technologies = newTechnologies;
    }
    if (editStartDate !== project.start_date) {
      updateData.start_date = editStartDate;
    }
    if (editEndDate !== (project.end_date || '')) {
      updateData.end_date = editEndDate || undefined;
    }

    const success = await onUpdate(project.id, updateData);
    if (success) {
      setIsEditing(false);
    }
    setIsSaving(false);
  };

  const handleCancel = () => {
    setEditRole(project.role);
    setEditTeamSize(project.team_size);
    setEditDescription(project.description);
    setEditTechnologies(project.technologies.join(', '));
    setEditStartDate(project.start_date);
    setEditEndDate(project.end_date || '');
    setIsEditing(false);
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.1 }}
      className={`card overflow-hidden ${
        isHighlighted ? 'ring-2 ring-primary-500' : ''
      } ${isEditMode && isEditing ? 'ring-2 ring-amber-500' : ''} ${isEditMode ? 'group' : ''}`}
    >
      <div
        className="p-4 cursor-pointer relative"
        onClick={() => !isEditing && setIsExpanded(!isExpanded)}
      >
        {isEditMode && !isEditing && (
          <div className="absolute top-2 right-10 flex gap-1 opacity-0 group-hover:opacity-100 transition-opacity z-10">
            <button
              onClick={handleEditClick}
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

        <div className="flex items-start justify-between">
          <div className="flex-1">
            <div className="flex items-center space-x-2 mb-1">
              {isHighlighted && (
                <Star className="w-4 h-4 text-amber-500 fill-amber-500" />
              )}
              <h3 className="font-semibold text-lg text-slate-900 dark:text-slate-100">
                {project.name}
              </h3>
            </div>
            <div className="flex flex-wrap items-center gap-3 text-sm text-slate-500 dark:text-slate-400">
              <span className="flex items-center space-x-1">
                <Users className="w-4 h-4" />
                <span>{project.role}</span>
              </span>
              <span className="flex items-center space-x-1">
                <Calendar className="w-4 h-4" />
                <span>{project.duration}</span>
              </span>
              <span className="flex items-center space-x-1">
                <Layers className="w-4 h-4" />
                <span>{project.team_size} {t('projects.teamSize')}</span>
              </span>
            </div>
          </div>
          <button className="p-1 text-slate-400 hover:text-slate-600 dark:hover:text-slate-300">
            {isExpanded ? (
              <ChevronUp className="w-5 h-5" />
            ) : (
              <ChevronDown className="w-5 h-5" />
            )}
          </button>
        </div>

        <div className="flex flex-wrap gap-2 mt-3">
          {project.technologies.slice(0, 5).map((tech) => (
            <span key={tech} className="skill-badge text-xs">
              {tech}
            </span>
          ))}
          {project.technologies.length > 5 && (
            <span className="skill-badge text-xs bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400">
              +{project.technologies.length - 5}
            </span>
          )}
        </div>
      </div>

      {isExpanded && (
        <motion.div
          initial={{ height: 0, opacity: 0 }}
          animate={{ height: 'auto', opacity: 1 }}
          exit={{ height: 0, opacity: 0 }}
          className="px-4 pb-4 border-t border-slate-200 dark:border-dark-border"
        >
          <div className="pt-4 space-y-4">
            {isEditing ? (
              <>
                <div>
                  <label className="text-sm font-medium text-slate-500 dark:text-slate-400 mb-1 block">
                    Role
                  </label>
                  <input
                    type="text"
                    value={editRole}
                    onChange={(e) => setEditRole(e.target.value)}
                    className="w-full px-3 py-2 border border-slate-300 dark:border-slate-600 rounded bg-white dark:bg-dark-bg text-slate-900 dark:text-slate-100"
                  />
                </div>
                <div>
                  <label className="text-sm font-medium text-slate-500 dark:text-slate-400 mb-1 block">
                    Team Size
                  </label>
                  <input
                    type="text"
                    value={editTeamSize}
                    onChange={(e) => setEditTeamSize(e.target.value)}
                    className="w-full px-3 py-2 border border-slate-300 dark:border-slate-600 rounded bg-white dark:bg-dark-bg text-slate-900 dark:text-slate-100"
                  />
                </div>
                <div>
                  <label className="text-sm font-medium text-slate-500 dark:text-slate-400 mb-1 block">
                    Technologies (comma separated)
                  </label>
                  <input
                    type="text"
                    value={editTechnologies}
                    onChange={(e) => setEditTechnologies(e.target.value)}
                    className="w-full px-3 py-2 border border-slate-300 dark:border-slate-600 rounded bg-white dark:bg-dark-bg text-slate-900 dark:text-slate-100"
                  />
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="text-sm font-medium text-slate-500 dark:text-slate-400 mb-1 block">
                      Start Date (YYYY-MM)
                    </label>
                    <input
                      type="month"
                      value={editStartDate}
                      onChange={(e) => setEditStartDate(e.target.value)}
                      className="w-full px-3 py-2 border border-slate-300 dark:border-slate-600 rounded bg-white dark:bg-dark-bg text-slate-900 dark:text-slate-100"
                    />
                  </div>
                  <div>
                    <label className="text-sm font-medium text-slate-500 dark:text-slate-400 mb-1 block">
                      End Date (YYYY-MM)
                    </label>
                    <input
                      type="month"
                      value={editEndDate}
                      onChange={(e) => setEditEndDate(e.target.value)}
                      placeholder="Leave empty for ongoing"
                      className="w-full px-3 py-2 border border-slate-300 dark:border-slate-600 rounded bg-white dark:bg-dark-bg text-slate-900 dark:text-slate-100"
                    />
                  </div>
                </div>
                <div>
                  <label className="text-sm font-medium text-slate-500 dark:text-slate-400 mb-1 block">
                    {t('projects.description')}
                  </label>
                  <textarea
                    value={editDescription}
                    onChange={(e) => setEditDescription(e.target.value)}
                    rows={4}
                    className="w-full px-3 py-2 border border-slate-300 dark:border-slate-600 rounded bg-white dark:bg-dark-bg text-slate-900 dark:text-slate-100"
                  />
                </div>
                <div className="flex gap-2 pt-2">
                  <button
                    onClick={handleSave}
                    disabled={isSaving}
                    className="flex-1 flex items-center justify-center gap-1 px-3 py-2 bg-green-600 text-white rounded hover:bg-green-700 disabled:opacity-50"
                  >
                    <Check className="w-4 h-4" />
                    Save
                  </button>
                  <button
                    onClick={handleCancel}
                    disabled={isSaving}
                    className="flex-1 flex items-center justify-center gap-1 px-3 py-2 bg-slate-500 text-white rounded hover:bg-slate-600 disabled:opacity-50"
                  >
                    <X className="w-4 h-4" />
                    Cancel
                  </button>
                </div>
              </>
            ) : (
              <>
                <div>
                  <h4 className="text-sm font-medium text-slate-500 dark:text-slate-400 mb-1">
                    {t('projects.phases')}
                  </h4>
                  <div className="flex flex-wrap gap-2">
                    {project.phases.map((phase) => (
                      <span
                        key={phase}
                        className="px-2 py-1 text-xs rounded bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300"
                      >
                        {phase}
                      </span>
                    ))}
                  </div>
                </div>

                <div>
                  <h4 className="text-sm font-medium text-slate-500 dark:text-slate-400 mb-1">
                    {t('projects.description')}
                  </h4>
                  <p className="text-slate-700 dark:text-slate-300 whitespace-pre-line text-sm">
                    {project.description}
                  </p>
                </div>

                <div>
                  <h4 className="text-sm font-medium text-slate-500 dark:text-slate-400 mb-1">
                    {t('projects.highlights')}
                  </h4>
                  <ul className="list-disc list-inside space-y-1">
                    {project.highlights.map((highlight, i) => (
                      <li
                        key={i}
                        className="text-sm text-slate-700 dark:text-slate-300"
                      >
                        {highlight}
                      </li>
                    ))}
                  </ul>
                </div>

                <div className="text-xs text-slate-400">
                  {project.start_date} - {project.end_date || 'Present'}
                </div>
              </>
            )}
          </div>
        </motion.div>
      )}
    </motion.div>
  );
};

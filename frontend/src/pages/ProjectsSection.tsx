import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { motion } from 'framer-motion';
import { Plus, X, Check } from 'lucide-react';
import { useProjects, useProjectsMutation } from '../hooks/useApi';
import { useAuth } from '../context/AuthContext';
import { ProjectCard } from '../components/ProjectCard';
import { ProjectUpdate, ProjectCreate } from '../types';

export const ProjectsSection: React.FC = () => {
  const { t } = useTranslation();
  const { isEditMode } = useAuth();
  const { data, loading, refetch } = useProjects();
  const { updateProject, deleteProject, createProject } = useProjectsMutation();
  const [showAddForm, setShowAddForm] = useState(false);
  const [isSaving, setIsSaving] = useState(false);

  // Form state
  const [newProject, setNewProject] = useState({
    name: '',
    role: '',
    team_size: '',
    technologies: '',
    environment: '',
    phases: '',
    start_date: '',
    end_date: '',
    description: '',
    highlights: '',
  });

  const handleUpdate = async (id: number, data: ProjectUpdate): Promise<boolean> => {
    const result = await updateProject(id, data);
    if (result) {
      await refetch();
      return true;
    }
    return false;
  };

  const handleDelete = async (id: number): Promise<boolean> => {
    const success = await deleteProject(id);
    if (success) {
      await refetch();
      return true;
    }
    return false;
  };

  const handleAddProject = async () => {
    if (!newProject.name.trim() || !newProject.role.trim()) return;

    setIsSaving(true);

    const projectData: ProjectCreate = {
      name: { ja: newProject.name, vi: newProject.name, en: newProject.name },
      role: newProject.role,
      team_size: newProject.team_size || '1',
      technologies: newProject.technologies.split(',').map(t => t.trim()).filter(Boolean),
      environment: newProject.environment || 'N/A',
      phases: newProject.phases.split(',').map(p => p.trim()).filter(Boolean),
      start_date: newProject.start_date || new Date().toISOString().slice(0, 7),
      end_date: newProject.end_date || undefined,
      description: { ja: newProject.description, vi: newProject.description, en: newProject.description },
      highlights: {
        ja: newProject.highlights.split('\n').filter(Boolean),
        vi: newProject.highlights.split('\n').filter(Boolean),
        en: newProject.highlights.split('\n').filter(Boolean),
      },
      relevance_fullstack: 5,
      relevance_leader: 5,
      relevance_brse: 5,
    };

    const result = await createProject(projectData);
    if (result) {
      await refetch();
      setShowAddForm(false);
      setNewProject({
        name: '',
        role: '',
        team_size: '',
        technologies: '',
        environment: '',
        phases: '',
        start_date: '',
        end_date: '',
        description: '',
        highlights: '',
      });
    }
    setIsSaving(false);
  };

  if (loading || !data) {
    return (
      <div className="animate-pulse space-y-4">
        <div className="h-8 bg-slate-200 dark:bg-slate-700 rounded w-1/4" />
        <div className="space-y-4">
          {[...Array(3)].map((_, i) => (
            <div key={i} className="card p-4 h-32" />
          ))}
        </div>
      </div>
    );
  }

  const { projects, highlighted } = data;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="section-title mb-0">{t('projects.title')}</h2>
        <div className="flex items-center gap-2">
          <span className="text-sm text-slate-500 dark:text-slate-400">
            {projects.length} projects
          </span>
          {isEditMode && (
            <button
              onClick={() => setShowAddForm(true)}
              className="p-1.5 bg-primary-100 dark:bg-primary-900/30 text-primary-600 dark:text-primary-400 rounded hover:bg-primary-200 dark:hover:bg-primary-900/50"
              title="Add project"
            >
              <Plus className="w-4 h-4" />
            </button>
          )}
        </div>
      </div>

      {/* Add Project Form */}
      {showAddForm && (
        <motion.div
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          className="card p-6 ring-2 ring-primary-500"
        >
          <h3 className="font-semibold text-lg text-slate-900 dark:text-slate-100 mb-4">
            Add New Project
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-slate-600 dark:text-slate-400 mb-1">
                Project Name *
              </label>
              <input
                type="text"
                value={newProject.name}
                onChange={(e) => setNewProject({ ...newProject, name: e.target.value })}
                className="w-full px-3 py-2 border border-slate-300 dark:border-slate-600 rounded bg-white dark:bg-dark-bg text-slate-900 dark:text-slate-100"
                placeholder="e.g., E-Commerce Platform"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-600 dark:text-slate-400 mb-1">
                Role *
              </label>
              <input
                type="text"
                value={newProject.role}
                onChange={(e) => setNewProject({ ...newProject, role: e.target.value })}
                className="w-full px-3 py-2 border border-slate-300 dark:border-slate-600 rounded bg-white dark:bg-dark-bg text-slate-900 dark:text-slate-100"
                placeholder="e.g., Full Stack Developer"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-600 dark:text-slate-400 mb-1">
                Team Size
              </label>
              <input
                type="text"
                value={newProject.team_size}
                onChange={(e) => setNewProject({ ...newProject, team_size: e.target.value })}
                className="w-full px-3 py-2 border border-slate-300 dark:border-slate-600 rounded bg-white dark:bg-dark-bg text-slate-900 dark:text-slate-100"
                placeholder="e.g., 5"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-600 dark:text-slate-400 mb-1">
                Start Date (YYYY-MM)
              </label>
              <input
                type="month"
                value={newProject.start_date}
                onChange={(e) => setNewProject({ ...newProject, start_date: e.target.value })}
                className="w-full px-3 py-2 border border-slate-300 dark:border-slate-600 rounded bg-white dark:bg-dark-bg text-slate-900 dark:text-slate-100"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-600 dark:text-slate-400 mb-1">
                End Date (YYYY-MM)
              </label>
              <input
                type="month"
                value={newProject.end_date}
                onChange={(e) => setNewProject({ ...newProject, end_date: e.target.value })}
                className="w-full px-3 py-2 border border-slate-300 dark:border-slate-600 rounded bg-white dark:bg-dark-bg text-slate-900 dark:text-slate-100"
                placeholder="Leave empty for ongoing"
              />
            </div>
            <div className="md:col-span-2">
              <label className="block text-sm font-medium text-slate-600 dark:text-slate-400 mb-1">
                Technologies (comma separated)
              </label>
              <input
                type="text"
                value={newProject.technologies}
                onChange={(e) => setNewProject({ ...newProject, technologies: e.target.value })}
                className="w-full px-3 py-2 border border-slate-300 dark:border-slate-600 rounded bg-white dark:bg-dark-bg text-slate-900 dark:text-slate-100"
                placeholder="e.g., React, TypeScript, Node.js, PostgreSQL"
              />
            </div>
            <div className="md:col-span-2">
              <label className="block text-sm font-medium text-slate-600 dark:text-slate-400 mb-1">
                Phases (comma separated)
              </label>
              <input
                type="text"
                value={newProject.phases}
                onChange={(e) => setNewProject({ ...newProject, phases: e.target.value })}
                className="w-full px-3 py-2 border border-slate-300 dark:border-slate-600 rounded bg-white dark:bg-dark-bg text-slate-900 dark:text-slate-100"
                placeholder="e.g., Design, Development, Testing, Deployment"
              />
            </div>
            <div className="md:col-span-2">
              <label className="block text-sm font-medium text-slate-600 dark:text-slate-400 mb-1">
                Environment
              </label>
              <input
                type="text"
                value={newProject.environment}
                onChange={(e) => setNewProject({ ...newProject, environment: e.target.value })}
                className="w-full px-3 py-2 border border-slate-300 dark:border-slate-600 rounded bg-white dark:bg-dark-bg text-slate-900 dark:text-slate-100"
                placeholder="e.g., AWS, Docker, Linux"
              />
            </div>
            <div className="md:col-span-2">
              <label className="block text-sm font-medium text-slate-600 dark:text-slate-400 mb-1">
                Description
              </label>
              <textarea
                value={newProject.description}
                onChange={(e) => setNewProject({ ...newProject, description: e.target.value })}
                rows={3}
                className="w-full px-3 py-2 border border-slate-300 dark:border-slate-600 rounded bg-white dark:bg-dark-bg text-slate-900 dark:text-slate-100"
                placeholder="Project description..."
              />
            </div>
            <div className="md:col-span-2">
              <label className="block text-sm font-medium text-slate-600 dark:text-slate-400 mb-1">
                Highlights (one per line)
              </label>
              <textarea
                value={newProject.highlights}
                onChange={(e) => setNewProject({ ...newProject, highlights: e.target.value })}
                rows={3}
                className="w-full px-3 py-2 border border-slate-300 dark:border-slate-600 rounded bg-white dark:bg-dark-bg text-slate-900 dark:text-slate-100"
                placeholder="Key achievement 1&#10;Key achievement 2&#10;Key achievement 3"
              />
            </div>
          </div>
          <div className="flex gap-2 mt-4">
            <button
              onClick={handleAddProject}
              disabled={isSaving || !newProject.name.trim() || !newProject.role.trim()}
              className="flex items-center gap-1 px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700 disabled:opacity-50"
            >
              <Check className="w-4 h-4" />
              Create Project
            </button>
            <button
              onClick={() => setShowAddForm(false)}
              disabled={isSaving}
              className="flex items-center gap-1 px-4 py-2 bg-slate-500 text-white rounded hover:bg-slate-600 disabled:opacity-50"
            >
              <X className="w-4 h-4" />
              Cancel
            </button>
          </div>
        </motion.div>
      )}

      <div className="space-y-4">
        {projects.map((project, index) => (
          <ProjectCard
            key={project.id}
            project={project}
            index={index}
            isHighlighted={highlighted.includes(project.id)}
            onUpdate={handleUpdate}
            onDelete={handleDelete}
          />
        ))}
      </div>
    </div>
  );
};

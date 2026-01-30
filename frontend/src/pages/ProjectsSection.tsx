import React from 'react';
import { useTranslation } from 'react-i18next';
import { useProjects } from '../hooks/useApi';
import { ProjectCard } from '../components/ProjectCard';

export const ProjectsSection: React.FC = () => {
  const { t } = useTranslation();
  const { data, loading } = useProjects();

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
        <span className="text-sm text-slate-500 dark:text-slate-400">
          {projects.length} projects
        </span>
      </div>

      <div className="space-y-4">
        {projects.map((project, index) => (
          <ProjectCard
            key={project.id}
            project={project}
            index={index}
            isHighlighted={highlighted.includes(project.id)}
          />
        ))}
      </div>
    </div>
  );
};

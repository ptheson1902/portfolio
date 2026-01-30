import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { useTranslation } from 'react-i18next';
import { ChevronDown, ChevronUp, Calendar, Users, Layers, Star } from 'lucide-react';
import { Project } from '../types';

interface ProjectCardProps {
  project: Project;
  index: number;
  isHighlighted: boolean;
}

export const ProjectCard: React.FC<ProjectCardProps> = ({
  project,
  index,
  isHighlighted,
}) => {
  const { t } = useTranslation();
  const [isExpanded, setIsExpanded] = useState(isHighlighted);

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.1 }}
      className={`card overflow-hidden ${
        isHighlighted ? 'ring-2 ring-primary-500' : ''
      }`}
    >
      <div
        className="p-4 cursor-pointer"
        onClick={() => setIsExpanded(!isExpanded)}
      >
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
          </div>
        </motion.div>
      )}
    </motion.div>
  );
};

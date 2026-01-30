import React from 'react';
import { motion } from 'framer-motion';
import { Skill } from '../types';

interface SkillCardProps {
  skill: Skill;
  index: number;
}

export const SkillCard: React.FC<SkillCardProps> = ({ skill, index }) => {
  const levelColors = [
    'bg-slate-300',
    'bg-amber-400',
    'bg-green-400',
    'bg-blue-500',
    'bg-purple-500',
  ];

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.05 }}
      className="card p-4 hover:shadow-md transition-shadow"
    >
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

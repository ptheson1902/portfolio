export type Role = 'leader' | 'brse' | 'fullstack';
export type Language = 'ja' | 'vi' | 'en';
export type AnswerMode = 'single' | 'bilingual';
export type Theme = 'light' | 'dark';

export interface Skill {
  id: number;
  name: string;
  level: number;
  experience: string;
  category: string;
}

export interface Project {
  id: number;
  name: string;
  role: string;
  team_size: string;
  technologies: string[];
  environment: string;
  phases: string[];
  start_date: string;
  end_date?: string;
  duration: string;
  description: string;
  highlights: string[];
}

export interface Profile {
  name: string;
  name_kana: string;
  gender: string;
  age: number;
  school: string;
  field: string;
  work_experience: string;
  japan_residence: string;
  japanese_level: string;
  self_pr: string;
}

export interface ProfileResponse {
  profile: Profile;
  role_emphasis: string[];
}

export interface SkillsResponse {
  programming_languages: Skill[];
  frameworks: Skill[];
  databases: Skill[];
  cloud: Skill[];
  other: Skill[];
}

export interface ProjectsResponse {
  projects: Project[];
  highlighted: number[];
}

export interface ChatRequest {
  question: string;
  lang: Language;
  role: Role;
  mode: AnswerMode;
}

export interface ChatResponse {
  answer: string;
  answer_secondary?: string;
  sources: string[];
}

export interface ChatMessage {
  id: string;
  type: 'user' | 'assistant';
  content: string;
  content_secondary?: string;
  timestamp: Date;
}

// Admin mutation types
export interface ProfileUpdate {
  name?: string;
  name_kana?: string;
  name_vi?: string;
  age?: number;
  school?: string;
  graduation_year?: number;
  field?: string;
  work_experience?: string;
  japan_residence?: string;
  japanese_level?: string;
}

export interface SkillCreate {
  name: string;
  category: string;
  level: number;
  experience: string;
}

export interface SkillUpdate {
  name?: string;
  level?: number;
  experience?: string;
  category?: string;
}

export interface SkillResponse {
  id: number;
  name: string;
  category: string;
  level: number;
  experience: string;
}

export interface ProjectCreate {
  name: Record<string, string>;
  role: string;
  team_size: string;
  technologies: string[];
  environment: string;
  phases: string[];
  start_date: string;
  end_date?: string;
  duration: string;
  description: Record<string, string>;
  highlights: Record<string, string[]>;
  relevance_fullstack?: number;
  relevance_leader?: number;
  relevance_brse?: number;
}

export interface ProjectUpdate {
  name?: Record<string, string>;
  role?: string;
  team_size?: string;
  technologies?: string[];
  environment?: string;
  phases?: string[];
  start_date?: string;
  end_date?: string;
  duration?: string;
  description?: Record<string, string>;
  highlights?: Record<string, string[]>;
  relevance_fullstack?: number;
  relevance_leader?: number;
  relevance_brse?: number;
}

export interface ProjectBrief {
  id: number;
  name: string;
  role: string;
  start_date: string;
  end_date?: string;
}

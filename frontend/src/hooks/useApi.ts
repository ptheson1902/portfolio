import { useState, useEffect, useCallback } from 'react';
import axios, { AxiosRequestConfig } from 'axios';
import { useApp } from '../context/AppContext';
import {
  ProfileResponse,
  SkillsResponse,
  ProjectsResponse,
  ChatRequest,
  ChatResponse,
  ProfileUpdate,
  SkillCreate,
  SkillUpdate,
  SkillResponse,
  ProjectCreate,
  ProjectUpdate,
  ProjectBrief,
} from '../types';

const AUTH_TOKEN_KEY = 'admin_token';

const api = axios.create({
  baseURL: '/api',
});

// Add auth header interceptor
api.interceptors.request.use((config) => {
  const token = localStorage.getItem(AUTH_TOKEN_KEY);
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const useProfile = () => {
  const { language, role } = useApp();
  const [data, setData] = useState<ProfileResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      try {
        const response = await api.get<ProfileResponse>('/profile', {
          params: { lang: language, role },
        });
        setData(response.data);
        setError(null);
      } catch (err) {
        setError(err as Error);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, [language, role]);

  return { data, loading, error };
};

export const useSkills = () => {
  const { language, role } = useApp();
  const [data, setData] = useState<SkillsResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      try {
        const response = await api.get<SkillsResponse>('/skills', {
          params: { lang: language, role },
        });
        setData(response.data);
        setError(null);
      } catch (err) {
        setError(err as Error);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, [language, role]);

  return { data, loading, error };
};

export const useProjects = () => {
  const { language, role } = useApp();
  const [data, setData] = useState<ProjectsResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      try {
        const response = await api.get<ProjectsResponse>('/projects', {
          params: { lang: language, role },
        });
        setData(response.data);
        setError(null);
      } catch (err) {
        setError(err as Error);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, [language, role]);

  return { data, loading, error };
};

export const useChat = () => {
  const { language, role, answerMode } = useApp();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  const sendMessage = useCallback(
    async (question: string): Promise<ChatResponse | null> => {
      setLoading(true);
      setError(null);
      try {
        const request: ChatRequest = {
          question,
          lang: language,
          role,
          mode: answerMode,
        };
        const response = await api.post<ChatResponse>('/chat', request);
        return response.data;
      } catch (err) {
        setError(err as Error);
        return null;
      } finally {
        setLoading(false);
      }
    },
    [language, role, answerMode]
  );

  return { sendMessage, loading, error };
};

// Mutation hooks for admin operations
export const useProfileMutation = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  const updateProfile = useCallback(async (data: ProfileUpdate): Promise<boolean> => {
    setLoading(true);
    setError(null);
    try {
      await api.put('/profile', data);
      return true;
    } catch (err) {
      setError(err as Error);
      return false;
    } finally {
      setLoading(false);
    }
  }, []);

  const updateSelfPr = useCallback(async (selfPr: Record<string, string>): Promise<boolean> => {
    setLoading(true);
    setError(null);
    try {
      await api.put('/profile/self-pr', { self_pr: selfPr });
      return true;
    } catch (err) {
      setError(err as Error);
      return false;
    } finally {
      setLoading(false);
    }
  }, []);

  return { updateProfile, updateSelfPr, loading, error };
};

export const useSkillsMutation = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  const createSkill = useCallback(async (data: SkillCreate): Promise<SkillResponse | null> => {
    setLoading(true);
    setError(null);
    try {
      const response = await api.post<SkillResponse>('/skills', data);
      return response.data;
    } catch (err) {
      setError(err as Error);
      return null;
    } finally {
      setLoading(false);
    }
  }, []);

  const updateSkill = useCallback(async (id: number, data: SkillUpdate): Promise<SkillResponse | null> => {
    setLoading(true);
    setError(null);
    try {
      const response = await api.put<SkillResponse>(`/skills/${id}`, data);
      return response.data;
    } catch (err) {
      setError(err as Error);
      return null;
    } finally {
      setLoading(false);
    }
  }, []);

  const deleteSkill = useCallback(async (id: number): Promise<boolean> => {
    setLoading(true);
    setError(null);
    try {
      await api.delete(`/skills/${id}`);
      return true;
    } catch (err) {
      setError(err as Error);
      return false;
    } finally {
      setLoading(false);
    }
  }, []);

  return { createSkill, updateSkill, deleteSkill, loading, error };
};

export const useProjectsMutation = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  const createProject = useCallback(async (data: ProjectCreate): Promise<ProjectBrief | null> => {
    setLoading(true);
    setError(null);
    try {
      const response = await api.post<ProjectBrief>('/projects', data);
      return response.data;
    } catch (err) {
      setError(err as Error);
      return null;
    } finally {
      setLoading(false);
    }
  }, []);

  const updateProject = useCallback(async (id: number, data: ProjectUpdate): Promise<ProjectBrief | null> => {
    setLoading(true);
    setError(null);
    try {
      const response = await api.put<ProjectBrief>(`/projects/${id}`, data);
      return response.data;
    } catch (err) {
      setError(err as Error);
      return null;
    } finally {
      setLoading(false);
    }
  }, []);

  const deleteProject = useCallback(async (id: number): Promise<boolean> => {
    setLoading(true);
    setError(null);
    try {
      await api.delete(`/projects/${id}`);
      return true;
    } catch (err) {
      setError(err as Error);
      return false;
    } finally {
      setLoading(false);
    }
  }, []);

  return { createProject, updateProject, deleteProject, loading, error };
};

import React, { createContext, useContext, useState, useEffect, ReactNode, useCallback } from 'react';
import axios from 'axios';

export type UserRole = 'owner' | 'visitor';

interface AuthContextType {
  isAuthenticated: boolean;
  role: UserRole;
  isEditMode: boolean;
  token: string | null;
  login: (token: string) => Promise<boolean>;
  logout: () => void;
  toggleEditMode: () => void;
  setEditMode: (value: boolean) => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

const AUTH_TOKEN_KEY = 'admin_token';

export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [token, setToken] = useState<string | null>(null);
  const [role, setRole] = useState<UserRole>('visitor');
  const [isEditMode, setIsEditMode] = useState(false);

  // Verify token on mount
  useEffect(() => {
    const savedToken = localStorage.getItem(AUTH_TOKEN_KEY);
    if (savedToken) {
      verifyToken(savedToken);
    }
  }, []);

  const verifyToken = async (tokenToVerify: string) => {
    try {
      const response = await axios.get('/api/auth/verify', {
        headers: { Authorization: `Bearer ${tokenToVerify}` },
      });
      if (response.data.valid) {
        setToken(tokenToVerify);
        setRole('owner');
        return true;
      }
    } catch {
      localStorage.removeItem(AUTH_TOKEN_KEY);
    }
    setToken(null);
    setRole('visitor');
    return false;
  };

  const login = useCallback(async (newToken: string): Promise<boolean> => {
    const isValid = await verifyToken(newToken);
    if (isValid) {
      localStorage.setItem(AUTH_TOKEN_KEY, newToken);
      return true;
    }
    return false;
  }, []);

  const logout = useCallback(() => {
    localStorage.removeItem(AUTH_TOKEN_KEY);
    setToken(null);
    setRole('visitor');
    setIsEditMode(false);
  }, []);

  const toggleEditMode = useCallback(() => {
    if (role === 'owner') {
      setIsEditMode((prev) => !prev);
    }
  }, [role]);

  const handleSetEditMode = useCallback((value: boolean) => {
    if (role === 'owner') {
      setIsEditMode(value);
    }
  }, [role]);

  return (
    <AuthContext.Provider
      value={{
        isAuthenticated: role === 'owner',
        role,
        isEditMode,
        token,
        login,
        logout,
        toggleEditMode,
        setEditMode: handleSetEditMode,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

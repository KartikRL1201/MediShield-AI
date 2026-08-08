import React, { createContext, useState, useEffect, ReactNode } from 'react';
import { UserProfile, LoginData, RegisterData } from '../../types/auth';
import authService from '../../services/authService';

interface AuthContextType {
  user: UserProfile | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (data: LoginData) => Promise<void>;
  register: (data: RegisterData) => Promise<void>;
  logout: () => void;
}

export const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<UserProfile | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);

  useEffect(() => {
    const initAuth = async () => {
      const token = localStorage.getItem('access_token');
      if (token) {
        try {
          const profile = await authService.getCurrentUser();
          setUser(profile);
        } catch (error) {
          console.error("Session expired or invalid", error);
          authService.logout();
        }
      }
      setIsLoading(false);
    };

    initAuth();
  }, []);

  const login = async (data: LoginData) => {
    await authService.login(data);
    const profile = await authService.getCurrentUser();
    setUser(profile);
  };

  const register = async (data: RegisterData) => {
    await authService.register(data);
    // Auto-login after successful registration
    await login({ email: data.email, password: data.password });
  };

  const logout = () => {
    authService.logout();
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{
      user,
      isAuthenticated: !!user,
      isLoading,
      login,
      register,
      logout
    }}>
      {children}
    </AuthContext.Provider>
  );
};

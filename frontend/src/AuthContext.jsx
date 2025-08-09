// src/AuthContext.jsx
import React, { createContext, useContext, useState, useEffect } from 'react';
import { apiClient } from './api.js';

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  const authenticate = async () => {
    try {
      setIsLoading(true);
      
      // Попытка аутентификации (в dev режиме используется тестовый пользователь)
      const authResult = await apiClient.authenticate();
      
      if (authResult.access_token) {
        apiClient.setToken(authResult.access_token);
        setUser(authResult.user);
        setIsAuthenticated(true);
      }
    } catch (error) {
      console.error('Authentication failed:', error);
      setIsAuthenticated(false);
      setUser(null);
    } finally {
      setIsLoading(false);
    }
  };

  const logout = () => {
    apiClient.removeToken();
    setUser(null);
    setIsAuthenticated(false);
  };

  useEffect(() => {
    // Проверка сохраненного токена при загрузке
    const token = localStorage.getItem('auth_token');
    if (token) {
      apiClient.setToken(token);
      // Попытка получить информацию о пользователе
      apiClient.getCurrentUser()
        .then(userData => {
          setUser(userData);
          setIsAuthenticated(true);
        })
        .catch(() => {
          // Токен невалиден, пытаемся аутентифицироваться заново
          authenticate();
        })
        .finally(() => setIsLoading(false));
    } else {
      // Нет токена, аутентифицируемся
      authenticate();
    }
  }, []);

  const value = {
    user,
    isAuthenticated,
    isLoading,
    authenticate,
    logout,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}; 
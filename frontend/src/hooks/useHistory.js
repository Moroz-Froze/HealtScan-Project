// src/hooks/useHistory.js
import { useState, useEffect } from 'react';
import { apiClient } from '../api.js';
import { useAuth } from '../AuthContext.jsx';

export const useHistory = () => {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const { isAuthenticated } = useAuth();

  const loadHistory = async (limit = 20, offset = 0) => {
    if (!isAuthenticated) return;
    
    try {
      setLoading(true);
      setError(null);
      const response = await apiClient.getQueryHistory(limit, offset);
      setHistory(response.history || []);
    } catch (err) {
      setError(err.message);
      console.error('Failed to load history:', err);
    } finally {
      setLoading(false);
    }
  };

  const clearHistory = async () => {
    if (!isAuthenticated) return;
    
    try {
      setLoading(true);
      await apiClient.clearHistory();
      setHistory([]);
    } catch (err) {
      setError(err.message);
      console.error('Failed to clear history:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (isAuthenticated) {
      loadHistory();
    }
  }, [isAuthenticated]);

  return {
    history,
    loading,
    error,
    loadHistory,
    clearHistory,
    refreshHistory: () => loadHistory(),
  };
}; 
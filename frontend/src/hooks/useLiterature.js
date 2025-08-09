// src/hooks/useLiterature.js
import { useState, useEffect } from 'react';
import { apiClient } from '../api.js';

export const useLiterature = () => {
  const [literature, setLiterature] = useState([]);
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const loadLiterature = async (category = null, search = null, limit = 20, offset = 0) => {
    try {
      setLoading(true);
      setError(null);
      const response = await apiClient.getLiterature(category, search, limit, offset);
      setLiterature(response.literature || []);
      setCategories(response.categories || []);
    } catch (err) {
      setError(err.message);
      console.error('Failed to load literature:', err);
    } finally {
      setLoading(false);
    }
  };

  const loadLiteratureDetail = async (id) => {
    try {
      setLoading(true);
      setError(null);
      return await apiClient.getLiteratureDetail(id);
    } catch (err) {
      setError(err.message);
      console.error('Failed to load literature detail:', err);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const searchLiterature = async (query, limit = 10) => {
    try {
      setLoading(true);
      setError(null);
      return await apiClient.searchLiterature(query, limit);
    } catch (err) {
      setError(err.message);
      console.error('Failed to search literature:', err);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadLiterature();
  }, []);

  return {
    literature,
    categories,
    loading,
    error,
    loadLiterature,
    loadLiteratureDetail,
    searchLiterature,
  };
}; 
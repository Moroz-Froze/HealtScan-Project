// src/api.js
const API_BASE_URL = import.meta.env.PROD ? 'http://127.0.0.1:8000' : '';

class ApiClient {
  constructor() {
    this.token = localStorage.getItem('auth_token');
  }

  setToken(token) {
    this.token = token;
    localStorage.setItem('auth_token', token);
  }

  removeToken() {
    this.token = null;
    localStorage.removeItem('auth_token');
  }

  async request(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;
    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    };

    if (this.token) {
      config.headers.Authorization = `Bearer ${this.token}`;
    }

    try {
      const response = await fetch(url, config);
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ message: 'Network error' }));
        throw new Error(errorData.detail || errorData.message || `HTTP ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('API request failed:', error);
      throw error;
    }
  }

  // Аутентификация
  async authenticate(initData = 'test_data') {
    return this.request('/api/auth', {
      method: 'POST',
      body: JSON.stringify({ initData }),
    });
  }

  async getCurrentUser() {
    return this.request('/api/auth/me');
  }

  // Сканирование
  async uploadImage(file) {
    const formData = new FormData();
    formData.append('file', file);
    
    return this.request('/api/scan/upload', {
      method: 'POST',
      headers: {
        // Убираем Content-Type, чтобы браузер установил правильный boundary для FormData
        Authorization: this.token ? `Bearer ${this.token}` : undefined,
      },
      body: formData,
    });
  }

  async getScanResult(scanId) {
    return this.request(`/api/scan/${scanId}`);
  }

  async getScanHistory(limit = 10, offset = 0) {
    return this.request(`/api/scan?limit=${limit}&offset=${offset}`);
  }

  // История запросов
  async getQueryHistory(limit = 20, offset = 0) {
    return this.request(`/api/history?limit=${limit}&offset=${offset}`);
  }

  async clearHistory() {
    return this.request('/api/history', {
      method: 'DELETE',
    });
  }

  // Справочная литература
  async getLiterature(category = null, search = null, limit = 20, offset = 0) {
    const params = new URLSearchParams();
    if (category) params.append('category', category);
    if (search) params.append('search', search);
    params.append('limit', limit);
    params.append('offset', offset);

    return this.request(`/api/literature?${params}`);
  }

  async getLiteratureDetail(id) {
    return this.request(`/api/literature/${id}`);
  }

  async getCategories() {
    return this.request('/api/literature/categories/');
  }

  async searchLiterature(query, limit = 10) {
    return this.request(`/api/literature/search/?q=${encodeURIComponent(query)}&limit=${limit}`);
  }
}

export const apiClient = new ApiClient(); 
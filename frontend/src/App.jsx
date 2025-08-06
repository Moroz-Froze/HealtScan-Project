import { useState } from 'react';

export default function App() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [imagePreview, setImagePreview] = useState('');

  const backendUrl = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000';

  const handleFileChange = async (e) => {
    const file = e.target.files?.[0];
    if (!file) return;

    // Показать превью
    const reader = new FileReader();
    reader.onload = () => setImagePreview(reader.result);
    reader.readAsDataURL(file);

    // Подготовить данные
    const formData = new FormData();
    formData.append('image', file);

    // Отправить
    setLoading(true);
    setError('');
    setResult(null);

    try {
      const response = await fetch(`${backendUrl}/predict`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`Ошибка сервера: ${response.status}`);
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      console.error('Ошибка:', err);
      setError(err.message || 'Не удалось обработать изображение');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h1>🔍 SkinWound AI</h1>
      <p>Загрузите фото кожной раны для анализа</p>

      {/* Кнопка загрузки */}
      <label className="upload-area">
        <span className="upload-text">
          {loading ? 'Обработка...' : '📎 Нажмите, чтобы выбрать фото'}
        </span>
        <input
          type="file"
          accept="image/*"
          onChange={handleFileChange}
          disabled={loading}
        />
      </label>

      {/* Превью изображения */}
      {imagePreview && (
        <div style={{ marginBottom: '20px' }}>
          <img
            src={imagePreview}
            alt="Preview"
            style={{
              maxWidth: '100%',
              maxHeight: '200px',
              borderRadius: '8px',
              border: '1px solid #ddd',
            }}
          />
        </div>
      )}

      {/* Состояние загрузки */}
      {loading && <p className="loading">Анализируем изображение...</p>}

      {/* Ошибка */}
      {error && <p className="error">⚠️ {error}</p>}

      {/* Результат */}
      {result && (
        <div className="result">
          <h3>Результат анализа</h3>
          <p><strong>Тип повреждения:</strong> {result.class}</p>
          <p><strong>Уверенность:</strong> {(result.confidence * 100).toFixed(2)}%</p>
          <p><strong>Рекомендации:</strong> {result.advice}</p>
        </div>
      )}
    </div>
  );
}
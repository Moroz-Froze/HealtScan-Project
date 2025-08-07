// src/App.jsx
import React, { useState } from 'react';
import './App.css';

const SkinScanApp = () => {
  const [image, setImage] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  // Имитация анализа нейросетью
  const mockAnalysis = (file) => {
    const types = [
      { condition: 'Прыщ / акне', recommendation: 'Рекомендуется использовать салициловую кислоту, избегать жирной пищи.' },
      { condition: 'Аллергическая реакция', recommendation: 'Возможно, контакт с раздражителем. Примите антигистаминное.' },
      { condition: 'Экзема', recommendation: 'Используйте увлажняющий крем, избегайте горячего душа.' },
      { condition: 'Папиллома', recommendation: 'Обратитесь к дерматологу для удаления.' },
      { condition: 'Родинка (невус)', recommendation: 'Не трогайте. При изменении — срочно к врачу.' },
    ];
    return types[Math.floor(Math.random() * types.length)];
  };

  const handleTakePhoto = async () => {
    try {
      // Имитация доступа к камере через Telegram
      const input = document.createElement('input');
      input.type = 'file';
      input.accept = 'image/*';
      input.capture = 'environment'; // задняя камера

      input.onchange = (e) => {
        const file = e.target.files[0];
        if (file) {
          const imageUrl = URL.createObjectURL(file);
          setImage(imageUrl);
          setLoading(true);

          // Эмуляция отправки в нейросеть
          setTimeout(() => {
            const analysis = mockAnalysis(file);
            setResult(analysis);
            setLoading(false);
          }, 2000);
        }
      };

      input.click();
    } catch (err) {
      console.error('Ошибка доступа к камере:', err);
      alert('Не удалось открыть камеру. Разрешите доступ.');
    }
  };

  const handleReset = () => {
    setImage(null);
    setResult(null);
    setLoading(false);
  };

  return (
    <div className="skin-scan-app">
      <h1>📸 SkinScan AI</h1>
      <p>Наведите камеру на кожную аномалию и сделайте снимок</p>

      {!image ? (
        <button className="photo-btn" onClick={handleTakePhoto}>
          📷 Сделать фото
        </button>
      ) : (
        <div className="result-section">
          <img src={image} alt="Skin anomaly" className="preview" />

          {loading ? (
            <div className="loading">
              <p>Анализируем... ⏳</p>
            </div>
          ) : (
            <div className="diagnosis">
              <h2>🔎 Результат анализа</h2>
              <p><strong>Диагноз:</strong> {result.condition}</p>
              <p><strong>Рекомендации:</strong> {result.recommendation}</p>
              <button className="retry-btn" onClick={handleReset}>
                Сделать новое фото
              </button>
            </div>
          )}
        </div>
      )}

      <footer className="footer">
        <small>⚠️ Это не замена врачу. При серьёзных симптомах — обращайтесь к дерматологу.</small>
      </footer>
    </div>
  );
};

export default SkinScanApp;
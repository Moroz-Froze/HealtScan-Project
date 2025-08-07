// src/main.jsx
import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import './index.css';
import App from './App.jsx';

import { init, miniApp, mainButton } from '@telegram-apps/sdk';

const initializeTelegramSDK = async () => {
  try {
    await init();

    // Готовим Mini App
    if (miniApp.ready.isAvailable()) {
      await miniApp.ready();
    }

    // Устанавливаем цвет заголовка
    miniApp.setHeaderColor('#f0f4ff');

    // Монтируем главную кнопку
    if (mainButton.mount.isAvailable()) {
      mainButton.mount();
    }

    // Настраиваем кнопку
    if (mainButton.setParams.isAvailable()) {
      mainButton.setParams({
        text: '📷 Сделать фото',
        backgroundColor: '#4A90E2',
        textColor: '#FFFFFF',
        isVisible: true,
        isEnabled: true,
      });
    }

    // Обработчик клика
    if (mainButton.onClick.isAvailable()) {
      mainButton.on('click', () => {
        const event = new CustomEvent('takePhotoRequest');
        window.dispatchEvent(event);
      });
    }

  } catch (error) {
    console.error('Ошибка инициализации SDK:', error);
  }
};

initializeTelegramSDK();

// Подключаем обработчик кастомного события
window.addEventListener('takePhotoRequest', () => {
  const input = document.createElement('input');
  input.type = 'file';
  input.accept = 'image/*';
  input.capture = 'environment';

  input.onchange = (e) => {
    const file = e.target.files[0];
    if (file) {
      const event = new CustomEvent('photoTaken', { detail: file });
      window.dispatchEvent(event);
    }
  };

  input.click();
});

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
  </StrictMode>
);
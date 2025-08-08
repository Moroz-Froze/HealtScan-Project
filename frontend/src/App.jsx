// src/App.jsx
import React, { useState } from 'react';
import './App.css';

// Компонент главной страницы
const HomePage = ({ onNavigate }) => {
  const [queryHistory] = useState([
    { id: 1, query: 'Укус слепня', icon: '🔍' },
    { id: 2, query: 'Укус комара', icon: '🔍' },
    { id: 3, query: 'Химический ожог', icon: '🔍' }
  ]);

  const handleScan = () => {
    onNavigate('loading');
  };

  const handleUploadImage = () => {
    onNavigate('upload');
  };

  const handleReferenceLiterature = () => {
    onNavigate('literature');
  };

  const handleSubscribe = () => {
    onNavigate('subscription');
  };

  return (
    <div className="zdrav-scan-app">
      {/* Заголовок */}
      <div className="header">
        <div className="welcome-text">
          <span>Добро пожаловать в </span>
        </div>
        
        {/* Логотип ЗдравСкан */}
        <div className="logo-container">
          <div className="text-logo">ЗдравСкан!</div>
        </div>
      </div>

      {/* История запросов */}
      <div className="query-history">
        <div className="history-title">История запросов</div>
        <div className="history-list">
          {queryHistory.map((item) => (
            <div key={item.id} className="history-item">
              <span className="history-icon">
                <img src="/images/Лупа.svg" alt="Лупа" className="history-icon-svg" />
              </span>
              <span className="history-text">{item.query}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Подписка */}
      <div className="subscription-section">
        <button className="subscribe-button" onClick={handleSubscribe}>
          <span className="subscribe-text">Оформить подписку</span>
          <span className="subscribe-icon">
            <img src="/images/Кредитки.svg" alt="Кредитки" className="credit-icon-svg" />
          </span>
        </button>
        <div className="subscription-status">подписка истекла 17.07.2025 г.</div>
      </div>

      {/* Реклама */}
      <div className="advertisement">
        <img src="/images/Group 3.svg" alt="Реклама" className="ad-image" />
      </div>

      {/* Основные кнопки */}
      <div className="main-actions">
        <button className="scan-button" onClick={handleScan}>
          <div className="scan-icon">
            <img src="/images/Кнопка скан квадрат с главного экрана.svg" alt="Скан" className="scan-icon-svg" />
          </div>
        </button>
        
        <div className="side-buttons">
          <button className="upload-button" onClick={handleUploadImage}>
            <span className="upload-text">Загрузить изображение</span>
            <span className="upload-icon">
              <img src="/images/Галерея.svg" alt="Галерея" className="upload-icon-svg" />
            </span>
          </button>
          
          <button className="literature-button" onClick={handleReferenceLiterature}>
            <span className="literature-text">Справочная литература</span>
            <span className="literature-icon">
              <img src="/images/Документы.svg" alt="Документы" className="literature-icon-head-svg" />
            </span>
          </button>
        </div>
      </div>
    </div>
  );
};

// Компонент страницы загрузки
const LoadingPage = ({ onNavigate }) => {
  return (
    <div className="loading-page">
      <div className="loading-logo">
        <img src="/images/лого для загрузочного экрана здравскан.svg" alt="ЗдравСкан" className="loading-logo-svg" />
      </div>
    </div>
  );
};

// Компонент страницы загрузки изображения
const UploadPage = ({ onNavigate }) => {
  const [selectedImage, setSelectedImage] = useState(null);

  const handleFileSelect = (event) => {
    const file = event.target.files[0];
    if (file) {
      const imageUrl = URL.createObjectURL(file);
      setSelectedImage(imageUrl);
    }
  };

  const handleTakePhoto = () => {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = 'image/*';
    input.capture = 'environment';
    input.onchange = handleFileSelect;
    input.click();
  };

  const handleScan = () => {
    if (selectedImage) {
      onNavigate('loading');
      // Имитация загрузки с возможностью ошибки
      setTimeout(() => {
        // Случайная ошибка для демонстрации
        const shouldError = Math.random() < 0.3; // 30% вероятность ошибки
        if (shouldError) {
          onNavigate('error');
        } else {
          onNavigate('scanner', { image: selectedImage });
        }
      }, 2000);
    }
  };

  return (
    <div className="upload-page">
      
      {!selectedImage ? (
        <div className="upload-options">
          <button className="upload-option" onClick={handleTakePhoto}>
            <div className="upload-icon-large">📷</div>
            <span>Сделать фото</span>
          </button>
          <button className="upload-option" onClick={() => document.getElementById('file-input').click()}>
            <div className="upload-icon-large">📁</div>
            <span>Выбрать из галереи</span>
          </button>
          <input
            id="file-input"
            type="file"
            accept="image/*"
            onChange={handleFileSelect}
            style={{ display: 'none' }}
          />
        </div>
      ) : (
        <div className="image-preview">
          <img src={selectedImage} alt="Preview" className="preview-image" />
          <div className="scan-overlay">
            <div className="scan-frame"></div>
          </div>
          <button className="scan-button-large" onClick={handleScan}>
            <div className="scan-icon-large">
              <img src="/images/Лупа.svg" alt="Лупа" className="scan-icon-lupa-svg" />
            </div>
            <span>Сканировать</span>
          </button>
        </div>
      )}
      
      <button className="back-button" onClick={() => onNavigate('home')}>
        ← Назад
      </button>
    </div>
  );
};

// Компонент страницы сканера
const ScannerPage = ({ image, onNavigate }) => {
  const [analysisResult] = useState({
    condition: 'Укус слепня',
    description: 'В большинстве случаев укус слепня для человека неприятен, но не опасен. Однако при склонности к аллергии или множественных укусах нужно обязательно обратиться к врачу.',
    recommendations: [
      'Промойте место укуса холодной водой',
      'Приложите лед для уменьшения отека',
      'Используйте антигистаминные препараты при аллергии',
      'Обратитесь к врачу при сильной реакции'
    ]
  });

  return (
    <div className="scanner-page">
      
      {/* Логотип */}
      <div className="scanner-logo">
        <img src="/images/Мини  лого здравскан синий для страницы сканера.svg" alt="ЗдравСкан" className="scanner-logo-svg" />
      </div>
      
      {/* Изображение с результатом */}
      <div className="image-analysis">
        <div className="image-container">
          <img src={image} alt="Analyzed" className="analysis-image" />
          <div className="scan-overlay">
            <img src="/images/Рамки сканера.svg" alt="Рамка сканера" className="scan-frame-svg" />
          </div>
        </div>
        
        <div className="analysis-result">
          <div className="result-label">на изображении</div>
          <div className="result-condition">{analysisResult.condition}</div>
          <div className="result-description">{analysisResult.description}</div>
          
          <div className="recommendations">
            <h3>Рекомендации:</h3>
            <ul>
              {analysisResult.recommendations.map((rec, index) => (
                <li key={index}>{rec}</li>
              ))}
            </ul>
          </div>
        </div>
      </div>
      
      {/* Навигация */}
      <div className="scanner-navigation">
        <button className="nav-button" onClick={() => onNavigate('upload')}>
          ←
        </button>
        <button className="nav-button home" onClick={() => onNavigate('home')}>
          <div className="home-icon">🏠</div>
        </button>
        <button className="nav-button scan" onClick={() => onNavigate('upload')}>
          <img src="/images/Кнопка задравскан постояянная вниз.svg" alt="ЗдравСкан" className="nav-scan-svg" />
        </button>
      </div>
    </div>
  );
};

// Компонент страницы справочной литературы
const LiteraturePage = ({ onNavigate }) => {
  const [literatureItems] = useState([
    {
      id: 1,
      title: 'Справочник по клинической офтальмологии',
      icon: '/images/Документы.svg'
    },
    {
      id: 2,
      title: 'Инсектная аллергия: диагностика и лечение',
      icon: '/images/Документы.svg'
    },
    {
      id: 3,
      title: 'Практическое руководство по неотложной помощи при укусах насекомых',
      icon: '/images/Документы.svg'
    },
    {
      id: 4,
      title: 'Кариес зубов: современные методы диагностики',
      icon: '/images/Документы.svg'
    },
    {
      id: 5,
      title: 'Аллергология и иммунология',
      icon: '/images/Документы.svg'
    }
  ]);

  const handleLiteratureClick = (item) => {
    console.log('Открыть литературу:', item.title);
    // Здесь можно добавить логику для открытия конкретной литературы
  };

  return (
    <div className="literature-page">
      <div className="literature-header">
        <h1>Справочная литература</h1>
      </div>
      
      <div className="literature-list">
        {literatureItems.map((item) => (
          <button
            key={item.id}
            className="literature-item"
            onClick={() => handleLiteratureClick(item)}
          >
            <span className="literature-item-icon">
              <img src={item.icon} alt="Документ" className="literature-icon-svg" />
            </span>
            <span className="literature-item-title">{item.title}</span>
          </button>
        ))}
      </div>
      
      {/* Навигация */}
      <div className="scanner-navigation">
        <button className="nav-button" onClick={() => onNavigate('home')}>
          ←
        </button>
        <button className="nav-button home" onClick={() => onNavigate('home')}>
          🏠
        </button>
        <button className="nav-button scan" onClick={() => onNavigate('upload')}>
          <img src="/images/Кнопка задравскан постояянная вниз.svg" alt="ЗдравСкан" className="nav-scan-svg" />
        </button>
      </div>
    </div>
  );
};

// Компонент страницы подписки
const SubscriptionPage = ({ onNavigate }) => {
  const [selectedPlan, setSelectedPlan] = useState('express');

  const handleTrialSubscribe = () => {
    console.log('Подписка на пробный период');
    // Здесь будет логика для оформления пробной подписки
  };

  const handleSubscribe = () => {
    console.log('Оформление подписки:', selectedPlan);
    // Здесь будет логика для оформления платной подписки
  };

  return (
    <div className="subscription-page">
      {/* Заголовок */}
      <div className="subscription-header">
        <h1>Подписка на</h1>
        <div className="subscription-app-name">ЗдравСкан</div>
      </div>

      {/* Пробный период */}
      <div className="trial-section">
        <h2>Хотите убедиться в эффективности ЗдравСкан лично?</h2>
        <div className="trial-highlight">попробуй 7 дней БЕСПЛАТНО</div>
        <p className="trial-description">
          Полный доступ ко всем функциям приложения. Автоматически не продлевается. 
          Для продолжения использования требуется платная подписка.
        </p>
        <button className="trial-button" onClick={handleTrialSubscribe}>
          подписаться на пробный период
        </button>
      </div>

      {/* Платные планы */}
      <div className="plans-section">
        <div className="plan-options">
          <label className="plan-option">
            <input
              type="radio"
              name="plan"
              value="express"
              checked={selectedPlan === 'express'}
              onChange={(e) => setSelectedPlan(e.target.value)}
            />
            <div className="plan-content">
              <div className="plan-name">Экспресс-проверка</div>
              <div className="plan-duration">(подписка на 1 месяц)</div>
              <div className="plan-price">229₽</div>
            </div>
          </label>

          <label className="plan-option">
            <input
              type="radio"
              name="plan"
              value="quarter"
              checked={selectedPlan === 'quarter'}
              onChange={(e) => setSelectedPlan(e.target.value)}
            />
            <div className="plan-content">
              <div className="plan-name">Триместр здоровья</div>
              <div className="plan-duration">(подписка на 3 месяца)</div>
              <div className="plan-price">749₽</div>
            </div>
          </label>

          <label className="plan-option">
            <input
              type="radio"
              name="plan"
              value="annual"
              checked={selectedPlan === 'annual'}
              onChange={(e) => setSelectedPlan(e.target.value)}
            />
            <div className="plan-content">
              <div className="plan-name">Годовой иммунитет</div>
              <div className="plan-duration">(подписка на 12 месяцев)</div>
              <div className="plan-price">2499₽</div>
            </div>
          </label>
        </div>

        <div className="legal-text">
          Подписываясь, вы соглашаетесь с условиями использования. 
          Подписка автоматически продлевается. Оплата производится через 
          App Store/Google Play. Данные обрабатываются в соответствии с 
          политикой конфиденциальности.
        </div>

        <button className="subscribe-button-large" onClick={handleSubscribe}>
          оформить подписку
        </button>
      </div>

      {/* Навигация */}
      <div className="scanner-navigation">
        <button className="nav-button" onClick={() => onNavigate('home')}>
          ←
        </button>
        <button className="nav-button home" onClick={() => onNavigate('home')}>
          🏠
        </button>
        <button className="nav-button scan" onClick={() => onNavigate('upload')}>
          <img src="/images/Кнопка задравскан постояянная вниз.svg" alt="ЗдравСкан" className="nav-scan-svg" />
        </button>
      </div>
    </div>
  );
};

// Компонент страницы с сообщением о подписке
const SubscriptionPromptPage = ({ onNavigate }) => {
  const handleSubscribe = () => {
    onNavigate('subscription');
  };

  return (
    <div className="subscription-prompt-page">
      <div className="prompt-content">
        <div className="prompt-text">
          <div className="prompt-line">Пссс......</div>
          <div className="prompt-line">кажется у тебя нет</div>
          <div className="prompt-line highlight">подписки :(</div>
        </div>
        
        <div className="prompt-description">
          Что бы продолжить пользоваться <span className="highlight">ЗдравСканом</span> сначала оформи подписку или пробный период.
        </div>
        
        <button className="prompt-subscribe-button" onClick={handleSubscribe}>
          <span>Оформить подписку</span>
          <span className="card-icon">💳</span>
        </button>
      </div>
      
      {/* Навигация */}
      <div className="scanner-navigation">
        <button className="nav-button" onClick={() => onNavigate('home')}>
          ←
        </button>
        <button className="nav-button home" onClick={() => onNavigate('home')}>
          🏠
        </button>
        <button className="nav-button scan" onClick={() => onNavigate('upload')}>
          <img src="/images/Кнопка задравскан постояянная вниз.svg" alt="ЗдравСкан" className="nav-scan-svg" />
        </button>
      </div>
    </div>
  );
};

// Компонент страницы ошибки
const ErrorPage = ({ onNavigate }) => {
  return (
    <div className="error-page">
      <div className="error-content">
        <h1 className="error-title">Что-то пошло не так...</h1>
        <p className="error-message">
          Сервис не работает на данный момент, попробуйте позже пожалуйста.
        </p>
      </div>
      
      <button className="back-button error-back" onClick={() => onNavigate('home')}>
        ←
      </button>
    </div>
  );
};

// Главный компонент приложения
const ZdravScanApp = () => {
  const [currentPage, setCurrentPage] = useState('home');
  const [pageData, setPageData] = useState({});

  const handleNavigate = (page, data = {}) => {
    setCurrentPage(page);
    setPageData(data);
  };

  const renderPage = () => {
    switch (currentPage) {
      case 'home':
        return <HomePage onNavigate={handleNavigate} />;
      case 'loading':
        return <LoadingPage onNavigate={handleNavigate} />;
      case 'upload':
        return <UploadPage onNavigate={handleNavigate} />;
      case 'scanner':
        return <ScannerPage image={pageData.image} onNavigate={handleNavigate} />;
      case 'literature':
        return <LiteraturePage onNavigate={handleNavigate} />;
      case 'subscription':
        return <SubscriptionPage onNavigate={handleNavigate} />;
      case 'subscription-prompt':
        return <SubscriptionPromptPage onNavigate={handleNavigate} />;
      case 'error':
        return <ErrorPage onNavigate={handleNavigate} />;
      default:
        return <HomePage onNavigate={handleNavigate} />;
    }
  };

  return (
    <div className="app-container">
      {renderPage()}
    </div>
  );
};

export default ZdravScanApp;
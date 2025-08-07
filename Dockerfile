# Dockerfile
FROM node:18-alpine

# Устанавливаем рабочую директорию
WORKDIR /opt/build

# Копируем package.json и package-lock.json (если есть) из папки frontend
COPY frontend/package.json .

# Устанавливаем зависимости
RUN npm --prefix frontend install

# Копируем весь код из frontend
COPY frontend/. .

# Собираем проект
RUN npm run build

# Указываем, что статика в папке build (как ожидает Timeweb)
# Timeweb ищет статику в /app/build
# API/Dockerfile
FROM python:3.11-slim

# Переходим сразу в /app/API
WORKDIR /app/API

# Копируем только то, что нужно
COPY API/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь код API в /app/API
COPY API/ .

# Копируем конфиг для доступа к переменным окружения
COPY config.py .

# Открываем на порту 8000
EXPOSE 8000

# Запускаем из текущей рабочей директории модуль api
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]

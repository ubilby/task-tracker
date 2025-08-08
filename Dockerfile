# Используем официальный образ Python версии 3.10.12
FROM python:3.13.5-slim

# Создаем рабочую директорию внутри контейнера
WORKDIR /app

# Теперь копируем все файлы проекта
COPY . .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Указываем команду для запуска main.py
CMD ["python", "main.py"]

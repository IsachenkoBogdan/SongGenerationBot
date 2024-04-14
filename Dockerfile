FROM python:3.9

# Установка рабочей директории в контейнере
WORKDIR /app

# Копирование файла с зависимостями и установка зависимостей
COPY requirements.txt .
RUN pip install -r requirements.txt

# Копирование всего проекта в контейнер
COPY . .
# Копирование файла secrets.toml в обе возможные директории
COPY .streamlit/secrets.toml /root/.streamlit/secrets.toml


# Выставление прав для исполнения скрипта
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Открытие портов для Streamlit и Telegram (если требуется)
EXPOSE 8501

# Задание entrypoint скрипта
ENTRYPOINT ["/entrypoint.sh"]



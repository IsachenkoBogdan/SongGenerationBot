#!/bin/bash

# Запуск Streamlit веб-приложения
streamlit run app_modules/streamlit_app.py &

# Запуск Telegram бота
cd bot
export PYTHONPATH="${PYTHONPATH}:/app"
python main.py

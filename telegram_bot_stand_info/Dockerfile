FROM python:3.11-slim

WORKDIR /bot

COPY telegram_bot_stand_info/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY telegram_bot_stand_info/ .

COPY config.py .

CMD ["python", "bot_run.py"]
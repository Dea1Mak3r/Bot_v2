FROM python:3.11-slim

WORKDIR /app

COPY web_interface/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY web_interface/ .

COPY config.py .

EXPOSE 8502

CMD ["streamlit", "run", "frontend.py", "--server.port=8502"]
FROM python:3.9-slim-bullseye

WORKDIR /app

RUN apt-get update && apt-get install -y gnupg2 curl

RUN apt-get update \
    && apt-get -y install gcc \
    && apt-get -y install g++ \
    && apt-get -y install unixodbc unixodbc-dev \
    && apt-get clean 

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.enableCORS=false"]

FROM python:3.10-slim

RUN apt-get update && apt-get install -y ffmpeg git build-essential

WORKDIR /app
COPY . .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "app.py"]

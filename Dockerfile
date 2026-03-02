FROM python:3.11-slim

RUN apt-get update && apt-get install -y ffmpeg git

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "app.py"]

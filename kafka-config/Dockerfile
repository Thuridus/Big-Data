FROM python:3
WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY kafka_subscriber.py ./
CMD ["python", "-u", "./kafka_subscriber.py"]
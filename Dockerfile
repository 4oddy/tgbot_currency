FROM python:3.10.4-slim-buster

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

CMD ["python", "main.py"]
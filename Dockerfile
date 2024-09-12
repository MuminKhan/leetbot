FROM python:3.12

WORKDIR /app
COPY requirements.txt .
COPY ./leetbot .

RUN pip install -r requirements.txt

CMD ["python", "leetbot/main.py"]

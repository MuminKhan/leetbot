FROM python:3.12

WORKDIR /app
COPY requirements.txt .
COPY ./leetbot .

RUN pip install -r requirements.txt

EXPOSE 5000
CMD ["python", "leetbot/main.py"]
 
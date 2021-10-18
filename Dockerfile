FROM python:3.8-alpine
WORKDIR /src
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY ./leetbot /src
EXPOSE 5000
CMD python leetbot/main.py
 
FROM python:3.8

COPY . .

RUN pip install -r requirements.txt
RUN mkdir videos
RUN mkdir videogif


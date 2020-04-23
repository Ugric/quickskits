FROM python:3.8

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

RUN mkdir videos
RUN mkdir videogif
RUN mkdir temp

CMD python quickskits.py

FROM python:alpine3.20

RUN mkdir /app && \
    mkdir /app/ssl

COPY . /app

RUN cd /app/ \ 
    && apk add build-base libffi-dev \ 
    && pip install -r requirements.txt \
    && chmod +x aliyun-cdn-ssl.py \ 
    && cp ./aliyun-cdn-ssl.py /etc/periodic/daily/
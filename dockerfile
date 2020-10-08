FROM tiangolo/uwsgi-nginx-flask:python3.6-alpine3.7

RUN apk update 
# && apk add gcc libc-dev make libffi-dev openssl-dev python3-dev libxml2-dev libxslt-dev 

WORKDIR /app

COPY ./backend /app

COPY requirements.txt ./

# RUN pip install --no-cache-dir -U pip wheel setuptools 

# RUN pip install --no-cache-dir -r requirements.txt







FROM alpine:3.7

RUN apk add --no-cache --virtual .build-deps g++ python3-dev libffi-dev jpeg-dev zlib-dev bash postgresql-dev postgresql-client && \
    apk add --no-cache --update python3 && \
    pip3 install --upgrade pip setuptools
ADD . /src/backend/

RUN chmod 777 -R /src/backend/
RUN pip install Pillow
RUN cd /src/backend/ && pip3 install -r requirements
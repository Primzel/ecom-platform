FROM alpine:3.7

RUN apk add --no-cache --virtual .build-deps g++ python3-dev libffi-dev openssl-dev jpeg-dev zlib-dev bash && \
    apk add --no-cache --update python3 && \
    pip3 install --upgrade pip setuptools
ADD . /src/backend/

RUN chmod 777 -R /src/backend/
RUN pip install Pillow
RUN cd /src/backend/ && pip3 install -r requirements && python3 manage.py migrate && python3 manage.py collectstatic --noinput
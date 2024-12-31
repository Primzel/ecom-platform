FROM python
RUN apt update && apt install -y g++ python3-dev libffi-dev libjpeg-dev zlib1g-dev bash postgresql-client

ADD . /src/backend/
WORKDIR /src/backend/
RUN chmod -R 777 /src/backend/
RUN pip install Pillow legacy-cgi
RUN cd /src/backend/ && pip3 install -r requirements

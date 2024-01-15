FROM python
RUN apt-get update
RUN apt install -y g++ python3-dev libffi-dev libjpeg-dev zlib1g-dev bash postgresql-client
ADD . /src/backend/

RUN chmod 777 -R /src/backend/
RUN pip install Pillow
RUN cd /src/backend/ && pip3 install -r requirements
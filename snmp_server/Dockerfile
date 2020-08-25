FROM python:3.8.5-alpine3.12

LABEL maintaner="Peng Xiao <xiaoquwl@gmail.com>"

COPY . /app
WORKDIR /app

RUN apk add --no-cache gcc libressl-dev musl-dev libffi-dev openssl-dev python3-dev alpine-sdk autoconf automake libtool&& \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    apk del gcc libressl-dev musl-dev libffi-dev openssl-dev python3-dev alpine-sdk autoconf automake libtool


EXPOSE 161/udp

CMD ["python", "snmp_server.py"]

FROM python:3.8.6-slim

LABEL maintaner="Peng Xiao <xiaoquwl@gmail.com>"

COPY . /app
WORKDIR /app

RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt


EXPOSE 161/udp

CMD ["python", "snmp_server.py"]

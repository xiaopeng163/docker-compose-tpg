#!/bin/bash

# pull image
docker pull telegraf:latest
docker pull prom/prometheus:latest
docker pull grafana/grafana

# build image
cd snmp_simulator
docker build -t snmp_simulator .

cd ..

# start
export COMPOSE_PROJECT_NAME=demo
docker-compose up -d
docker-compose ps

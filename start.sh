#!/bin/bash

# pull image
docker pull telegraf:latest
docker pull prom/prometheus:latest
docker pull grafana/grafana

# build image
docker build -t snmp_simulator snmp_simulator/
docker build -t json_exporter json_exporter/


# start
export COMPOSE_PROJECT_NAME=demo
docker-compose up -d
docker-compose ps

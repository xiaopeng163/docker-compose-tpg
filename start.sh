#!/bin/bash

# pull image
docker pull telegraf:latest
docker pull prom/prometheus:latest
docker pull grafana/grafana

# build image
docker build -t snmp_simulator -f snmp_simulator/Dockerfile
docker build -t json_exporter -f json_exporter/Dockerfile


# start
export COMPOSE_PROJECT_NAME=demo
docker-compose up -d
docker-compose ps

#!/bin/bash

export COMPOSE_PROJECT_NAME=demo
docker-compose stop
docker-compose rm -f

# clean
while true; do
    read -p "Do you want to cleanup all containers and volumes?" yn
    case $yn in
    [Yy]*)
        docker system prune -f
        docker volume rm $(docker volume ls -q)
        break
        ;;
    [Nn]*) exit ;;
    *) echo "Please answer yes or no." ;;
    esac
done

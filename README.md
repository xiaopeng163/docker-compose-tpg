# Telegraf + Prometheus + Grafana Local Testing Environments

Setup learning environment for Telegraf, Prometheus and Grafana with docker-compose. (include SNMP simulators)

## Requirements

`docker` and `docker-compose` installed.

```
$ docker version
Client: Docker Engine - Community
 Version:           19.03.13
 API version:       1.40
 Go version:        go1.13.15
 Git commit:        4484c46d9d
 Built:             Wed Sep 16 17:02:52 2020
 OS/Arch:           linux/amd64
 Experimental:      false

Server: Docker Engine - Community
 Engine:
  Version:          19.03.13
  API version:      1.40 (minimum version 1.12)
  Go version:       go1.13.15
  Git commit:       4484c46d9d
  Built:            Wed Sep 16 17:01:20 2020
  OS/Arch:          linux/amd64
  Experimental:     false
 containerd:
  Version:          1.3.7
  GitCommit:        8fba4e9a7d01810a393d5d25a3621dc101981175
 runc:
  Version:          1.0.0-rc10
  GitCommit:        dc9208a3303feef5b3839f4323d9beb36df0a9dd
 docker-init:
  Version:          0.18.0
  GitCommit:        fec3683
$ docker compose --version
Docker version 19.03.13, build 4484c46d9d
$
```

## Quick Start

```shell
./start.sh
```

### Grafana

http://127.0.0.1:3000 username:password admin:admin

### Scaling

```shell
$ export COMPOSE_PROJECT_NAME=demo
$ docker-compose up -d --scale cisco_router=3 --scale palo_alto=3
grafana is up-to-date
telegraf is up-to-date
prometheus is up-to-date
Creating demo_cisco_router_2 ... done
Creating demo_cisco_router_3 ... done
Creating demo_palo_alto_2    ... done
Creating demo_palo_alto_3    ... done
```

change telegraf cfg

`telegraf/telegraf.conf`

```
[[inputs.snmp]]
agents = [
    "demo_cisco_router_1:161",
    "demo_cisco_router_2:161",
    "demo_cisco_router_3:161",
    "demo_palo_alto_1:161",
    "demo_palo_alto_2:161",
    "demo_palo_alto_3:161"
]
```

restart telegraf

```shell
docker restart telegraf
```

## Stop and cleanup

```shell
./stop.sh
```

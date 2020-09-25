# Telegraf + Prometheus + Grafana Local Testing Environments

## Start

```shell
./start.sh
```

## Check Grafana

http://127.0.0.1:3000 username:password admin:admin (need change password after first login)

add data prometheus data source: http://prometheus:9090

## Import Dashboard

Copy json `/grafana/dashboard/cisco.json`

## Scaling

```shell
$ docker-compose up -d --scale cisco_router=5
telegraf is up-to-date
Starting github_cisco_router_1 ...
grafana is up-to-date
Creating github_cisco_router_2 ... done
Creating github_cisco_router_3 ... done
Creating github_cisco_router_4 ... done
Creating github_cisco_router_5 ... done
```

change telegraf cfg

`telegraf/telegraf.conf`

```
[[inputs.snmp]]
agents = [ "github_cisco_router_1:161","github_cisco_router_2:161","github_cisco_router_3:161","github_cisco_router_4:161","github_cisco_router_5:161" ]
```

restart telegraf

```shell
docker restart telegraf
```

## Stop

```shell
./stop.sh
```

# SNMP Test

Start

```
$ export COMPOSE_PROJECT_NAME=cisco
$ docker-compose build
$ docker-compose up -d --scale router=2
Starting telegraf       ... done
Starting prometheus     ... done
Starting grafana        ... done
Creating cisco_router_1 ... done
Creating cisco_router_2 ... done
```

check

```
$ docker-compose ps
     Name                   Command               State                          Ports
--------------------------------------------------------------------------------------------------------------
cisco_router_1   python snmp_server.py            Up      161/udp
cisco_router_2   python snmp_server.py            Up      161/udp
grafana          /run.sh                          Up      0.0.0.0:3000->3000/tcp
prometheus       /bin/prometheus --config.f ...   Up      0.0.0.0:9090->9090/tcp
telegraf         /entrypoint.sh telegraf -- ...   Up      8092/udp, 8094/tcp, 8125/udp, 0.0.0.0:9126->9126/tcp
```

check grafana

http://127.0.0.1:3000 username:password admin:admin (need change password after first login)

check prometheus

http://127.0.0.1:9090

Scaling

```
$ docker-compose up -d --scale router=5
cisco_snmp_client_1 is up-to-date
Starting cisco_router_1 ... done
Creating cisco_router_2 ... done
Creating cisco_router_3 ... done
Creating cisco_router_4 ... done
Creating cisco_router_5 ... done
```

change telegraf cfg

`telegraf/telegraf.conf`

```
[[inputs.snmp]]
agents = [ "cisco_router_1:161", "cisco_router_2:161", "cisco_router_3:161", "cisco_router_4:161", "cisco_router_5:161" ]
version = 2
community = "public"
```

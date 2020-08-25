# SNMP Test

Start

```
$ export COMPOSE_PROJECT_NAME=cisco
$ docker-compose up -d
```

check

```
$ docker-compose ps
       Name                      Command               State    Ports
----------------------------------------------------------------------
cisco_router_1        python snmp_server.py            Up      161/udp
cisco_snmp_client_1   sh -c while true;do sleep  ...   Up
```

check snmp connection

```
$ docker-compose exec snmp_client sh
/omd # snmpget -v 2c -c public cisco_router_1 sysName.0
SNMPv2-MIB::sysName.0 = STRING: 5143a6a45148
/omd # exit
$
```

Scaling

```
$ docker-compose up -d --scale router=5
cisco_snmp_client_1 is up-to-date
Starting cisco_router_1 ... done
Creating cisco_router_2 ... done
Creating cisco_router_3 ... done
Creating cisco_router_4 ... done
Creating cisco_router_5 ... done
$ docker-compose ps
       Name                      Command               State    Ports
----------------------------------------------------------------------
cisco_router_1        python snmp_server.py            Up      161/udp
cisco_router_2        python snmp_server.py            Up      161/udp
cisco_router_3        python snmp_server.py            Up      161/udp
cisco_router_4        python snmp_server.py            Up      161/udp
cisco_router_5        python snmp_server.py            Up      161/udp
cisco_snmp_client_1   sh -c while true;do sleep  ...   Up
```

Check connection again (with different hostname)

```
$ docker-compose exec snmp_client sh
/omd # for i in `seq 5`; do snmpget -v 2c -c public cisco_router_$i sysName.0;done
SNMPv2-MIB::sysName.0 = STRING: 5143a6a45148
SNMPv2-MIB::sysName.0 = STRING: 74ecf3338abd
SNMPv2-MIB::sysName.0 = STRING: c0b31ebcf91e
SNMPv2-MIB::sysName.0 = STRING: d5d8cb8f1302
SNMPv2-MIB::sysName.0 = STRING: 9b31c3e16512
/omd #
```

#!/bin/bash

ports="3260 8000 6080 6081 8003 8004 3333 8773 8774 8775 9191 8776 3306 9292 111 80 4369 48402 22 "
for port in $ports
do
  iptables -A OUTPUT -p tcp --sport 3260 -j ACCEPT 
  iptables -A INPUT -p tcp --dport 3260 -j ACCEPT
done

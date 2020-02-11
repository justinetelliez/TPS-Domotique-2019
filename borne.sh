#!/bin/bash

### ce script est fait pour les pc de la I005 après une reinstalation d'ubuntu
### (à lancer en root)

### pour configurer le point d'accès cisco: lionenmajuscule 192.168.1.145

###############################

apt-get install iptables
apt-get install dnsmasq

###############################
## ajout d'une addresse ip pour l'interface sur laquelle on a branché le point d'accès (enp3s0)

ip a a 192.168.1.254/24 dev enp3s0 

###############################
## iptables

iptables -F INPUT	#suppression des anciennes règles
iptables -F FORWARD
iptables -F OUTPUT

iptables -t nat -A POSTROUTING -o eno1 -j MASQUERADE	# avec eno1 l'interface connectée à internet
iptables -A FORWARD -i enp3s0 -o eno1 -j ACCEPT
iptables -A FORWARD -i eno1 -o enp3s0 -m state --state RELATED,ESTABLISHED -j ACCEPT

# pour afficher les règles de la table : iptables -L --line-numbers
# seules les deux règles précédentes doivent être présentent

#####################################
## configuration /etc/dnsmasq.conf :

rm /etc/dnsmasq.conf # on supprime le fichier au cas où il y avait déjà une configuration

echo "interface=enp3s0\n" >> /etc/dnsmasq.conf
echo "dhcp-range=192.168.1.50,192.168.1.150,255.255.255.0,24h" >> /etc/dnsmasq.conf
echo "dhcp-option=3,192.168.1.254"  >> /etc/dnsmasq.conf 
echo "dhcp-option=6,192.168.1.254"  >> /etc/dnsmasq.conf

######################################
## on tue les processus utilisant dnsmasq

ps aux | grep dnsmasq | awk '{print $2}' >> tmp.txt 	# on récupère les pids et on les 
							# écrit dans un fichier temporaire
while read p; do
	kill -9 $p	# on tue les processus
done < tmp.txt

rm tmp.txt 
###################################
## on relance dnsmasq avec la nouvelle configuration

service dnsmasq restart

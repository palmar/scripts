#!/bin/bash 
# dig $line +short >> ip address 
# whois $line >> Lists full details including the name servers 
# whois $line | grep "Name Server" | cut -d ":" -f 2 | sed 's/ //' | 
while read domain 
do 
echo $domain
ipaddress=`dig $domain +short`
echo $ipaddress
nameserver=`dig $domain ns +short | sed -n 1p`
echo $nameserver
echo $domain,$ipaddress,$nameserver >> output.csv
done < domains.txt

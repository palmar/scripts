#!/bin/bash
STARTPAGE=13
ENDPAGE=18

for ((i=STARTPAGE; i<=ENDPAGE; i++));
do
	wget "http://www.teamliquid.net/forum/mafia/440546-golden-sun-the-lost-age-mafia-djinn-edition?page="$i
done;
echo
 

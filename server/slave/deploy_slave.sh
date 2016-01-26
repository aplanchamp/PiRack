#!/bin/bash
echo "Create /etc/slave folder"
ssh root@$1 mkdir /etc/slave
echo "Coppying configuration.ini to /etc/slave"
scp ./configuration.ini root@$1:/etc/slave/
echo "Copying slave makefile to /etc/slave"
scp ./slave/Makefile root@$1:/etc/slave/
echo "Copying slave librairy to /etc/slave"
scp ./slave/slave.c root@$1:/etc/slave/
echo "Copying slave executable to /etc/slave"
scp -r ./slave/src root@$1:/etc/slave/

echo "Make de l'executable"
ssh root@$1 'cd /etc/slave/ && make'
echo "Copying slave to /usr/local/sbin"
ssh root@$1 cp /etc/slave/slave /usr/local/sbin/

echo "Compresser le dossier scripts"
tar -zcvf ./slave/scripts.tar.gz ./slave/scripts

echo "Envoi du tar.gz dans les slaves"
scp ./slave/scripts.tar.gz root@$1:/etc/slave/

echo "Untar the tar.gz"
ssh root@$1 'cd /etc/slave/ && tar -zxvf scripts.tar.gz'

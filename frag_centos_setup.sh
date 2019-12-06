#!/bin/bash

yum clean all

echo '----------installing python----------'
sudo yum install -y https://centos7.iuscommunity.org/ius-release.rpm
sudo yum update
sudo yum install -y python36u python36u-libs python36u-devel python36u-pip

echo '----------installing Cython----------'
sudo python3.6 -m pip install Cython==0.23

echo '----------installing paramiko----------'
python3.6 -m pip install paramiko

echo '----------installing kivy----------'
python3.6 -m pip install pygame
python3.6 -m pip install kivy

echo '----------installing pymysql----------'
python3.6 -m pip install pymysql

echo '----------installing pycryptodome----------'
python3.6 -m pip install pycryptodome

echo '----------installing mysql-----------'
yum install mysql
wget http://repo.mysql.com/mysql-community-release-el7-5.noarch.rpm
sudo rpm -ivh mysql-community-release-el7-5.noarch.rpm
yum update
echo '**********RUN THESE COMMANDS IN ORDER***********'
echo 'remove mariadb-libs'
echo 'remove mariadb-community'
echo 'run'
echo 'exit'
echo '************************************************'
yum shell
sudo yum install mysql-server
sudo systemctl start mysqld
sudo mysql_secure_installation

echo '----------installing free radius----------'
yum install freeradius

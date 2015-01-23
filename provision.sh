#!/bin/bash

############################################################
# common
############################################################
sudo apt-get update -q
sudo apt-get install -q -y nginx supervisor uwsgi
sudo apt-get install -q -y vim make htop python-software-properties
sudo apt-get install -q -y python python-dev python-pip
sudo apt-get install -q -y build-essential python-setuptools python-dev apache2-utils uwsgi-plugin-python libjpeg8 libjpeg62-dev libfreetype6 libfreetype6-dev uwsgi-plugin-python
sudo apt-get install -q -y git-core libxml2-dev libxslt1-dev
sudo apt-get install -q -y nmap htop vim unzip
sudo easy_install pip
sudo pip install virtualenv virtualenvwrapper

VIRTUALENV_HOME=/var/apps

echo "export WORKON_HOME=$VIRTUALENV_HOME/.virtualenvs" >> $HOME/.bash_profile
echo "source /usr/local/bin/virtualenvwrapper.sh" >> $HOME/.bash_profile
source $HOME/.bash_profile
mkdir -p $WORKON_HOME


############################################################
# redis
############################################################
if [ ! -e "/etc/apt/sources.list.d/redis.list" ] ; then
    sudo sh -c 'echo "deb http://ppa.launchpad.net/chris-lea/redis-server/ubuntu precise main\ndeb-src http://ppa.launchpad.net/chris-lea/redis-server/ubuntu precise main " >> /etc/apt/sources.list.d/redis.list'
    sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys C7917B12
    sudo apt-get update -q
fi

sudo apt-get install -q -y redis-server

sudo sed -i 's/^bind 127.0.0.1/#bind 127.0.0.1/g' /etc/redis/redis.conf
sudo service redis-server restart

exit

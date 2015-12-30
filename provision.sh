#!/bin/bash

############################################################
# common
############################################################
sudo apt-get update -q
sudo apt-get install -q -y vim make htop python-software-properties
sudo apt-get install -q -y python python-dev python-pip
sudo apt-get install -q -y build-essential python-setuptools python-dev apache2-utils uwsgi-plugin-python libjpeg8 libjpeg62-dev libfreetype6 libfreetype6-dev uwsgi-plugin-python
sudo apt-get install -q -y git-core libxml2-dev libxslt1-dev
sudo apt-get install -q -y nmap htop vim unzip
sudo apt-get install -q -y nginx-extras supervisor uwsgi
sudo apt-get install -q -y ffmpeg libav-tools libavcodec-extra-53
sudo easy_install pip
sudo pip install virtualenv virtualenvwrapper

AS_USER=$USER
#AS_USER=vagrant
AS_USER_HOME=$HOME
#AS_USER_HOME=/home/vagrant

APPS_HOME=/var/apps
VIRTUALENV_HOME=$APPS_HOME

if ! grep -q "export WORKON_HOME=$VIRTUALENV_HOME/.virtualenvs" "$AS_USER_HOME/.bash_profile" ; then
  echo "export WORKON_HOME=$VIRTUALENV_HOME/.virtualenvs" >> $AS_USER_HOME/.bash_profile
fi
if ! grep -q "source /usr/local/bin/virtualenvwrapper.sh" "$AS_USER_HOME/.bash_profile" ; then
  echo "source /usr/local/bin/virtualenvwrapper.sh" >> $AS_USER_HOME/.bash_profile
fi

sudo chown -R $AS_USER:$AS_USER $AS_USER_HOME/.bash_profile
source $AS_USER_HOME/.bash_profile
mkdir -p $WORKON_HOME

sudo mkdir -p $APPS_HOME
sudo mkdir -p $APPS_HOME/chute-client/versions/
sudo mkdir -p $APPS_HOME/chute-client/media/

sudo chown -R $AS_USER:$AS_USER $APPS_HOME

ln -s $APPS_HOME/chute-client/versions/chute-client $APPS_HOME/chute-client/chute-client

mkvirtualenv chute-client
workon chute-client
pip install -r $APPS_HOME/chute-client/chute-client/requirements.txt

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

# Copy the configs for nginx supervisor & uwsgi
sudo cp $AS_USER_HOME/conf/chute-client-hosts /etc/hosts
sudo cp $AS_USER_HOME/conf/chute-client /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default

sudo cp $AS_USER_HOME/conf/chute-client.conf /etc/supervisor/conf.d/chute-client.conf
sudo cp $AS_USER_HOME/conf/chute-client-worker.conf /etc/supervisor/conf.d/chute-client-worker.conf
sudo cp $AS_USER_HOME/conf/chute-client.ini /etc/uwsgi/apps-enabled/chute-client.ini

sudo service redis-server restart
sudo service nginx restart
#sudo service supervisor restart
sudo supervisorctl restart all

cd $APPS_HOME/chute-client/chute-client
python manage.py register -p 41061info
python manage.py update_playlist
exit

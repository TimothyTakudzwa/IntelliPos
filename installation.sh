#!bin/bash
echo -n "******************************************************************************************"
echo -n "Updating System Packages"
echo -n "******************************************************************************************"
sudo yum -y update
sudo yum -y install yum-utils
sudo yum -y groupinstall development
sudo yum install gcc openssl-devel bzip2-devel libffi-devel
#Get and Instal Python 3.8
echo -n "******************************************************************************************"
echo -n "Installing Python"
echo -n "******************************************************************************************"
sudo yum -y install wget
cd /opt && sudo wget https://www.python.org/ftp/python/3.8.7/Python-3.8.7.tgz
sudo tar xzf Python-3.8.7.tgz
cd Python-3.8.7
sudo ./configure --enable-optimizations
sudo make altinstall
sudo rm -f /opt/Python-3.8.7.tgz
PATH=$PATH:/usr/local/bin
echo -n "******************************************************************************************"
echo -n "Installing Virtual Environment"
echo -n "******************************************************************************************"
#Install Virtual Env
pip3 install virtualenv
VENV=/home/intellipos/IntelliPos/venv
virtualenv -p /usr/local/bin/python3.8 $VENV
source $VENV/bin/activate
#Install Application Requirements
echo -n "******************************************************************************************"
echo -n "Installing Application Requirements"
echo -n "******************************************************************************************"
pip3 install -r requirements.txt

#!bin/bash
echo -e "******************************************************************************************\n\n"
echo -e "Updating System Packages"
echo -e "\n\n******************************************************************************************"
sudo yum -y update
sudo yum -y install yum-utils
sudo yum -y groupinstall development
sudo yum install gcc openssl-devel bzip2-devel libffi-devel
#Get and Instal Python 3.8
echo -e "******************************************************************************************\n\n"
echo -e "\n\nInstalling Python"
echo -e "******************************************************************************************"
sudo yum -y install wget
cd /opt && sudo wget https://www.python.org/ftp/python/3.8.7/Python-3.8.7.tgz
sudo tar xzf Python-3.8.7.tgz
cd Python-3.8.7
sudo ./configure --enable-optimizations
sudo make altinstall
sudo rm -f /opt/Python-3.8.7.tgz
PATH=$PATH:/usr/local/bin
echo -e "******************************************************************************************\n\n"
echo -e "\n\nInstalling Virtual Environment"
echo -e "******************************************************************************************"
#Install Virtual Env
pip3 install virtualenv
VENV=/home/intellipos/IntelliPos/venv
virtualenv -p /usr/local/bin/python3.8 $VENV
source $VENV/bin/activate
#Install Application Requirements
echo -e "******************************************************************************************\n\n"
echo -e "Installing Application Requirements\n\n"
echo -e "\n\n******************************************************************************************"
cd /home/intellipos/IntelliPos/ && pip3 install -r requirements.txt

#!bin/bash
echo -e "******************************************************************************************\n\n"
echo -e "Updating System Packages"
echo -e "\n\n******************************************************************************************"
sudo yum -y update
sudo yum -y install yum-utils
sudo yum -y groupinstall development
sudo yum install gcc openssl-devel bzip2-devel libffi-devel
echo -e "******************************************************************************************\n\n"
echo -e "Installing Supervisor"
echo -e "\n\n******************************************************************************************"
sudo yum -y install supervisor
sudo systemctl start supervisord
sudo systemctl enable supervisord
echo -e "******************************************************************************************\n\n"
echo -e "Installing Nginx"
echo -e "\n\n******************************************************************************************"
sudo yum -y install nginx
sudo systemctl start nginx
sudo systemctl enable nginx
#Get and Instal Python 3.8
echo -e "******************************************************************************************\n\n"
echo -e "Installing Python"
echo -e "\n\n******************************************************************************************"
sudo yum -y install wget
cd /opt && sudo wget https://www.python.org/ftp/python/3.8.7/Python-3.8.7.tgz
sudo tar xzf Python-3.8.7.tgz
cd Python-3.8.7
sudo ./configure --enable-optimizations
sudo make altinstall
sudo rm -f /opt/Python-3.8.7.tgz
PATH=$PATH:/usr/local/bin
echo -e "******************************************************************************************\n\n"
echo -e "Installing Virtual Environment"
echo -e "\n\n******************************************************************************************"
#Install Virtual Env
sudo pip3 install virtualenv
VENV=/home/intellipos/IntelliPos/venv
virtualenv -p /usr/local/bin/python3.8 $VENV --reset-app-data
source $VENV/bin/activate
#Install Application Requirements
echo -e "******************************************************************************************\n\n"
echo -e "Installing Application Requirements\n\n"
echo -e "\n\n******************************************************************************************"
cd /home/intellipos/IntelliPos/ && pip3 install -r requirements.txt
sudo mkdir /var/log/intellipos/
echo -e "******************************************************************************************\n\n"
echo -e "Creating Log Files \n\n"
echo -e "\n\n******************************************************************************************"
touch /var/log/intellipos/access.log
touch /var/log/intellipos/error.log

#!/bin/bash



echo "Mr Sheep's requirements"


echo "On the installation, you would be asked your password and to type -y"

sleep 3

sudo apt-get install libxss1 libappindicator1 libindicator7 xvfb unzip

wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb

sudo dpkg -i google-chrome*.deb
sudo apt-get install -f

wget -N http://chromedriver.storage.googleapis.com/2.29/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
chmod +x chromedriver

sudo mv -f chromedriver /usr/local/share/chromedriver
sudo ln -s /usr/local/share/chromedriver /usr/local/bin/chromedriver
sudo ln -s /usr/local/share/chromedriver /usr/bin/chromedriver

sudo apt-get install python3-pip

sudo pip3 install pyvirtualdisplay selenium












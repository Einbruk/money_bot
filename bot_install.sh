#!/bin/bash

apt update && apt upgrade
apt install python3.11
apt install pip
pip3 install pyTelegramBotAPI
cp -r /usr/local/lib/python3.10/dist-packages /usr/local/lib/python3.11/
apt install git
cd /home
git clone https://github.com/Einbruk/money_bot
cd /home/money_bot
python3.11 main.py &
cd /

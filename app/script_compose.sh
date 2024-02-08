#!/bin/bash
sudo apt update
cd app/
sudo apt install -y python3-pip
sudo pip install --no-cache-dir -r requirements.txt
sudo docker-compose build
sudo docker-compose up -d --always
sudo docker-compose up -d --always
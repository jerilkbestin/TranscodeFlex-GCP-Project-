#!/bin/bash

# Install Python3 and pip3
sudo apt update
sudo apt install -y python3 python3-pip

# Install Python dependencies
pip3 install -r requirements.txt

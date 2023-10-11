#!/bin/bash

while true; do
    autossh -M 0 -f -N -L 65432:localhost:5432 -i ~/.ssh/id_rsa rootR@194.135.22.213 -o "ServerAliveInterval 30" -o "ServerAliveCountMax 3"
    echo "Туннель разорван. Переустановка..."
    sleep 5
done

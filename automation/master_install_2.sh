#!/usr/bin/env bash

# Install a pod network add-on (To allow the pods communicating with each others)
echo "Install flannel"
sudo kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/bc79dd1505b0c8681ece4de4c0d86c5cd2643275/Documentation/kube-flannel.yml

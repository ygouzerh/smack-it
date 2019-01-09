#!/usr/bin/env bash

#Initialize the master
echo "Initialize the master"
sudo kubeadm init --config kadmconf_mas.yml

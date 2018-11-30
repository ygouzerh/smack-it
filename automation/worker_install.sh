#!/usr/bin/env bash

#Initialize the worker
sudo hostnamectl set-hostname $(curl -s http://169.254.169.254/latest/meta-data/local-hostname)
sudo swapoff -a
sudo apt-get update && apt-get install -y apt-transport-https curl
sudo curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -
sudo cat <<EOF >/etc/apt/sources.list.d/kubernetes.list
deb https://apt.kubernetes.io/ kubernetes-xenial main
EOF
sudo apt-get update
sudo apt-get install -y kubelet kubeadm docker.io
sudo apt-mark hold kubelet kubeadm docker.io

# After the command sudo kubeadm init --config kadmconfig_mas.yml has finished, join the worker to the master
sudo kubeadm join --config kadmconf_wor.yml

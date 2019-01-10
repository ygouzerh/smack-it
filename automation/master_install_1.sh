#!/usr/bin/env bash

# WARNING : DO NOT EXECUTE THIS FILE IN SUDO.
# Because sudo $(sudo chown $(id -u):$(id -g)) != sudo chown $(id -u):$(id -g)

#To make kubectl work for your non-root user, run these commands, which are also part of the kubeadm init output:
echo "Make kubectl work for your non-root user"
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config

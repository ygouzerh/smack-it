#!/usr/bin/env bash


# NOT FINISHED YET
# To be executed on the master or inside a pod (replicat)
# What if the driver falls down

# Configure spark role
kubectl create serviceaccount spark
kubectl create clusterrolebinding spark-role --clusterrole=edit --serviceaccount=default:spark --namespace=default


# install jsk and spark
sudo apt install -y openjdk-8-jdk
wget http://mirrors.standaloneinstaller.com/apache/spark/spark-2.4.0/spark-2.4.0-bin-hadoop2.7.tgz
tar -xvzf spark-2.4.0-bin-hadoop2.7.tgz
rm spark-2.4.0-bin-hadoop2.7.tgz

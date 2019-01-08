#!/usr/bin/env bash

# the order should be respected, we can do a for f in file1 file2 ...

sudo kubectl apply -f zookeeper-service.yml
sudo kubectl apply -f zookeeper-service-headless.yml
sudo kubectl apply -f zookeeper-statefulset.yml

sleep 30

sudo kubectl apply -f kafka-service.yml
sudo kubectl apply -f kafka-service-headless.yml
sudo kubectl apply -f kafka-statefulset.yml


# Create the topics, one for each country (see kakfa best practices (design-patterns ...))
# Wait until the pod kafka-0 if ready (should be taking into account TODO)
sudo kubectl exec kafka-0 -- /usr/bin/kafka-topics --zookeeper kafka-zookeeper:2181 --topic france --create --partitions 1 --replication-factor 1

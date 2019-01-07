#!/usr/bin/env bash

# the order should be respected, we can do a for f in file1 file2 ...

kubectl apply -f zookeeper-service.yml
kubectl apply -f zookeeper-service-headless.yml
kubectl apply -f zookeeper-stateful.yml
kubectl apply -f kafka-service.yml
kubectl apply -f kafka-service-headless.yml
kubectl apply -f kafka-statefulset.yml


# Create the topics, one for each country (see kakfa best practices (design-patterns ...))
# Wait until the pod kafka-0 if ready (should be taking into account TODO)
kubectl exec kafka-0 -- /usr/bin/kafka-topics --zookeeper kafka-zookeeper:2181 --topic france --create --partitions 1 --replication-factor 1

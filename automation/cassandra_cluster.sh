#!/usr/bin/env bash


kubectl apply -f cassandra-service-headless.yml
kubectl apply -f cassandra-service.yml
kubectl apply -f cassandra-statefulset.yml
kubectl apply -f cassandra-create-table.yml
kubectl apply -f cassandra-display-table.yml

#!/usr/bin/env bash


kubectl apply -f cassandra-service-headless.yml
kubectl apply -f cassandra-service.yml
kubectl apply -f cassandra-statefulset.yml

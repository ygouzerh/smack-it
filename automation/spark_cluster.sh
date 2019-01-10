#!/usr/bin/env bash


# NOT FINISHED YET

ERROR

# To be executed on the master or inside a pod (replicat)
# What if the driver falls down
kubectl create serviceaccount spark

kubectl create clusterrolebinding spark-role --clusterrole=edit --serviceaccount=default:spark --namespace=default


sudo apt install -y openjdk-8-jdk

wget http://mirrors.standaloneinstaller.com/apache/spark/spark-2.4.0/spark-2.4.0-bin-hadoop2.7.tgz

tar -xvzf spark-2.4.0-bin-hadoop2.7.tgz

rm spark-2.4.0-bin-hadoop2.7.tgz

mkdir spark-2.4.0-bin-hadoop2.7/src/

cp spark_consumer.py spark-2.4.0-bin-hadoop2.7/src/


cd spark-2.4.0-bin-hadoop2.7


sudo ./bin/docker-image-tool.sh -r docker.io/machine424  -t 1 build

sudo ./bin/docker-image-tool.sh -r docker.io/machine424  -t 1 push


sudo ./bin/spark-submit     --master k8s://https://172.31.38.115:6443     --deploy-mode cluster     --name spark-pi     --conf spark.executor.instances=2     --conf spark.kubernetes.container.image=machine424/spark-py:1    --conf spark.kubernetes.authenticate.driver.serviceAccountName=spark     --jars http://central.maven.org/maven2/org/apache/spark/spark-streaming-kafka-0-8-assembly_2.11/2.4.0/spark-streaming-kafka-0-8-assembly_2.11-2.4.0.jar      local:///spark_consumer.py

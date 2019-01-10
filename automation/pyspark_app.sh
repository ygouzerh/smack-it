#!/usr/bin/env bash


# copy the pyspark application (to be put inside the docker image)
mkdir spark-2.4.0-bin-hadoop2.7/src/
cp spark_consumer.py spark-2.4.0-bin-hadoop2.7/src/


# build the pyspark image and push it into docker hub
cd spark-2.4.0-bin-hadoop2.7

SHOULD PUSH (docker login)

sudo ./bin/docker-image-tool.sh -r docker.io/machine424  -t 3 build
sudo ./bin/docker-image-tool.sh -r docker.io/machine424  -t 3 push

# launch spark application
sudo ./bin/spark-submit     --master k8s://https://$(curl http://169.254.169.254/latest/meta-data/public-ipv4):6443     --deploy-mode cluster     --name spark-pi     --conf spark.executor.instances=3     --driver-java-options="-Droot.logger=ERROR,console"     --conf spark.kubernetes.container.image=machine424/spark-py:3    --conf spark.kubernetes.authenticate.driver.serviceAccountName=spark     --jars http://central.maven.org/maven2/org/apache/spark/spark-streaming-kafka-0-8-assembly_2.11/2.4.0/spark-streaming-kafka-0-8-assembly_2.11-2.4.0.jar      local:///spark_consumer.py

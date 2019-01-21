#!/bin/bash


./bin/spark-submit     --master k8s://https://${KUBERNETES_SERVICE_HOST}:443    --deploy-mode cluster     --name spark-pi     --conf spark.executor.instances=2     --driver-java-options="-Droot.logger=ERROR,console"     --conf spark.kubernetes.container.image=machine424/spark-py:8    --conf spark.kubernetes.authenticate.driver.serviceAccountName=spark     --jars http://central.maven.org/maven2/org/apache/spark/spark-streaming-kafka-0-8-assembly_2.11/2.4.0/spark-streaming-kafka-0-8-assembly_2.11-2.4.0.jar      local:///opt/spark/python/lib/spark_consumer.py

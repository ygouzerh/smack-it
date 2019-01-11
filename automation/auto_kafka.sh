#!/usr/bin/env bash

# Go at the project's root
cd ..

# Get master
echo "Retrieve the master..."
#master_public_ip=$(./manage.py read type get-master-public-ip)
master="ubuntu@34.242.47.132"

scp -o IdentitiesOnly=yes -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -i /Users/ayoubmrini424/k8s/master/connect-to-master.pem ./automation/kafka_cluster.sh "$master":~/

echo "Copying kafka manifests to the master"
for filename in config/kafka_clus/*.yml; do
  scp -o IdentitiesOnly=yes -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -i /Users/ayoubmrini424/k8s/master/connect-to-master.pem "$filename" "$master":~/
done

# According to the manifests,the cluster will contain one broker and one zookeeper (can be modified)
echo "Connect to the master to deploy kafka cluster"
echo "Connection to $master"
# Launch the command on the master
ssh -o IdentitiesOnly=yes -T -o "StrictHostKeyChecking no" -i /Users/ayoubmrini424/k8s/master/connect-to-master.pem "$master" << EOF
echo "------ KAFKA CLUSTER DEPLOYMENT --------"
sudo ./kafka_cluster.sh
EOF

cd automation

#!/usr/bin/env bash

# Go at the project's root
cd ..

# Where to store the private key
mkdir -p ssh/

# Create the aws infrastructure
#./manage.py install run
# Get master
echo "Retrieve the master..."
#master_public_ip=$(./manage.py read type get-master-public-ip)
master="ubuntu@34.242.218.115"

# Copy to be able to relaunch the ./deploy command infinitely
echo "Save the kadm conf worker's file"
cp ./config/k8s_clus/kadmconf_wor_default.yml ./config/k8s_clus/kadmconf_wor.yml

echo "Add the master public ip to the kadm conf worker's file"
echo "  - 34.242.218.115:6443" >> ./config/k8s_clus/kadmconf_wor.yml

echo "Copy configuration files and manifests to the master"
scp -o IdentitiesOnly=yes -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -i /Users/ayoubmrini424/k8s/master/connect-to-master.pem ./config/k8s_clus/kadmconf_mas.yml "$master":~/
scp -o IdentitiesOnly=yes -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -i /Users/ayoubmrini424/k8s/master/connect-to-master.pem ./config/k8s_clus/storage-class.yml "$master":~/
scp -o IdentitiesOnly=yes -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -i /Users/ayoubmrini424/k8s/master/connect-to-master.pem ./automation/master_install_*.sh "$master":~/
scp -o IdentitiesOnly=yes -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -i /Users/ayoubmrini424/k8s/master/connect-to-master.pem ./automation/common_install.sh "$master":~/

scp -o IdentitiesOnly=yes -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -i /Users/ayoubmrini424/k8s/master/connect-to-master.pem ./automation/cassandra_cluster.sh "$master":~/

# Send pyspark application to the master
scp -o IdentitiesOnly=yes -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -i /Users/ayoubmrini424/k8s/master/connect-to-master.pem ./src/spark/spark_consumer.py "$master":~/
scp -o IdentitiesOnly=yes -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -i /Users/ayoubmrini424/k8s/master/connect-to-master.pem ./src/spark/Dockerfile "$master":~/
scp -o IdentitiesOnly=yes -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -i /Users/ayoubmrini424/k8s/master/connect-to-master.pem ./config/spark/spark-submit.yml "$master":~/


# Send tweets producer yaml to the master
scp -o IdentitiesOnly=yes -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -i /Users/ayoubmrini424/k8s/master/connect-to-master.pem ./config/api/tweet-producer.yml "$master":~/

# Send web appli yamls to the master
scp -o IdentitiesOnly=yes -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -i /Users/ayoubmrini424/k8s/master/connect-to-master.pem ./config/app/app-f.yml "$master":~/
scp -o IdentitiesOnly=yes -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -i /Users/ayoubmrini424/k8s/master/connect-to-master.pem ./config/app/app-f-service.yml "$master":~/




echo "Connect to the master to launch the installation phase"
echo "Connection to $master"
# Launch the commands on the master
# Need to cut the installation in three, because master_install_1 need to be executed as the user
ssh -o IdentitiesOnly=yes -T -o "StrictHostKeyChecking no" -i /Users/ayoubmrini424/k8s/master/connect-to-master.pem "$master" << EOF
echo "Tearing down the last cluster"
sudo rm .kube/config
rm .kube/config
sudo kubeadm reset -f
echo "------ INSTALLATION --------"
sudo ./common_install.sh
sudo ./master_install_0.sh
./master_install_1.sh
sudo ./master_install_2.sh
kubectl apply -f storage-class.yml
EOF

echo "-- Workers configuration --"

strings=(
    "34.240.110.177"
    "63.33.192.2"
    "54.229.186.58"
)


for worker_ip in "${strings[@]}"; do
  worker="ubuntu@$worker_ip"
  echo "Copy configuration files to the worker"
  scp -o IdentitiesOnly=yes -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -i /Users/ayoubmrini424/k8s/master/connect-to-master.pem ./config/k8s_clus/kadmconf_wor.yml "$worker":~/
  scp -o IdentitiesOnly=yes -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -i /Users/ayoubmrini424/k8s/master/connect-to-master.pem ./automation/worker_install.sh "$worker":~/
  scp -o IdentitiesOnly=yes -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -i /Users/ayoubmrini424/k8s/master/connect-to-master.pem ./automation/common_install.sh "$worker":~/
  echo "Connect to the worker to launch the installation phase"
  echo "Connection to $worker"
  # Launch the commands on the worker
  ssh -o IdentitiesOnly=yes -T -o "StrictHostKeyChecking no" -i /Users/ayoubmrini424/k8s/master/connect-to-master.pem "$worker" << EOF
  echo "Tearing down the last cluster"
  sudo kubeadm reset -f
  echo "------ INSTALLATION --------"
  hostname
  sudo ./common_install.sh
  sudo ./worker_install.sh
EOF
done

echo "------ KAFKA CLUSTER INSTALLATION --------"
cd automation
./auto_kafka.sh
cd ..


echo "Copying cassandra manifests to the master"
for filename in config/cassandra_clus/*.yml; do
  scp -o IdentitiesOnly=yes -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -i /Users/ayoubmrini424/k8s/master/connect-to-master.pem "$filename" "$master":~/
done

echo "Connect to the master to deploy cassandra cluster"
echo "Connection to $master"
#Launch the command on the master
ssh -o IdentitiesOnly=yes -T -o "StrictHostKeyChecking no" -i /Users/ayoubmrini424/k8s/master/connect-to-master.pem "$master" << EOF
echo "------ CASSANDRA CLUSTER DEPLOYMENT --------"
sudo ./cassandra_cluster.sh
EOF

echo "------ START SENDING TWEETS --------"
ssh -o IdentitiesOnly=yes -T -o "StrictHostKeyChecking no" -i /Users/ayoubmrini424/k8s/master/connect-to-master.pem "$master" << EOF
kubectl apply -f tweet-producer.yml
EOF

echo "------ DEPLOY THE WEB APP --------"
ssh -o IdentitiesOnly=yes -T -o "StrictHostKeyChecking no" -i /Users/ayoubmrini424/k8s/master/connect-to-master.pem "$master" << EOF
kubectl apply -f app-f-service.yml
kubectl apply -f app-f.yml
EOF


echo "------ START SPARK --------"
ssh -o IdentitiesOnly=yes -T -o "StrictHostKeyChecking no" -i /Users/ayoubmrini424/k8s/master/connect-to-master.pem "$master" << EOF
echo "------ SPARK CLUSTER DEPLOYMENT --------"
kubectl create serviceaccount spark
kubectl create clusterrolebinding spark-role --clusterrole=edit --serviceaccount=default:spark --namespace=default
kubectl apply -f spark-submit.yml
EOF

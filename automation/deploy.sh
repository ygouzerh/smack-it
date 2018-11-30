#!/usr/bin/env bash

# Go at the project's root
cd ..

# Create the aws infrastructure
./manage.py install run

# Get master
echo "Retrieve the master..."
master_public_ip=$(./manage.py read type get-master-public-ip)
master="ubuntu@$master_public_ip"

# Copy to be able to relaunch the ./deploy command infinitely
echo "Save the kadm conf worker's file"
cp ./config/k8s_clus/kadmconf_wor_default.yml ./config/k8s_clus/kadmconf_wor.yml

echo "Add the master public ip to the kadm conf worker's file"
echo "  - $master_public_ip:6443" >> ./config/k8s_clus/kadmconf_wor.yml

echo "Copy configuration files to the master"
scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -i ssh/Smackey ./config/k8s_clus/kadmconf_mas.yml "$master":~/
scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -i ssh/Smackey ./automation/master_install.sh "$master":~/
scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -i ssh/Smackey ./automation/common_install.sh "$master":~/

echo "Connect to the master to launch the installation phase"
echo "Connection to $master"
# Launch the command on the master
ssh -T -o "StrictHostKeyChecking no" -i ssh/Smackey "$master" << EOF
echo "------ INSTALLATION --------"
sudo ./common_install.sh
sudo ./master_install.sh
EOF

echo "-- Workers configuration --"

for worker_ip in $(./manage.py read type get-workers-public-ip)
do
  worker="ubuntu@$worker_ip"
  echo "Copy configuration files to the worker"
  scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -i ssh/Smackey ./config/k8s_clus/kadmconf_wor.yml "$worker":~/
  scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -i ssh/Smackey ./automation/worker_install.sh "$worker":~/
  scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -i ssh/Smackey ./automation/common_install.sh "$worker":~/
  echo "Connect to the worker to launch the installation phase"
  echo "Connection to $worker"
  # Launch the command on the master
  ssh -T -o "StrictHostKeyChecking no" -i ssh/Smackey "$worker" << EOF
  echo "------ INSTALLATION --------"
  hostname
  #sudo ./common_install.sh
  #sudo ./worker_install.sh
EOF
done
#!/usr/bin/env bash

##### FUNCTIONS #####

## TRANSFER FILES FUNCTIONS
transfer_files_on_master(){
  # Transfer config files to the master
  master=$1
  echo "Deploy.sh : ----- COPY CONFIGURATION FILES (MASTER) : $master -----"
  scp -o IdentitiesOnly=yes -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -i ssh/Smackey ./config/k8s_clus/kadmconf_mas.yml "$master":~/ &
  pid_one=$!
  scp -o IdentitiesOnly=yes -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -i ssh/Smackey ./automation/master_install.sh "$master":~/ &
  pid_two=$!
  scp -o IdentitiesOnly=yes -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -i ssh/Smackey ./automation/common_install.sh "$master":~/ &
  pid_three=$!
  wait $pid_one
  wait $pid_two
  wait $pid_three
}

transfer_files_on_workers(){
  # Transfer config files to the worker
  for worker_ip in $(./manage.py read type get-workers-public-ip)
  do
    worker="ubuntu@$worker_ip"
    echo "Deploy.sh : ---- COPY CONFIGURATION FILES (WORKER) : $worker_ip"
    scp -o IdentitiesOnly=yes -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -i ssh/Smackey ./config/k8s_clus/kadmconf_wor.yml "$worker":~/ &
    pid_one=$!
    scp -o IdentitiesOnly=yes -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -i ssh/Smackey ./automation/worker_install.sh "$worker":~/ &
    pid_two=$!
    scp -o IdentitiesOnly=yes -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -i ssh/Smackey ./automation/common_install.sh "$worker":~/ &
    pid_three=$!
    wait $pid_one
    wait $pid_two
    wait $pid_three
  done
}

transfer_files(){
  echo "Deploy.sh : ----- TRANSFERT FILES -----"
  # Wrapper to transfer config files in parallel
  transfer_files_on_master $1 &
  pid_one=$!
  transfer_files_on_workers &
  pid_two=$!
  wait $pid_one
  wait $pid_two
}

## INSTALLATION FUNCTIONS
install_master(){
  master=$1
  # Launch installation scripts on the master
  echo "Deploy.sh : ----- MASTER INSTALLATION  -----"
  ssh -o IdentitiesOnly=yes -T -o "StrictHostKeyChecking no" -i ssh/Smackey "$master" << EOF
  sudo ./common_install.sh
  sudo ./master_install.sh
EOF
}

install_worker(){
  # Launch installation scripts on one worker
  worker_ip=$1
  worker="ubuntu@$worker_ip"
  echo "Deploy.sh : -- CONNECTION TO $worker -- "
  ssh -o IdentitiesOnly=yes -T -o "StrictHostKeyChecking no" -i ssh/Smackey "$worker" << EOF
  hostname
  sudo ./common_install.sh
  sudo ./worker_install.sh
EOF
}

install_workers(){
  # Launch the installation scripts on the worker
  echo "Deploy.sh : ----- WORKER INSTALLATION -----"
  for worker_ip in $(./manage.py read type get-workers-public-ip)
  do
    install_worker $worker_ip &
    pid_one=$!
    wait $pid_one
  done
}

install(){
  install_master $1
  install_workers
}

##### MAIN #####

# Go at the project's root
cd ..

# Where to store the private key
mkdir -p ssh/

# Create the aws infrastructure
./manage.py install run

# Retrieve the master
echo "Deploy.sh : Retrieve the master..."
master_public_ip=$(./manage.py read type get-master-public-ip)
master="ubuntu@$master_public_ip"

# Copy to be able to relaunch the ./deploy command infinitely
echo "Deploy.sh : Save the kadm conf worker's file"
cp ./config/k8s_clus/kadmconf_wor_default.yml ./config/k8s_clus/kadmconf_wor.yml

echo "Deploy.sh : Add the master public ip to the kadm conf worker's file"
echo "  - $master_public_ip:6443" >> ./config/k8s_clus/kadmconf_wor.yml

# Transfer the config files
transfer_files $master

# Install the master / workers
install $master

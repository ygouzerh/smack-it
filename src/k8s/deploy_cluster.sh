#I) Create the instances

### 1) Instance Type: All the nodes should have : (we use t2.micro for the moment)
#  2 GB or more of RAM
#  2 CPUs or more

### 2) AMI: The instances use the AMI ami-0773391ae604c49a4 (we didn't test on the others)

### 3) Security Group: Certain ports should be opened: (we open all the ports for the moment)
  # For the masters nodes: (for the moment there is just one master)

    # Protocol	   Direction	  Port Range	   Purpose	                   Used By
    # TCP	          Inbound	       6443  	   Kubernetes API server	        All
    # TCP	          Inbound	       2379-2380	etcd server client API	    kube-apiserver, etcd
    # TCP	          Inbound	       10250	   Kubelet API	                 Self, Control plane
    # TCP	          Inbound	       10251	   kube-scheduler	                Self
    # TCP	          Inbound	       10252	   kube-controller-manager	     Self

  # For the workers nodes:

    # Protocol	Direction	Port Range	     Purpose	         Used By
    # TCP	      Inbound	 10250	       Kubelet API	       Self, Control plane
    # TCP	      Inbound	 30000-32767  	NodePort Services     	All

### 4) IAM: give permission to all the nodes (so they can manage EBS/EFS): (we give the AdministratorAccess Policy for now)

### 5) The hostname of each node must match EC2’s private DNS entry for that node. (done, see below)

### 6) Tag all the resources used by the cluster (EC2, volumes, subnets, securitygroups,) with--> kubernetes.io/cluster/kubernetes=owned

### 7) Disable the swap on the machines, pods should fit within the memory of the node. (done, see below)




#II) Configure the instances & deploy the k8s cluster

## 1) To be executed on the masters (one for the moment) :

# For now, kubectl is also installed on the master;  we can install it on
# a development system and configuring it to connect to the remote Kubernetes cluster.
sudo hostnamectl set-hostname $(curl -s http://169.254.169.254/latest/meta-data/local-hostname)
sudo swapoff -a
sudo apt-get update && apt-get install -y apt-transport-https curl
sudo curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -
sudo cat <<EOF >/etc/apt/sources.list.d/kubernetes.list
deb https://apt.kubernetes.io/ kubernetes-xenial main
EOF
sudo apt-get update
sudo apt-get install -y kubelet kubeadm kubectl docker.io
sudo apt-mark hold kubelet kubeadm kubectl docker.io

#Initialize the master
sudo kubeadm init --config kadmconfig_mas.yml


#To make kubectl work for your non-root user, run these commands, which are also part of the kubeadm init output:
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config

# Install a pod network add-on (To allow the pods communicating with each others)
sudo kubectl apply -f https://docs.projectcalico.org/v3.1/getting-started/kubernetes/installation/hosted/rbac-kdd.yaml
sudo kubectl apply -f https://docs.projectcalico.org/v3.1/getting-started/kubernetes/installation/hosted/kubernetes-datastore/calico-networking/1.7/calico.yaml





## 2) To be executed on the workers:
sudo hostnamectl set-hostname $(curl -s http://169.254.169.254/latest/meta-data/local-hostname)
sudo swapoff -a
sudo apt-get update && apt-get install -y apt-transport-https curl
sudo curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -
sudo cat <<EOF >/etc/apt/sources.list.d/kubernetes.list
deb https://apt.kubernetes.io/ kubernetes-xenial main
EOF
sudo apt-get update
sudo apt-get install -y kubelet kubeadm docker.io
sudo apt-mark hold kubelet kubeadm docker.io


# After the command sudo kubeadm init --config kadmconfig_mas.yml has finished, join the worker to the master
sudo kubeadm join --config kadmconf_wor.yml

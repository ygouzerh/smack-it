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
# --pod-network-cidr=192.168.0.0/16 for Calico
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


cat <<EOF | sudo tee /etc/default/kubelet
KUBELET_EXTRA_ARGS=--cloud-provider=aws
EOF

# After the command sudo kubeadm init --config kadmconfig_mas.yml has finished, join the worker to the master
# eg.: sudo kubeadm join MASTER_PRIVATE_IP:6443 --token <token> --discovery-token-ca-cert-hash sha256:xxxx
# To get this command, run on the master:
sudo kubeadm token create --print-join-command







######################Trash


# To get the public IPv4 of an instance
curl http://169.254.169.254/latest/meta-data/public-ipv4





# To execute on all nodes
# ssh -o "StrictHostKeyChecking no" -i master/connect-to-master.pem ubuntu@IP
# kubectl communicates with server-api located on the master to deploy a
# containerized application for example.

# mkdir -p /etc/kubernetes/
# touch /etc/kubernetes/cloud.conf
# cat << EOF  > /etc/kubernetes/cloud.conf
# [Global]
# KubernetesClusterTag=kubernetes
# KubernetesClusterID=kubernetes
# Zone=eu-west-1b
# EOF
# sudo chmod 0600 /etc/kubernetes/cloud.conf
# # change the hostname, maybe we should also edit the /etc/cloud/cloud.cfg file.






# alias for kubectl and auto-completion, should to install a package called bash-completion
alias k=kubectl
source <(kubectl completion bash) # to add it to the profile echo "source <(kubectl completion bash)" >> ~/.bashrc
source <(kubectl completion bash | sed s/kubectl/k/g) # to add it to the profile echo "source <(kubectl completion bash | sed s/kubectl/k/g)" >> ~/.bashrc






# To control the cluster from a remote machine (dev machine) other than the master
# On the master (on /home/ubuntu for eg)
sudo cp /etc/kubernetes/admin.conf . && sudo chown ubuntu admin.conf

# on the remote machine

##
scp -o "StrictHostKeyChecking no" -i master/connect-to-master.pem ubuntu@GLOBAL_MASTER_ID:admin.conf .
  # the certificate will not  be validated : kubectl --kubeconfig ./admin.conf --insecure-skip-tls-verify get nodes
kubectl --kubeconfig ./admin.conf get nodes


## or, to make this cluster the one by default
mkdir -p $HOME/.kube
scp -o "StrictHostKeyChecking no" -i master/connect-to-master.pem ubuntu@GLOBAL_MASTER_ID:admin.conf $HOME/.kube/config
kubectl get nodes

#Dashboard
kubectl --kubeconfig ./admin.conf proxy
#Access the dashboard on:
# http://localhost:8001/api/v1/namespaces/kube-system/services/https:kubernetes-dashboard:/proxy/



##### TALK about the limitations=things to be done
# only one master (see official site)
# Auto scaling (pods and nodes)




kubectl edit node ip-172-31-22-38.eu-west-1.compute.internal

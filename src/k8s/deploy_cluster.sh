


# For the moment we will install a SINGLE master Kubernetes cluster
# this should be automated


# install kubeadm, kubelet and kubectl on every node of the cluster (including the master)
# kubectl is not required on the workers but that way from any machine, with the right permissions, we can use kubectl.
# prevent automatic updates


sudo apt-get update && apt-get install -y apt-transport-https curl
sudo curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -
sudo cat <<EOF >/etc/apt/sources.list.d/kubernetes.list
deb https://apt.kubernetes.io/ kubernetes-xenial main
EOF
sudo apt-get update
sudo apt-get install -y kubelet kubeadm kubectl docker.io
sudo apt-mark hold kubelet kubeadm kubectl docker.io

# SSH to the master
# Kubeadm installs for us : etcd (the cluster database), the API server (which the kubectl CLI communicates with), the scheduler etc.
#To make kubectl work for your non-root user, run these commands, which are also part of the kubeadm init output:
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config

#Initialize the master
# --pod-network-cidr=192.168.0.0/16 for Calico
kubeadm init --pod-network-cidr=192.168.0.0/16


# Install a pod network add-on (To allow the pods communicating with each others)
# We will use Calico for that
kubectl apply -f https://docs.projectcalico.org/v3.1/getting-started/kubernetes/installation/hosted/rbac-kdd.yaml
kubectl apply -f https://docs.projectcalico.org/v3.1/getting-started/kubernetes/installation/hosted/kubernetes-datastore/calico-networking/1.7/calico.yaml



# join nodes to the cluster.

#SSH to the machine
#Become root (e.g. sudo su -)
#Run the command that was output by kubeadm init. For example:
kubeadm join --token <token> <master-ip>:<master-port> --discovery-token-ca-cert-hash sha256:<hash>

#!/bin/bash

sudo swapoff -a

sudo systemctl stop containerd

systemctl stop snap.microk8s.daemon-kubelite.service

sudo kubeadm reset

sudo rm -rf /etc/cni/net.d

sudo kubeadm init --pod-network-cidr=10.244.0.0/16

mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config

kubectl create -f kube-flannel.yml

echo "sudo $(kubeadm token create --print-join-command)" >> join.sh

nohup python -m http.server 1234 &

#!/bin/bash

sudo swapoff -a

sudo systemctl stop containerd

sudo systemctl restart crio

sudo kubeadm reset

sudo rm -rf /etc/cni/net.d

sudo swapoff -a

kubeadm join 192.168.21.81:6443 --token 2nk9k2.9p8evudq8klxemzy \
	--discovery-token-ca-cert-hash sha256:4903d22e72993f6dcb6dddd7bd6b8924b6660697e5b828acf8eca8e9adf400cf 

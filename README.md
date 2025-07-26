# GCP VM setup:

## Machine configuration
select e2-standard-4 (4 vCPU, 2 core, 16 GB memory) for VM in GCP
2 CPUs are for minikube

## OS and storage
change to ubuntu with version Ubuntu 24.04 LTS x86/64
Size setting to 150 GB

## Networking
Allow HTTP traffic, HTTPS traffic, and Load Balancer Health Checks
Enable IP forwarding

## After creating VM
1. connect to SSH
2. install Docker in the machine, could go search for "docker install on ubuntu" or "https://docs.docker.com/engine/install/ubuntu/" and look for installation commands
### First command
# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update

Second command
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

Third command for verifying installation
sudo docker run hello-world

Then go to "Linux post installation steps for Docker Engine" or "https://docs.docker.com/engine/install/linux-postinstall/"
First command
sudo groupadd docker

Secnond command
sudo usermod -aG docker $USER

Third command
newgrp docker

Fourth command (used to verify)
docker run hello-world

Configure Docker to start on boot with systemd
First command
sudo systemctl enable docker.service

Second command
sudo systemctl enable containerd.service

3. Install minikube ("https://minikube.sigs.k8s.io/docs/start/?arch=%2Flinux%2Fx86-64%2Fstable%2Fbinary+download")
select Linux, x86-64, Stable, Binary Download

Commands
curl -LO https://github.com/kubernetes/minikube/releases/latest/download/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube && rm minikube-linux-amd64

minikube start

4. Install kubectl for linux
select x86-64
commands
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo snap install kubectl --classic (need that sudo, this command is for installation)
kubectl version --client (for verifying if installation success)






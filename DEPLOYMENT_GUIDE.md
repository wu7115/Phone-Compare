## GCP VM Setup

### VM Configuration

* Select **e2-standard-4** (4 vCPUs, 2 cores, 16 GB memory)
  * Reserve 2 CPUs for Minikube

### OS and Storage

* OS: **Ubuntu 24.04 LTS x86/64**
* Disk Size: **150 GB**

### Networking

* Enable:

  * HTTP Traffic
  * HTTPS Traffic
  * Load Balancer Health Checks
* Enable **IP Forwarding**

## Firewall Setup in GCP

* Go to **VPC Network > Firewall**
* Create Rule:

  * Direction: **Ingress**
  * Action: **Allow**
  * Targets: **All instances in the network**
  * Source IP ranges: **0.0.0.0/0**
  * Protocols and ports: **Allow all**

## Connect to SSH and Install Docker

Refer to [Docker's official Ubuntu installation guide](https://docs.docker.com/engine/install/ubuntu/)

```bash
# Add Docker's official GPG key
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add Docker repository to Apt sources
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo \"${UBUNTU_CODENAME:-$VERSION_CODENAME}\") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update

# Install Docker
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Verify installation
sudo docker run hello-world
```

### Post-installation Docker Setup

Refer to [Linux post-install steps](https://docs.docker.com/engine/install/linux-postinstall/):

```bash
sudo groupadd docker
sudo usermod -aG docker $USER
newgrp docker

docker run hello-world

# Enable Docker on boot
sudo systemctl enable docker.service
sudo systemctl enable containerd.service
```

## Install Minikube

Refer to [Minikube install guide](https://minikube.sigs.k8s.io/docs/start/):

```bash
curl -LO https://github.com/kubernetes/minikube/releases/latest/download/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube && rm minikube-linux-amd64

minikube start
```

## Install kubectl

```bash
# Download the kubectl binary
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"

# Install with Snap
sudo snap install kubectl --classic

# Verify installation
kubectl version --client
```

## Clone Project Repository

```bash
git clone https://github.com/{your-username}/{Project}
cd Phone-Compare

# Set Git config
git config --global user.email "{your email}"
git config --global user.name "{your name}"

# Commit and push changes
git add .
git commit -m "commit"
git push origin main

# If asked, use your GitHub token as password

# Pull updates from repo
git pull origin main
```

## Build and Deploy App on VM

```bash
# Point Docker to Minikube
eval $(minikube docker-env)

# Build Docker image
docker build -t flask-app:latest .

# Create Kubernetes secrets
kubectl create secret generic llmops-secrets \
  --from-literal=GROQ_API_KEY="" \
  --from-literal=ASTRA_DB_APPLICATION_TOKEN="" \
  --from-literal=ASTRA_DB_KEYSPACE="default_keyspace" \
  --from-literal=ASTRA_DB_API_ENDPOINT="" \
  --from-literal=HF_TOKEN="" \
  --from-literal=HUGGINGFACEHUB_API_TOKEN=""

# Deploy to Kubernetes
kubectl apply -f flask-deployment.yaml
kubectl get pods

# Port forward to expose app
kubectl port-forward svc/flask-service 5001:80 --address 0.0.0.0
```

## Monitoring with Prometheus & Grafana

```bash
cd Phone-Compare

# Create monitoring namespace
kubectl create namespace monitoring
kubectl get ns

# Apply deployment configs
kubectl apply -f prometheus/prometheus-configmap.yaml
kubectl apply -f prometheus/prometheus-deployment.yaml
kubectl apply -f grafana/grafana-deployment.yaml

# Expose Prometheus and Grafana
kubectl port-forward --address 0.0.0.0 svc/prometheus-service -n monitoring 9090:9090
kubectl port-forward --address 0.0.0.0 svc/grafana-service -n monitoring 3000:3000
```

### Access Prometheus and Grafana

* Open in browser: `http://{VM External IP}:9090` for Prometheus
* Open in browser: `http://{VM External IP}:3000` for Grafana
* Default login: **admin / admin**

### Configure Grafana

1. Go to **Data Sources**
2. Click **Add data source** → select **Prometheus**
3. Set URL to: `http://prometheus-service.monitoring.svc.cluster.local:9090`
4. Click **Save & Test**

### Create Dashboard

1. Navigate to **Dashboards** → **Create dashboard**
2. Add **visualization**
3. Select **Prometheus** as data source
4. Choose and configure your desired metrics

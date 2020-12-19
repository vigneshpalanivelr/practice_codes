#!/bin/bash

# Install Docker CE on RHEL 7 # Update system.
sudo yum update -y

# Un-Install packages.
sudo yum remove -y docker-common
sudo yum remove -y docker
sudo yum remove -y container-selinux
sudo yum remove -y docker-selinux
sudo yum remove -y docker-engine

# Install required packages.
sudo yum install -y wget
sudo yum install -y lvm2
sudo yum install -y device-mapper
sudo yum install -y device-mapper-persistent-data
sudo yum install -y device-mapper-event
sudo yum install -y device-mapper-libs
sudo yum install -y device-mapper-event-libs

# Install container-selinux. Check for latest version: http://mirror.centos.org/centos/7/extras/x86_64/Packages/.
# Set up Docker repository.
wget https://download.docker.com/linux/centos/docker-ce.repo -O /etc/yum.repos.d/docker-ce.repo

# Correct the docker-ce.repo
# sed -i 's/$releasever/7/g' /etc/yum.repos.d/docker-ce.repo

# Install Docker CE and tools.
sudo yum -y install docker-ce

# Start and Enable Docker
systemctl start docker
systemctl enable docker

# List Docker Packages
yum list docker-ce --showduplicates | sort -r
docker version
docker info


# Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/1.27.4/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
docker-compose --version

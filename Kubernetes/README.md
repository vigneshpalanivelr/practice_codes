- [Kubernetes Commands](#kubernetes-commands)
  * [Minikube commands](#minikube-commands)
    + [Creating profile (Docker & hyperkit)](#creating-profile--docker---hyperkit-)
    + [Check and Select Profile](#check-and-select-profile)
    + [Connect to minikube cluster](#connect-to-minikube-cluster)
    + [Add & Delete a node](#add---delete-a-node)
    + [Start, Stop & Delete cluster](#start--stop---delete-cluster)
    + [Ip and Service](#ip-and-service)
    + [Port Forwording](#port-forwording)
  * [Kubectl Config](#kubectl-config)
  * [Resources](#resources)
  * [Node Commands](#node-commands)
  * [Pod Commands](#pod-commands)
    + [Create pod](#create-pod)
    + [List the pods](#list-the-pods)
    + [Describing pods](#describing-pods)
    + [Delete pods](#delete-pods)
    + [Connecting to container](#connecting-to-container)
    + [Logs of a pod](#logs-of-a-pod)
    + [Access a pod using port-forwording](#access-a-pod-using-port-forwording)
  * [Replica set commands](#replica-set-commands)
    + [Create RS](#create-rs)
    + [List RS](#list-rs)
    + [Describe](#describe)
    + [Delete](#delete)
  * [Deployment Commands](#deployment-commands)
    + [Create deployments](#create-deployments)
    + [List Deployments](#list-deployments)
    + [Scale Deployment](#scale-deployment)
    + [Set image of a deployment](#set-image-of-a-deployment)
    + [Deployment rollout](#deployment-rollout)
  * [Service Commands](#service-commands)
    + [Create ClusterIP service](#create-clusterip-service)
    + [Access in minikube](#access-in-minikube)
    + [Create ClusterIP service with multiple ports](#create-clusterip-service-with-multiple-ports)
    + [Access in minikube](#access-in-minikube-1)
    + [Create NodePort service](#create-nodeport-service)
    + [Access in laptop](#access-in-laptop)
    + [Create NodePort service with multiple ports](#create-nodeport-service-with-multiple-ports)
    + [Access in minikube](#access-in-minikube-2)
  * [Ingress Commands](#ingress-commands)
    + [Enable Ingress controller in Minicube](#enable-ingress-controller-in-minicube)
    + [Create resources for Path Based Routing](#create-resources-for-path-based-routing)
    + [Create resources for Host Based Routing](#create-resources-for-host-based-routing)
    + [Configure Default Backend](#configure-default-backend)
    + [HTTP to HTTPS TLS Certificate addition](#http-to-https-tls-certificate-addition)

<small><i><a href='http://ecotrust-canada.github.io/markdown-toc/'>Table of contents generated with markdown-toc</a></i></small>


# Kubernetes Commands

## Minikube commands
### Creating profile (Docker & hyperkit)
```
minikube status
minikube start --nodes 5 -p vignesh-cluster --driver=docker
brew install hyperkit
minikube start --nodes 5 -p vignesh-vm-cluster  --vm=true
```
### Check and Select Profile
```
minikube status
minikube profile list
minikube profile vignesh-cluster
```

### Connect to minikube cluster
```
minikube ssh
minikube dashboard
```

### Add & Delete a node
```
minikube node add --worker -p vignesh-cluster
minikube node delete vignesh-cluster-m03 -p vignesh-cluster
```

### Start, Stop & Delete cluster
```
minikube start
minikube stop
minikube delete
rm -rf ~/.minikube/
```

### Ip and Service
```
minikube ip -p vignesh-cluster
minikube service vignesh-service -p vignesh-cluster
minikube addons enable ingress
```

### Port Forwording
```
kubectl port-forward <service> <source-port>:<target-port>
```

## Kubectl Config
```
kubectl config view
kubectl config get-contexts
kubectl config set-context vignesh-cluster
kubectl config set-context --current --namespace=<namespace>
```
------------

## Resources
```
kubectl api-resources | grep -i pod
kubectl delete all --all
```
------------

## Node Commands
```
kubectl get nodes
kubectl describe nodes
```

------------
## Pod Commands
### Create pod
```
kubectl run nginx-pod --image=nginx
kubectl run nginx-pod --image=nginx --namespace=<namespace>
kubectl apply -f nginx-pod.yaml
kubectl apply -f nginx-pod.yaml --namespace=<namespace>
```

### List the pods
```
kubectl get pods
kubectl get pods -A
kubectl get pods -o wide
kubectl get pods -n <namespace>
```

### Describing pods
`kubectl describe pod nginx-pod-2 | less`

### Delete pods
```
kubectl delete pod nginx-pod-1
kubectl delete -f nginx-pod.yaml
```

### Connecting to container
`kubectl exec -it <pod-name> -c <con-name> -- bash`

### Logs of a pod
`kubectl logs nginx-pod-2`

### Access a pod using port-forwording
`kubectl port-forward nginx-pod-2 8080:80`

------------

## Replica set commands
### Create RS
```
kubectl apply -f vignesh-rs.yaml
kubectl apply -f vignesh-rs.yaml -n <namespace>
```

### List RS
```
kubectl get rs
kubectl get rs -A
kubectl get rs -n <namespace> -o wide
```

### Describe
`kubectl describe rs <rs_name>`

### Delete
```
kubectl delete rs <rs_name>
kubectl delete -f vignesh-rs.yaml
```

------------
  
## Deployment Commands
### Create deployments
`kubectl apply -f deployment-handson.yaml`

### List Deployments
`kubectl get deployment`

### Scale Deployment
`kubectl scale --replicas=2 deployment/deployment-handson`

### Set image of a deployment
```
kubectl set image deployment/deployment-handson deployment-handson-con=nginx:1.20
kubectl set image deployment/deployment-handson deployment-handson-con=nginx:1.19 --record
```

### Deployment rollout
```
kubectl rollout history deployments
kubectl rollout undo deployment --to-revision=6
kubectl rollout status deployment/deployment-handson
```

------------
  
## Service Commands
### Create ClusterIP service
```
kubectl apply -f service-handson.yaml
kubectl get all -o wide
```

### Access in minikube
```
minikube ssh
curl <node-port-ip>:8080
curl <worker-ip>:80
```

### Create ClusterIP service with multiple ports
```
kubectl apply -f service-handson-mp.yaml
kubectl get all -o wide
```

### Access in minikube
```
minikube ssh
curl <node-port-ip>:8080
curl <node-port-ip>:8081
curl <worker-ip>:80
```

### Create NodePort service
```
kubectl apply -f service-handson-np.yaml
kubectl get all -o wide
```

### Access in laptop
```
minikube ip
curl <minikube-ip>:32000
minikube ssh
curl <node-port-ip>:8080
curl <worker-ip>:80
```

### Create NodePort service with multiple ports
```
kubectl apply -f service-handson-mp-mp.yaml
kubectl get all -o wide
```

### Access in minikube
```
minikube ip
curl <minikube-ip>:32001
minikube ssh
curl <node-port-ip>:8081
curl <worker-ip>:80
```

------------

## Ingress Commands
### Enable Ingress controller in Minicube
```
minikube addons enable ingress
kubectl get ing
```

### Create resources for Path Based Routing
```
curl http://ingress-nginx.com/
curl -L http://ingress-nginx.com/demo
```

### Create resources for Host Based Routing
```
curl -L http://ingress-nginx-hbr-1.com
curl -L http://ingress-nginx-hbr-2.com/demo
```

### Configure Default Backend
### HTTP to HTTPS TLS Certificate addition
```
openssl req -x509 -newkey rsa:4096 -sha256 -nodes -keyout tls.key -out tls.crt -subj "/CN=ingress-nginx.com" -days 10000
kubectl create secret tls ingress-nginx-com-tls --cert tls.crt --key tls.key
kubectl apply -f 05-ingress-handson/ingress-handson.yaml 
hit https://ingress-nginx.com/
and type thisisunsafe in browser webpage
```
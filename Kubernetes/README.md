# Kubernetes Commands

## Minikube commands
### Creating profile (Docker & hyperkit)
minikube status
minikube start --nodes 5 -p vignesh-cluster --driver=docker
brew install hyperkit
minikube start --nodes 5 -p vignesh-vm-cluster  --vm=true
### Check and Select Profile
minikube status
minikube profile list
minikube profile vignesh-cluster
### Connect to minikube cluster
minikube ssh
minikube dashboard
### Add & Delete a node
minikube node add --worker -p vignesh-cluster
minikube node delete vignesh-cluster-m03 -p vignesh-cluster
### Start, Stop & Delete cluster
minikube start
minikube stop
minikube delete
rm -rf ~/.minikube/
### Ip and Service
minikube ip -p vignesh-cluster
minikube service vignesh-service -p vignesh-cluster
minikube addons enable ingress
### Port Forwording
kubectl port-forward <service> <source-port>:<target-port>


## Kubectl Config
kubectl config view
kubectl config get-contexts
kubectl config set-context vignesh-cluster
kubectl config set-context --current --namespace=<namespace>

## Resources
kubectl api-resources | grep -i pod
kubectl delete all --all

## Node Commands
kubectl get nodes
kubectl describe nodes

## Pod Commands
### Create pod
kubectl run nginx-pod --image=nginx
kubectl run nginx-pod --image=nginx --namespace=<namespace>
kubectl apply -f nginx-pod.yaml
kubectl apply -f nginx-pod.yaml --namespace=<namespace>
### List the pods
kubectl get pods
kubectl get pods -A
kubectl get pods -o wide
kubectl get pods -n <namespace>
### Describing pods
kubectl describe pod nginx-pod-2 | less
### Delete pods
kubectl delete pod nginx-pod-1
kubectl delete -f nginx-pod.yaml
### Connecting to container
kubectl exec -it <pod-name> -c <con-name> -- bash
### Logs of a pod
kubectl logs nginx-pod-2
### Access a pod using port-forwording
kubectl port-forward nginx-pod-2 8080:80

## Replica set commands
### Create RS
kubectl apply -f vignesh-rs.yaml
kubectl apply -f vignesh-rs.yaml -n <namespace>
### List RS
kubectl get rs
kubectl get rs -A
kubectl get rs -n <namespace> -o wide
### Describe
kubectl describe rs <rs_name>
### Delete
kubectl delete rs <rs_name>
kubectl delete -f vignesh-rs.yaml

## Deployment Commands
### Create deployments
kubectl apply -f deployment-handson.yaml
### List Deployments
kubectl get deployment
### Scale Deployment
kubectl scale --replicas=2 deployment/deployment-handson
### Set image of a deployment
kubectl set image deployment/deployment-handson deployment-handson-con=nginx:1.20
kubectl set image deployment/deployment-handson deployment-handson-con=nginx:1.19 --record
### Deployment rollout
kubectl rollout history deployments
kubectl rollout undo deployment --to-revision=6
kubectl rollout status deployment/deployment-handson

## Service Commands
### Create ClusterIP service
kubectl apply -f service-handson.yaml
kubectl get all -o wide
### Access in minikube
minikube ssh
curl <node-port-ip>:8080
curl <worker-ip>:80
### Create ClusterIP service with multiple ports
kubectl apply -f service-handson-mp.yaml
kubectl get all -o wide
### Access in minikube
minikube ssh
curl <node-port-ip>:8080
curl <node-port-ip>:8081
curl <worker-ip>:80
### Create NodePort service
kubectl apply -f service-handson-np.yaml
kubectl get all -o wide
### Access in laptop
minikube ip
curl <minikube-ip>:32000
minikube ssh
curl <node-port-ip>:8080
curl <worker-ip>:80
### Create NodePort service with multiple ports
kubectl apply -f service-handson-mp-mp.yaml
kubectl get all -o wide
### Access in minikube
minikube ip
curl <minikube-ip>:32001
minikube ssh
curl <node-port-ip>:8081
curl <worker-ip>:80
### Do /04-services-handson/service-deployment-python-demo.yaml
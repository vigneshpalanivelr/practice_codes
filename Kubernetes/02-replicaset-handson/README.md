# Repliction Set - Hands-On
```
1) Create Replication Set YAML with pod name rs-handson-pod
- kubectl apply -f replicaset-handson/rs-handson.yaml

2) Create a pod with name nginx-pod
- kubectl apply -f  02-replicaset-handson/nginx-pod.yaml 

3) Check total number of pods and pods are created via Replication set
- kubectl get pods -owide
- kubectl get pods -l team=int -owide

4) Show the repica set created
- kubectl get rs

5) Delete nginx-pod-2 created pod and check pods
- kubectl delete pod nginx-pod
- kubectl get pods -owide

6) Delete a pod created by Replication Set
- kubectl delete pod rs-handson-pjltw
- kubectl get pods

7) Delete a node and check the pods
- kubectl get pods -o wide
- kubectl get nodes
- minikube node delete vignesh-vm-cluster-m02 -p vignesh-vm-cluster
- kubectl get pods -o wide
```
## Create Replication Set YAML with pod name rs-handson-pod
- kubectl apply -f replicaset-handson/rs-handson.yaml
```
dhivyamalathirajasekaran$ cat 02-replicaset-handson/rs-handson.yaml 
---
apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: rs-handson
  labels:
    team: int
spec:
  replicas: 3
  selector:
    matchLabels:
      team: int
  template:
    metadata:
      name: rs-handson-pod
      labels:
        team: int
    spec:
      containers:
      - name: rs-handson-con
        image: nginx:latest
        ports:
        - containerPort: 81

dhivyamalathirajasekaran$ kubectl apply -f replicaset-handson/rs-handson.yaml 
replicaset.apps/rs-handson created
```

## Create a pod with name nginx-pod
- kubectl apply -f  02-replicaset-handson/nginx-pod.yaml 
```
dhivyamalathirajasekaran$ cat 02-replicaset-handson/nginx-pod.yaml 
---
apiVersion: v1
kind: Pod
metadata:
  name: nginx-pod
spec:
  containers:
  - name: nginx-con
    image: nginx:latest
    ports:
    - containerPort: 80

dhivyamalathirajasekaran$ kubectl apply -f  02-replicaset-handson/nginx-pod.yaml 
pod/nginx-pod-2 created
```

## Check total number of pods and pods are created via Replication set
- kubectl get pods -owide
- kubectl get pods -l team=int -owide
```
dhivyamalathirajasekaran$ kubectl get pods -owide
NAME               READY   STATUS    RESTARTS   AGE    IP            NODE                     NOMINATED NODE   READINESS GATES
nginx-pod          1/1     Running   0          12m    10.244.2.13   vignesh-vm-cluster-m03   <none>           <none>
rs-handson-pjltw   1/1     Running   0          103s   10.244.2.14   vignesh-vm-cluster-m03   <none>           <none>
rs-handson-srvdf   1/1     Running   0          12m    10.244.1.13   vignesh-vm-cluster-m02   <none>           <none>
rs-handson-wdmww   1/1     Running   0          12m    10.244.3.14   vignesh-vm-cluster-m04   <none>           <none>

dhivyamalathirajasekaran$ kubectl get pods -l team=int -owide
NAME               READY   STATUS    RESTARTS   AGE     IP            NODE                     NOMINATED NODE   READINESS GATES
rs-handson-pjltw   1/1     Running   0          5m11s   10.244.2.14   vignesh-vm-cluster-m03   <none>           <none>
rs-handson-srvdf   1/1     Running   0          15m     10.244.1.13   vignesh-vm-cluster-m02   <none>           <none>
rs-handson-wdmww   1/1     Running   0          15m     10.244.3.14   vignesh-vm-cluster-m04   <none>           <none>
```

## Show the repica set created
- kubectl get rs
```
dhivyamalathirajasekaran$ kubectl get rs
NAME         DESIRED   CURRENT   READY   AGE
rs-handson   3         3         3       19m
```

## Delete nginx-pod-2 created pod and check pods
- kubectl delete pod nginx-pod
- kubectl get pods -owide
```
dhivyamalathirajasekaran$ kubectl delete pod nginx-pod
pod "nginx-pod" deleted

dhivyamalathirajasekaran$ kubectl get pods -owide
NAME               READY   STATUS    RESTARTS   AGE   IP            NODE                     NOMINATED NODE   READINESS GATES
rs-handson-pjltw   1/1     Running   0          14m   10.244.2.14   vignesh-vm-cluster-m03   <none>           <none>
rs-handson-srvdf   1/1     Running   0          25m   10.244.1.13   vignesh-vm-cluster-m02   <none>           <none>
rs-handson-wdmww   1/1     Running   0          25m   10.244.3.14   vignesh-vm-cluster-m04   <none>           <none>
```

## Delete a pod created by Replication Set
- kubectl delete pod rs-handson-pjltw
- kubectl get pods
```
dhivyamalathirajasekaran$ kubectl delete pod rs-handson-pjltw
pod "rs-handson-pjltw" deleted

dhivyamalathirajasekaran$ kubectl get pods
NAME               READY   STATUS    RESTARTS   AGE
rs-handson-q4qjf   1/1     Running   0          66s
rs-handson-srvdf   1/1     Running   0          83m
rs-handson-wdmww   1/1     Running   0          83m
```

## Delete a node and check the pods
- kubectl get pods -o wide
- kubectl get nodes
- minikube node delete vignesh-vm-cluster-m02 -p vignesh-vm-cluster
- kubectl get pods -o wide
- kubectl get nodes
```
dhivyamalathirajasekaran$ kubectl get pods -o wide
NAME               READY   STATUS    RESTARTS   AGE    IP            NODE                     NOMINATED NODE   READINESS GATES
rs-handson-q4qjf   1/1     Running   0          2m9s   10.244.2.15   vignesh-vm-cluster-m03   <none>           <none>
rs-handson-srvdf   1/1     Running   0          84m    10.244.1.13   vignesh-vm-cluster-m02   <none>           <none>
rs-handson-wdmww   1/1     Running   0          84m    10.244.3.14   vignesh-vm-cluster-m04   <none>           <none>

dhivyamalathirajasekaran$ kubectl get nodes
NAME                     STATUS   ROLES           AGE     VERSION
vignesh-vm-cluster       Ready    control-plane   14d     v1.28.3
vignesh-vm-cluster-m02   Ready    <none>          6h30m   v1.28.3
vignesh-vm-cluster-m03   Ready    <none>          6h29m   v1.28.3
vignesh-vm-cluster-m04   Ready    <none>          6h28m   v1.28.3
vignesh-vm-cluster-m05   Ready    <none>          6h28m   v1.28.3

dhivyamalathirajasekaran$ minikube node delete vignesh-vm-cluster-m02 -p vignesh-vm-cluster
🔥  Deleting node vignesh-vm-cluster-m02 from cluster vignesh-vm-cluster
🔥  Deleting "vignesh-vm-cluster-m02" in hyperkit ...
💀  Node vignesh-vm-cluster-m02 was successfully deleted.

dhivyamalathirajasekaran$ kubectl get pods -o wide
NAME               READY   STATUS              RESTARTS   AGE     IP            NODE                     NOMINATED NODE   READINESS GATES
rs-handson-f2mrv   0/1     ContainerCreating   0          19s     <none>        vignesh-vm-cluster-m05   <none>           <none>
rs-handson-q4qjf   1/1     Running             0          4m26s   10.244.2.15   vignesh-vm-cluster-m03   <none>           <none>
rs-handson-wdmww   1/1     Running             0          87m     10.244.3.14   vignesh-vm-cluster-m04   <none>           <none>

dhivyamalathirajasekaran$ kubectl get nodes
NAME                     STATUS   ROLES           AGE     VERSION
vignesh-vm-cluster       Ready    control-plane   14d     v1.28.3
vignesh-vm-cluster-m03   Ready    <none>          6h38m   v1.28.3
vignesh-vm-cluster-m04   Ready    <none>          6h37m   v1.28.3
vignesh-vm-cluster-m05   Ready    <none>          6h37m   v1.28.3
```
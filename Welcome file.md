# KubeCTL commands
**Table of Contents**

[TOCM]

[TOC]

## nodes
```sh                
kubectl get nodes
kubectl describe node <node>

--Ex:------------------------------------------------
controlplane $ kubectl get nodes    
NAME           STATUS   ROLES           AGE   VERSION
controlplane   Ready    control-plane   33d   v1.29.0
node01         Ready    <none>          33d   v1.29.0
```
## namespace
- By default all the resources will be created under **default** namesapce
- Always set namespace before doing anything
```sh
kubectl get namespace
kubectl create namespace <ns>
kubectl config set-context --current --namespace=<ns>
kubectl delete namespace <ns>
kubectl describe namespace <ns>

--Ex:------------------------------------------------
controlplane $ kubectl get namespace
NAME                 STATUS   AGE
default              Active   33d
kube-node-lease      Active   33d
kube-public          Active   33d
kube-system          Active   33d
local-path-storage   Active   33d

--Ex:-------------------------------------------------
controlplane $ vi vignesh-namespace.yaml
```
```yaml
---
apiVersion: v1
kind: Namespace
metadata:
  name: vignesh-ns
```
```sh
--Ex:------------------------------------------------
controlplane $ kubectl create -f vignesh-namespace.yaml
namespace/vignesh-ns created

--Ex:------------------------------------------------
controlplane $ kubectl get ns
NAME                 STATUS   AGE
default              Active   33d
kube-node-lease      Active   33d
kube-public          Active   33d
kube-system          Active   33d
local-path-storage   Active   33d
vignesh-ns           Active   10s

--Ex:------------------------------------------------
controlplane $ kubectl config set-context --current --namespace=vignesh-ns
Context "kubernetes-admin@kubernetes" modified.

--Ex:------------------------------------------------
controlplane $ kubectl delete namespace vignesh-ns
namespace/vignesh-ns deleted
```
## pods
+ There are 12 system pods under **kube-system** namespace
+ 4 Important controlplane pods
    + kube-apiserver
    + etcd
    + kube-controller-manager
    + kube-scheduler
 + 6 other pods
	 + kube-proxy (2)
	 + coredns(2)
	 + canal(2)
	 + calico-kube-controllers
	 + local-path-provisioner
```sh
kubectl get pods
kubectl get pods -A
kubectl get pods -A -o wide
kubectl get pods -n vignesh-ns
kubectl get pods --selector <key=value> --namespace=vignesh-ns
kubectl create -f vignesh-pod.yaml
kubectl create -f vignesh-pod.yaml --namespace=vignesh-ns
kubectl describe pod <pod>
kubectl delete pods <pod>

--Ex:---------------------------------------------------------------------------------------------------------------------------------------------------------------
controlplane $ kubectl get pods 
No resources found in default namespace.

--Ex:---------------------------------------------------------------------------------------------------------------------------------------------------------------

controlplane $ kubectl get pods -A
NAMESPACE            NAME                                      READY   STATUS    RESTARTS       AGE
kube-system          calico-kube-controllers-9d57d8f49-jvt8w   1/1     Running   3 (8m2s ago)   33d
kube-system          canal-gjxwj                               2/2     Running   2 (8m1s ago)   33d
kube-system          canal-j6pwg                               2/2     Running   2 (8m2s ago)   33d
kube-system          coredns-86b698fbb6-8q542                  1/1     Running   1 (8m1s ago)   33d
kube-system          coredns-86b698fbb6-hqpmj                  1/1     Running   1 (8m1s ago)   33d
kube-system          etcd-controlplane                         1/1     Running   2 (8m2s ago)   33d
kube-system          kube-apiserver-controlplane               1/1     Running   2 (8m2s ago)   33d
kube-system          kube-controller-manager-controlplane      1/1     Running   2 (8m2s ago)   33d
kube-system          kube-proxy-85drq                          1/1     Running   2 (8m2s ago)   33d
kube-system          kube-proxy-lhxdd                          1/1     Running   1 (8m1s ago)   33d
kube-system          kube-scheduler-controlplane               1/1     Running   2 (8m2s ago)   33d
local-path-storage   local-path-provisioner-5d854bc5c4-h55kw   1/1     Running   2 (8m2s ago)   33d

--Ex:---------------------------------------------------------------------------------------------------------------------------------------------------------------

controlplane $ kubectl get pods -A -o wide
NAMESPACE            NAME                                      READY   STATUS    RESTARTS        AGE   IP            NODE           NOMINATED NODE   READINESS GATES
kube-system          calico-kube-controllers-9d57d8f49-jvt8w   1/1     Running   3 (8m14s ago)   33d   192.168.0.2   controlplane   <none>           <none>
kube-system          canal-gjxwj                               2/2     Running   2 (8m13s ago)   33d   172.30.2.2    node01         <none>           <none>
kube-system          canal-j6pwg                               2/2     Running   2 (8m14s ago)   33d   172.30.1.2    controlplane   <none>           <none>
kube-system          coredns-86b698fbb6-8q542                  1/1     Running   1 (8m13s ago)   33d   192.168.1.3   node01         <none>           <none>
kube-system          coredns-86b698fbb6-hqpmj                  1/1     Running   1 (8m13s ago)   33d   192.168.1.2   node01         <none>           <none>
kube-system          etcd-controlplane                         1/1     Running   2 (8m14s ago)   33d   172.30.1.2    controlplane   <none>           <none>
kube-system          kube-apiserver-controlplane               1/1     Running   2 (8m14s ago)   33d   172.30.1.2    controlplane   <none>           <none>
kube-system          kube-controller-manager-controlplane      1/1     Running   2 (8m14s ago)   33d   172.30.1.2    controlplane   <none>           <none>
kube-system          kube-proxy-85drq                          1/1     Running   2 (8m14s ago)   33d   172.30.1.2    controlplane   <none>           <none>
kube-system          kube-proxy-lhxdd                          1/1     Running   1 (8m13s ago)   33d   172.30.2.2    node01         <none>           <none>
kube-system          kube-scheduler-controlplane               1/1     Running   2 (8m14s ago)   33d   172.30.1.2    controlplane   <none>           <none>
local-path-storage   local-path-provisioner-5d854bc5c4-h55kw   1/1     Running   2 (8m14s ago)   33d   192.168.0.3   controlplane   <none>           <none>

--Ex:---------------------------------------------------------------------------------------------------------------------------------------------------------------
```
```yaml
---
apiVersion: v1
kind: Pod
metadata:
  name: vignesh-pod-1
  labels:
    app: bank-app
    type: front-end
spec:
  containers:
  - name: vignesh-pod-1
    image: nginx:1.14.2
    ports:
    - containerPort: 80
```
```sh
--Ex:---------------------------------------------------------------------------------------------------------------------------------------------------------------
controlplane $ vi vignesh-pod.yaml
controlplane $ kubectl create -f vignesh-pod.yaml  
pod/vignesh-pod-1 created

--Ex:---------------------------------------------------------------------------------------------------------------------------------------------------------------
controlplane $ kubectl get pods -A | grep vignesh-pod-1
NAMESPACE            NAME                                      READY   STATUS    RESTARTS       AGE
default              vignesh-pod-1                             0/1     ContainerCreating   0             5s

--Ex:---------------------------------------------------------------------------------------------------------------------------------------------------------------
controlplane $ kubectl create -f vignesh-pod.yaml 
pod/vignesh-pod-1 created
```
```yaml
---
apiVersion: v1
kind: Pod
metadata:
  name: vignesh-pod-2
  namespace: vignesh-ns
  labels:
    app: bank-db
    type: back-end
spec:
  containers:
  - name: vignesh-pod-2
    image: nginx:1.14.2
    ports:
    - containerPort: 80
```
```sh
--Ex:---------------------------------------------------------------------------------------------------------------------------------------------------------------
controlplane $ kubectl create -f vignesh-pod.yaml 
pod/vignesh-pod-1 created

--Ex:---------------------------------------------------------------------------------------------------------------------------------------------------------------
controlplane $ kubectl get pods -A | grep vignesh-pod
NAMESPACE            NAME                                      READY   STATUS    RESTARTS      AGE    IP            NODE           NOMINATED NODE   READINESS GATES
default              vignesh-pod-1                             1/1     Running   0             118s   192.168.1.4   node01         <none>           <none>
vignesh-ns           vignesh-pod-2                             1/1     Running   0             7s     192.168.1.5   node01         <none>           <none>

--Ex:---------------------------------------------------------------------------------------------------------------------------------------------------------------
controlplane $ kubectl get pods --selector app=bank-db --namespace=vignesh-ns
NAME            READY   STATUS    RESTARTS   AGE
vignesh-pod-2   1/1     Running   0          4m45s
```
## service
```sh
kubectl get services
kubectl create -f vignesh-service.yaml --namespace=vignesh-ns
kubectl delete service vignesh-service


--Ex:---------------------------------------------------------------------------------------------------------------------------------------------------------------
controlplane $ kubectl get services
No resources found in vignesh-ns namespace.

--Ex:---------------------------------------------------------------------------------------------------------------------------------------------------------------
controlplane $ kubectl config set-context --current --namespace=default
Context "kubernetes-admin@kubernetes" modified.

--Ex:---------------------------------------------------------------------------------------------------------------------------------------------------------------
controlplane $ kubectl get services
NAME         TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
kubernetes   ClusterIP   10.96.0.1    <none>        443/TCP   33d
```
```yaml
---
apiVersion: v1
kind: Service
metadata:
  name: vignesh-service
spec:
  ports:
    - targetPort: 80
      port: 80
  selector:
    app: bank-db
    type: back-end
```
```sh
--Ex:---------------------------------------------------------------------------------------------------------------------------------------------------------------
controlplane $ vi vignesh-service.yaml
controlplane $ kubectl create -f vignesh-service.yaml --namespace=vignesh-ns
service/vignesh-service created

--Ex:---------------------------------------------------------------------------------------------------------------------------------------------------------------
controlplane $ kubectl get service
NAME              TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)   AGE
kubernetes        ClusterIP   10.96.0.1       <none>        443/TCP   33d
vignesh-service   ClusterIP   10.96.234.232   <none>        80/TCP    6s

--Ex:---------------------------------------------------------------------------------------------------------------------------------------------------------------
controlplane $ kubectl get pods
NAME            READY   STATUS    RESTARTS   AGE
vignesh-pod-2   1/1     Running   0          38m

--Ex:---------------------------------------------------------------------------------------------------------------------------------------------------------------
controlplane $ kubectl config set-context --current --namespace=vignesh-ns
Context "kubernetes-admin@kubernetes" modified.

--Ex:---------------------------------------------------------------------------------------------------------------------------------------------------------------
controlplane $ kubectl get pods
NAME            READY   STATUS    RESTARTS   AGE
vignesh-pod-1   1/1     Running   0          40m

--Ex:---------------------------------------------------------------------------------------------------------------------------------------------------------------
controlplane $ kubectl get services
NAME              TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)   AGE
vignesh-service   ClusterIP   10.98.253.142   <none>        80/TCP    91s

controlplane $ curl http://10.98.253.142:80

--Ex:---------------------------------------------------------------------------------------------------------------------------------------------------------------
controlplane $ vi vignesh-service.yaml 
```
```yaml
---
apiVersion: v1
kind: Service
metadata:
  name: vignesh-service
spec:
  type: NodePort
  ports:
    - targetPort: 80
      port: 80
      nodePort: 32000
  selector:
    app: bank-db
    type: back-end
```
```sh
--Ex:---------------------------------------------------------------------------------------------------------------------------------------------------------------
controlplane $ kubectl delete service vignesh-service
service "vignesh-service" deleted

--Ex:---------------------------------------------------------------------------------------------------------------------------------------------------------------
controlplane $ kubectl create -f vignesh-service.yaml 
service/vignesh-service created

--Ex:---------------------------------------------------------------------------------------------------------------------------------------------------------------
controlplane $ kubectl get services
NAME              TYPE       CLUSTER-IP      EXTERNAL-IP   PORT(S)        AGE
vignesh-service   NodePort   10.98.125.192   <none>        80:32000/TCP   37s

controlplane $ curl http://10.98.125.192:80
```
<!--stackedit_data:
eyJoaXN0b3J5IjpbLTMzMjMwNTUxNCwtMTUyOTczNDk5MCwtOD
czNTIxNjc4LC0zNjcxNTA4OCwyMDgxODU5MTYyLDE4Mjg2MDc2
MTksLTE1MTg0NDEyNDIsLTE2NTg2Njk0MzUsLTE4MjU1MDUyNj
UsLTE3MDE2NDg5OV19
-->
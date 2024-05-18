- [Service Hands-On](#service-hands-on)
  * [List services](#list-services)
  * [Create ClusterIP Service](#create-clusterip-service)
  * [Access Nginx Application - Minikube](#access-nginx-application---minikube)
  * [Access Nginx Application - Worker / Pod](#access-nginx-application---worker---pod)
  * [Access Nginx Application - Worker / Pod (Multiple connections)](#access-nginx-application---worker---pod--multiple-connections-)
  * [Access Nginx Application - PortForwording](#access-nginx-application---portforwording)
  * [Create NodePort Service](#create-nodeport-service)
  * [Python App Demo using ClusterIP](#python-app-demo-using-clusterip)
  * [Python App Demo using NodePort](#python-app-demo-using-nodeport)

<small><i><a href='http://ecotrust-canada.github.io/markdown-toc/'>Table of contents generated with markdown-toc</a></i></small>


# Service Hands-On
```
1) List services
kubectl get services

2) Create ClusterIP Service
kubectl apply -f 04-services-handson/service-handson.yaml 
kubectl get svc
kubectl get all -o wide

4) Access Nginx Application - Minikube
minikube ssh
curl localhost:8080 * 2
kubectl logs <all pods>


5) Access Nginx Application Worker / Pod
kubectl exec -it deployment-handson-7d6d5d5d88-6j7mr -- bash
curl 10.107.231.120:8080
i=1; while [ "$i" -le 20 ]; do curl service-handson:8080; i=$(( i + 1 )); done; Continuously hit NodePort IP from the cluster will distribute the load 
kubectl logs <all pods>

6) Access Nginx Application - PortForwording
kubectl port-forward service/service-handson 8082:8080
kubectl get all -o wide
http://localhost:8082/ # Continuously hit, port-forwording IP will always select only one pod
kubectl logs <all pods>

7) Create NodePort Service
minikube ip
curl 192.168.64.3:32000
get all -o wide
minikube ssh
curl 10.107.231.120:8080 
curl 10.244.0.18:80

8) Python App Demo using ClusterIP
kubectl apply -f 04-services-handson/service-deployment-python-demo.yaml
kubectl get all -o wide
kubectl get pods -l app=sample-python-app -o wide
minikube ssh
curl -L 10.244.1.5:8000/demo


9) Python App Demo using NodePort
kubectl apply -f 04-services-handson/service-deployment-python-demo.yaml 
kubectl get all -o wide
curl -L 192.168.64.3:31000/demo
```


## List services
- kubectl get services
```
dhivyamalathirajasekaran$ kubectl get services

NAME         TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
kubernetes   ClusterIP   10.96.0.1    <none>        443/TCP   6h19m
```

## Create ClusterIP Service
- kubectl apply -f 04-services-handson/service-handson.yaml 
- kubectl get svc
```
dhivyamalathirajasekaran$ cat 04-services-handson/service-handson.yaml 
apiVersion: v1
kind: Service
metadata:
  name: service-handson
spec:
  selector:
    team: int
  type: ClusterIP
  ports:
  - name: service-handson
    protocol: TCP
    port: 8080
    targetPort: 80
    
dhivyamalathirajasekaran$ kubectl apply -f 04-services-handson/service-handson.yaml 
service/service-handson created

dhivyamalathirajasekaran$ kubectl get all
NAME                                      READY   STATUS    RESTARTS   AGE
pod/deployment-handson-7d6d5d5d88-6j7mr   1/1     Running   0          3h5m
pod/deployment-handson-7d6d5d5d88-n7bnv   1/1     Running   0          3h5m
pod/deployment-handson-7d6d5d5d88-p6wtw   1/1     Running   0          3h5m
pod/deployment-handson-7d6d5d5d88-vf4f6   1/1     Running   0          3h5m

NAME                      TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)    AGE
service/kubernetes        ClusterIP   10.96.0.1        <none>        443/TCP    6h23m
service/service-handson   ClusterIP   10.107.231.120   <none>        8080/TCP   14s

NAME                                 READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/deployment-handson   4/4     4            4           6h16m

NAME                                            DESIRED   CURRENT   READY   AGE
replicaset.apps/deployment-handson-5d4d56577c   0         0         0       3h23m
replicaset.apps/deployment-handson-5d54b9f9c    0         0         0       3h20m
replicaset.apps/deployment-handson-5d5c489556   0         0         0       3h34m
replicaset.apps/deployment-handson-645fdb6957   0         0         0       3h45m
replicaset.apps/deployment-handson-7d6d5d5d88   4         4         4       3h19m
replicaset.apps/deployment-handson-85b5ccd5f5   0         0         0       6h16m

dhivyamalathirajasekaran$ kubectl get svc
NAME              TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)    AGE
kubernetes        ClusterIP   10.96.0.1        <none>        443/TCP    6h27m
service-handson   ClusterIP   10.107.231.120   <none>        8080/TCP   3m48s
```

## Access Nginx Application - Minikube
- minikube ssh
- curl localhost:8080
- kubectl logs deployment-handson-7d6d5d5d88-n7bnv
- kubectl logs deployment-handson-7d6d5d5d88-6j7mr
```
dhivyamalathirajasekaran$ minikube ssh
                         _             _            
            _         _ ( )           ( )           
  ___ ___  (_)  ___  (_)| |/')  _   _ | |_      __  
/' _ ` _ `\| |/' _ `\| || , <  ( ) ( )| '_`\  /'__`\
| ( ) ( ) || || ( ) || || |\`\ | (_) || |_) )(  ___/
(_) (_) (_)(_)(_) (_)(_)(_) (_)`\___/'(_,__/'`\____)


$ curl 10.107.231.120:8080
SUCCESS

$ curl 10.107.231.120:8080
SUCCESS

dhivyamalathirajasekaran$ kubectl get nodes -o wide
NAME                     STATUS   ROLES           AGE   VERSION   INTERNAL-IP    EXTERNAL-IP   OS-IMAGE               KERNEL-VERSION   CONTAINER-RUNTIME
vignesh-vm-cluster       Ready    control-plane   14d   v1.28.3   192.168.64.3   <none>        Buildroot 2021.02.12   5.10.57          docker://24.0.7
vignesh-vm-cluster-m03   Ready    <none>          14h   v1.28.3   192.168.64.5   <none>        Buildroot 2021.02.12   5.10.57          docker://24.0.7
vignesh-vm-cluster-m04   Ready    <none>          14h   v1.28.3   192.168.64.6   <none>        Buildroot 2021.02.12   5.10.57          docker://24.0.7
vignesh-vm-cluster-m05   Ready    <none>          14h   v1.28.3   192.168.64.7   <none>        Buildroot 2021.02.12   5.10.57          docker://24.0.7

dhivyamalathirajasekaran$ kubectl logs deployment-handson-7d6d5d5d88-n7bnv
192.168.64.3 - - [04/May/2024:19:49:16 +0000] "GET / HTTP/1.1" 200 612 "-" "curl/7.79.1" "-"

dhivyamalathirajasekaran$ kubectl logs deployment-handson-7d6d5d5d88-6j7mr
192.168.64.3 - - [04/May/2024:19:49:18 +0000] "GET / HTTP/1.1" 200 612 "-" "curl/7.79.1" "-"
```

## Access Nginx Application - Worker / Pod
- kubectl exec -it deployment-handson-7d6d5d5d88-6j7mr -- bash
- curl 10.107.231.120:8080
- kubectl logs deployment-handson-7d6d5d5d88-n7bnv
- kubectl logs deployment-handson-7d6d5d5d88-6j7mr
```
dhivyamalathirajasekaran$ kubectl exec -it deployment-handson-7d6d5d5d88-6j7mr -- bash
root@deployment-handson-7d6d5d5d88-6j7mr:/# curl 10.107.231.120:8080
SUCCESS

dhivyamalathirajasekaran$ kubectl get pods -o wide
NAME                                  READY   STATUS    RESTARTS   AGE     IP            NODE                     NOMINATED NODE   READINESS GATES
deployment-handson-7d6d5d5d88-6j7mr   1/1     Running   0          3h29m   10.244.0.16   vignesh-vm-cluster       <none>           <none>
deployment-handson-7d6d5d5d88-n7bnv   1/1     Running   0          3h30m   10.244.3.23   vignesh-vm-cluster-m04   <none>           <none>
deployment-handson-7d6d5d5d88-p6wtw   1/1     Running   0          3h30m   10.244.2.24   vignesh-vm-cluster-m03   <none>           <none>
deployment-handson-7d6d5d5d88-vf4f6   1/1     Running   0          3h30m   10.244.4.17   vignesh-vm-cluster-m05   <none>           <none>

dhivyamalathirajasekaran$ kubectl logs deployment-handson-7d6d5d5d88-n7bnv
192.168.64.3 - - [04/May/2024:19:49:16 +0000] "GET / HTTP/1.1" 200 612 "-" "curl/7.79.1" "-"
10.244.0.16 - - [04/May/2024:19:52:39 +0000] "GET / HTTP/1.1" 200 612 "-" "curl/7.64.0" "-"
```

## Access Nginx Application - Worker / Pod (Multiple connections)
- kubectl exec -it deployment-handson-7d6d5d5d88-6j7mr -- bash
- i=1; while [ "$i" -le 20 ]; do curl service-handson:8080; i=$(( i + 1 )); done;
- kubectl logs deployment-handson-7d6d5d5d88-n7bnv
- kubectl logs deployment-handson-7d6d5d5d88-6j7mr
```
dhivyamalathirajasekaran$ kubectl exec -it deployment-handson-7d6d5d5d88-6j7mr -- bash
root@deployment-handson-7d6d5d5d88-6j7mr:/# i=1; while [ "$i" -le 20 ]; do curl service-handson:8080; i=$(( i + 1 )); done;
SUCCESS
.
.
.
SUCCESS

dhivyamalathirajasekaran$ kubectl get pods
NAME                                  READY   STATUS    RESTARTS   AGE
deployment-handson-7d6d5d5d88-6j7mr   1/1     Running   0          3h40m
deployment-handson-7d6d5d5d88-n7bnv   1/1     Running   0          3h41m
deployment-handson-7d6d5d5d88-p6wtw   1/1     Running   0          3h41m
deployment-handson-7d6d5d5d88-vf4f6   1/1     Running   0          3h41m

dhivyamalathirajasekaran$ kubectl logs deployment-handson-7d6d5d5d88-6j7mr
192.168.64.3 - - [04/May/2024:19:49:18 +0000] "GET / HTTP/1.1" 200 612 "-" "curl/7.79.1" "-"
10.244.0.1 - - [04/May/2024:20:20:17 +0000] "GET / HTTP/1.1" 200 612 "-" "curl/7.64.0" "-"
10.244.0.1 - - [04/May/2024:20:20:17 +0000] "GET / HTTP/1.1" 200 612 "-" "curl/7.64.0" "-"
10.244.0.1 - - [04/May/2024:20:20:17 +0000] "GET / HTTP/1.1" 200 612 "-" "curl/7.64.0" "-"
10.244.0.1 - - [04/May/2024:20:20:17 +0000] "GET / HTTP/1.1" 200 612 "-" "curl/7.64.0" "-"

dhivyamalathirajasekaran$ kubectl logs deployment-handson-7d6d5d5d88-n7bnv
192.168.64.3 - - [04/May/2024:19:49:16 +0000] "GET / HTTP/1.1" 200 612 "-" "curl/7.79.1" "-"
10.244.0.16 - - [04/May/2024:19:52:39 +0000] "GET / HTTP/1.1" 200 612 "-" "curl/7.64.0" "-"
10.244.0.16 - - [04/May/2024:20:20:17 +0000] "GET / HTTP/1.1" 200 612 "-" "curl/7.64.0" "-"
10.244.0.16 - - [04/May/2024:20:20:17 +0000] "GET / HTTP/1.1" 200 612 "-" "curl/7.64.0" "-"
10.244.0.16 - - [04/May/2024:20:20:17 +0000] "GET / HTTP/1.1" 200 612 "-" "curl/7.64.0" "-"
10.244.0.16 - - [04/May/2024:20:20:17 +0000] "GET / HTTP/1.1" 200 612 "-" "curl/7.64.0" "-"
10.244.0.16 - - [04/May/2024:20:20:17 +0000] "GET / HTTP/1.1" 200 612 "-" "curl/7.64.0" "-"
10.244.0.16 - - [04/May/2024:20:20:17 +0000] "GET / HTTP/1.1" 200 612 "-" "curl/7.64.0" "-"
10.244.0.16 - - [04/May/2024:20:20:17 +0000] "GET / HTTP/1.1" 200 612 "-" "curl/7.64.0" "-"

dhivyamalathirajasekaran$ kubectl logs deployment-handson-7d6d5d5d88-p6wtw
10.244.0.16 - - [04/May/2024:20:20:17 +0000] "GET / HTTP/1.1" 200 612 "-" "curl/7.64.0" "-"
10.244.0.16 - - [04/May/2024:20:20:17 +0000] "GET / HTTP/1.1" 200 612 "-" "curl/7.64.0" "-"

dhivyamalathirajasekaran$ kubectl logs deployment-handson-7d6d5d5d88-vf4f6
10.244.0.16 - - [04/May/2024:20:20:17 +0000] "GET / HTTP/1.1" 200 612 "-" "curl/7.64.0" "-"
10.244.0.16 - - [04/May/2024:20:20:17 +0000] "GET / HTTP/1.1" 200 612 "-" "curl/7.64.0" "-"
10.244.0.16 - - [04/May/2024:20:20:17 +0000] "GET / HTTP/1.1" 200 612 "-" "curl/7.64.0" "-"
10.244.0.16 - - [04/May/2024:20:20:17 +0000] "GET / HTTP/1.1" 200 612 "-" "curl/7.64.0" "-"
10.244.0.16 - - [04/May/2024:20:20:17 +0000] "GET / HTTP/1.1" 200 612 "-" "curl/7.64.0" "-"
10.244.0.16 - - [04/May/2024:20:20:17 +0000] "GET / HTTP/1.1" 200 612 "-" "curl/7.64.0" "-"
10.244.0.16 - - [04/May/2024:20:20:17 +0000] "GET / HTTP/1.1" 200 612 "-" "curl/7.64.0" "-"
```

## Access Nginx Application - PortForwording
- kubectl port-forward service/service-handson 8082:8080
- http://localhost:8082/
```
dhivyamalathirajasekaran$ kubectl port-forward service/service-handson 8082:8080
Forwarding from 127.0.0.1:8082 -> 80
Forwarding from [::1]:8082 -> 80
Handling connection for 8082

dhivyamalathirajasekaran$ kubectl logs deployment-handson-7d6d5d5d88-p6wtw
127.0.0.1 - - [04/May/2024:19:56:48 +0000] "GET / HTTP/1.1" 200 612 "-" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36" "-"
2024/05/04 19:56:48 [error] 30#30: *1 open() "/usr/share/nginx/html/favicon.ico" failed (2: No such file or directory), client: 127.0.0.1, server: localhost, request: "GET /favicon.ico HTTP/1.1", host: "localhost:8082", referrer: "http://localhost:8082/"
127.0.0.1 - - [04/May/2024:19:56:48 +0000] "GET /favicon.ico HTTP/1.1" 404 555 "http://localhost:8082/" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36" "-"
127.0.0.1 - - [04/May/2024:20:06:54 +0000] "GET / HTTP/1.1" 304 0 "-" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36" "-"
127.0.0.1 - - [04/May/2024:20:06:59 +0000] "GET / HTTP/1.1" 304 0 "-" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36" "-"
127.0.0.1 - - [04/May/2024:20:07:01 +0000] "GET / HTTP/1.1" 304 0 "-" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36" "-"
127.0.0.1 - - [04/May/2024:20:07:02 +0000] "GET / HTTP/1.1" 304 0 "-" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36" "-"
127.0.0.1 - - [04/May/2024:20:07:03 +0000] "GET / HTTP/1.1" 304 0 "-" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36" "-"
127.0.0.1 - - [04/May/2024:20:07:04 +0000] "GET / HTTP/1.1" 304 0 "-" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36" "-"
127.0.0.1 - - [04/May/2024:20:07:05 +0000] "GET / HTTP/1.1" 304 0 "-" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36" "-"
```

## Create NodePort Service
- minikube ip
- curl 192.168.64.3:32000
- get all -o wide
- minikube ssh
- curl 10.107.231.120:8080 
- curl 10.244.0.18:80
```
dhivyamalathirajasekaran$ cat 04-services-handson/service-handson-np.yaml 
apiVersion: v1
kind: Service
metadata:
  name: service-handson
  labels:
    team: int
spec:
  selector:
    team: int
  type: NodePort
  ports:
  - name: service-handson-ngx
    protocol: TCP
    port: 8080
    targetPort: 80
    nodePort: 32000

dhivyamalathirajasekaran$ minikube ip
192.168.64.3

dhivyamalathirajasekaran$ curl 192.168.64.3:32000
SUCCESS

dhivyamalathirajasekaran$ kubectl get all -o wide
NAME                                      READY   STATUS    RESTARTS        AGE   IP            NODE                     NOMINATED NODE   READINESS GATES
pod/deployment-handson-7d6d5d5d88-6j7mr   1/1     Running   1 (4h22m ago)   19h   10.244.0.18   vignesh-vm-cluster       <none>           <none>
pod/deployment-handson-7d6d5d5d88-n7bnv   1/1     Running   0               19h   10.244.3.23   vignesh-vm-cluster-m04   <none>           <none>
pod/deployment-handson-7d6d5d5d88-p6wtw   1/1     Running   0               19h   10.244.2.24   vignesh-vm-cluster-m03   <none>           <none>
pod/deployment-handson-7d6d5d5d88-vf4f6   1/1     Running   0               19h   10.244.4.17   vignesh-vm-cluster-m05   <none>           <none>

NAME                      TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)          AGE   SELECTOR
service/kubernetes        ClusterIP   10.96.0.1        <none>        443/TCP          22h   <none>
service/service-handson   NodePort    10.107.231.120   <none>        8080:32000/TCP   16h   team=int

NAME                                 READY   UP-TO-DATE   AVAILABLE   AGE   CONTAINERS               IMAGES       SELECTOR
deployment.apps/deployment-handson   4/4     4            4           22h   deployment-handson-con   nginx:1.18   team=int

NAME                                            DESIRED   CURRENT   READY   AGE   CONTAINERS               IMAGES         SELECTOR
replicaset.apps/deployment-handson-5d4d56577c   0         0         0       19h   deployment-handson-con   nginx:1.20     pod-template-hash=5d4d56577c,team=int
replicaset.apps/deployment-handson-5d54b9f9c    0         0         0       19h   deployment-handson-con   nginx:1.19     pod-template-hash=5d54b9f9c,team=int
replicaset.apps/deployment-handson-5d5c489556   0         0         0       19h   deployment-handson-con   nginx:1.21     pod-template-hash=5d5c489556,team=int
replicaset.apps/deployment-handson-645fdb6957   0         0         0       19h   deployment-handson-con   nginx:1.21.3   pod-template-hash=645fdb6957,team=int
replicaset.apps/deployment-handson-7d6d5d5d88   4         4         4       19h   deployment-handson-con   nginx:1.18     pod-template-hash=7d6d5d5d88,team=int
replicaset.apps/deployment-handson-85b5ccd5f5   0         0         0       22h   deployment-handson-con   nginx:latest   pod-template-hash=85b5ccd5f5,team=int

dhivyamalathirajasekaran$ minikube ssh
                         _             _            
            _         _ ( )           ( )           
  ___ ___  (_)  ___  (_)| |/')  _   _ | |_      __  
/' _ ` _ `\| |/' _ `\| || , <  ( ) ( )| '_`\  /'__`\
| ( ) ( ) || || ( ) || || |\`\ | (_) || |_) )(  ___/
(_) (_) (_)(_)(_) (_)(_)(_) (_)`\___/'(_,__/'`\____)


$ curl 10.107.231.120:8080 
SUCCESS

$ curl 10.244.0.18:80
SUCCESS
```

## Python App Demo using ClusterIP
- kubectl apply -f 04-services-handson/service-deployment-python-demo.yaml
- kubectl get all -o wide
```
dhivyamalathirajasekaran$ cat 04-services-handson/service-deployment-python-demo.yaml 
apiVersion: apps/v1
kind: Deployment
metadata:
  name: sample-python-app
  labels:
    app: sample-python-app
spec:
  replicas: 2
  selector:
    matchLabels:
      app: sample-python-app
  template:
    metadata:
      labels:
        app: sample-python-app
    spec:
      containers:
      - name: sample-python-app
        image: abhishekf5/python-sample-app-demo:v1
        ports:
        - containerPort: 8000

dhivyamalathirajasekaran$ kubectl apply -f 04-services-handson/service-deployment-python-demo.yaml 
deployment.apps/sample-python-app created

dhivyamalathirajasekaran$ kubectl get all -o wide
NAME                                      READY   STATUS              RESTARTS       AGE     IP           NODE                     NOMINATED NODE   READINESS GATES
pod/deployment-handson-7d6d5d5d88-6bcrq   1/1     Running             0              83s     10.244.1.4   vignesh-vm-cluster-m03   <none>           <none>
pod/deployment-handson-7d6d5d5d88-6j7mr   1/1     Running             2 (4m5s ago)   25h     10.244.0.3   vignesh-vm-cluster       <none>           <none>
pod/deployment-handson-7d6d5d5d88-n2vkp   1/1     Running             0              83s     10.244.2.2   vignesh-vm-cluster-m04   <none>           <none>
pod/deployment-handson-7d6d5d5d88-wcncb   1/1     Running             0              2m15s   10.244.1.2   vignesh-vm-cluster-m03   <none>           <none>
pod/sample-python-app-7ddbdd9945-fmf4z    0/1     ContainerCreating   0              67s     <none>       vignesh-vm-cluster-m03   <none>           <none>
pod/sample-python-app-7ddbdd9945-lcxmr    0/1     ContainerCreating   0              67s     <none>       vignesh-vm-cluster-m04   <none>           <none>

NAME                      TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)                         AGE   SELECTOR
service/kubernetes        ClusterIP   10.96.0.1        <none>        443/TCP                         28h   <none>
service/service-handson   NodePort    10.107.231.120   <none>        8080:32000/TCP,8081:32001/TCP   22h   team=int

NAME                                 READY   UP-TO-DATE   AVAILABLE   AGE   CONTAINERS               IMAGES                                 SELECTOR
deployment.apps/deployment-handson   4/4     4            4           28h   deployment-handson-con   nginx:1.18                             team=int
deployment.apps/sample-python-app    0/2     2            0           67s   sample-python-app        abhishekf5/python-sample-app-demo:v1   app=sample-python-app

NAME                                            DESIRED   CURRENT   READY   AGE   CONTAINERS               IMAGES                                 SELECTOR
replicaset.apps/deployment-handson-5d4d56577c   0         0         0       25h   deployment-handson-con   nginx:1.20                             pod-template-hash=5d4d56577c,team=int
replicaset.apps/deployment-handson-5d54b9f9c    0         0         0       25h   deployment-handson-con   nginx:1.19                             pod-template-hash=5d54b9f9c,team=int
replicaset.apps/deployment-handson-5d5c489556   0         0         0       26h   deployment-handson-con   nginx:1.21                             pod-template-hash=5d5c489556,team=int
replicaset.apps/deployment-handson-645fdb6957   0         0         0       26h   deployment-handson-con   nginx:1.21.3                           pod-template-hash=645fdb6957,team=int
replicaset.apps/deployment-handson-7d6d5d5d88   4         4         4       25h   deployment-handson-con   nginx:1.18                             pod-template-hash=7d6d5d5d88,team=int
replicaset.apps/deployment-handson-85b5ccd5f5   0         0         0       28h   deployment-handson-con   nginx:latest                           pod-template-hash=85b5ccd5f5,team=int
replicaset.apps/sample-python-app-7ddbdd9945    2         2         0       67s   sample-python-app        abhishekf5/python-sample-app-demo:v1   app=sample-python-app,pod-template-hash=7ddbdd9945


dhivyamalathirajasekaran$ kubectl get all -o wide
NAME                                      READY   STATUS    RESTARTS        AGE     IP           NODE                     NOMINATED NODE   READINESS GATES
pod/deployment-handson-7d6d5d5d88-6bcrq   1/1     Running   0               2m15s   10.244.1.4   vignesh-vm-cluster-m03   <none>           <none>
pod/deployment-handson-7d6d5d5d88-6j7mr   1/1     Running   2 (4m57s ago)   25h     10.244.0.3   vignesh-vm-cluster       <none>           <none>
pod/deployment-handson-7d6d5d5d88-n2vkp   1/1     Running   0               2m15s   10.244.2.2   vignesh-vm-cluster-m04   <none>           <none>
pod/deployment-handson-7d6d5d5d88-wcncb   1/1     Running   0               3m7s    10.244.1.2   vignesh-vm-cluster-m03   <none>           <none>
pod/sample-python-app-7ddbdd9945-fmf4z    1/1     Running   0               119s    10.244.1.5   vignesh-vm-cluster-m03   <none>           <none>
pod/sample-python-app-7ddbdd9945-lcxmr    1/1     Running   0               119s    10.244.2.4   vignesh-vm-cluster-m04   <none>           <none>

NAME                      TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)                         AGE   SELECTOR
service/kubernetes        ClusterIP   10.96.0.1        <none>        443/TCP                         28h   <none>
service/service-handson   NodePort    10.107.231.120   <none>        8080:32000/TCP,8081:32001/TCP   22h   team=int

NAME                                 READY   UP-TO-DATE   AVAILABLE   AGE    CONTAINERS               IMAGES                                 SELECTOR
deployment.apps/deployment-handson   4/4     4            4           28h    deployment-handson-con   nginx:1.18                             team=int
deployment.apps/sample-python-app    2/2     2            2           119s   sample-python-app        abhishekf5/python-sample-app-demo:v1   app=sample-python-app

NAME                                            DESIRED   CURRENT   READY   AGE    CONTAINERS               IMAGES                                 SELECTOR
replicaset.apps/deployment-handson-5d4d56577c   0         0         0       25h    deployment-handson-con   nginx:1.20                             pod-template-hash=5d4d56577c,team=int
replicaset.apps/deployment-handson-5d54b9f9c    0         0         0       25h    deployment-handson-con   nginx:1.19                             pod-template-hash=5d54b9f9c,team=int
replicaset.apps/deployment-handson-5d5c489556   0         0         0       26h    deployment-handson-con   nginx:1.21                             pod-template-hash=5d5c489556,team=int
replicaset.apps/deployment-handson-645fdb6957   0         0         0       26h    deployment-handson-con   nginx:1.21.3                           pod-template-hash=645fdb6957,team=int
replicaset.apps/deployment-handson-7d6d5d5d88   4         4         4       25h    deployment-handson-con   nginx:1.18                             pod-template-hash=7d6d5d5d88,team=int
replicaset.apps/deployment-handson-85b5ccd5f5   0         0         0       28h    deployment-handson-con   nginx:latest                           pod-template-hash=85b5ccd5f5,team=int
replicaset.apps/sample-python-app-7ddbdd9945    2         2         2       119s   sample-python-app        abhishekf5/python-sample-app-demo:v1   app=sample-python-app,pod-template-hash=7ddbdd9945

dhivyamalathirajasekaran$ kubectl get pods -l app=sample-python-app -o wide
NAME                                 READY   STATUS    RESTARTS   AGE     IP           NODE                     NOMINATED NODE   READINESS GATES
sample-python-app-7ddbdd9945-fmf4z   1/1     Running   0          9m33s   10.244.1.5   vignesh-vm-cluster-m03   <none>           <none>
sample-python-app-7ddbdd9945-lcxmr   1/1     Running   0          9m33s   10.244.2.4   vignesh-vm-cluster-m04   <none>           <none>
(base) Dhivyamalathis-MacBook-Pro:Kubernetes dhivyamalathirajasekaran$ minikube ssh
                         _             _            
            _         _ ( )           ( )           
  ___ ___  (_)  ___  (_)| |/')  _   _ | |_      __  
/' _ ` _ `\| |/' _ `\| || , <  ( ) ( )| '_`\  /'__`\
| ( ) ( ) || || ( ) || || |\`\ | (_) || |_) )(  ___/
(_) (_) (_)(_)(_) (_)(_)(_) (_)`\___/'(_,__/'`\____)

$ curl -L 10.244.1.5:8000/demo
SUCCESS
```

## Python App Demo using NodePort
- kubectl apply -f 04-services-handson/service-deployment-python-demo.yaml 
- kubectl get all -o wide
- curl -L 192.168.64.3:31000/demo
```
dhivyamalathirajasekaran$ cat 04-services-handson/service-deployment-python-demo.yaml 
apiVersion: apps/v1
kind: Deployment
metadata:
  name: sample-python-app
  labels:
    app: sample-python-app
spec:
  replicas: 2
  selector:
    matchLabels:
      app: sample-python-app
  template:
    metadata:
      labels:
        app: sample-python-app
    spec:
      containers:
      - name: sample-python-app
        image: abhishekf5/python-sample-app-demo:v1
        ports:
        - containerPort: 8000

---
apiVersion: v1
kind: Service
metadata:
  name: sample-python-app-service
spec:
  selector:
    app: sample-python-app
  type: NodePort
  ports:
  - name: sample-python-app-service
    protocol: TCP
    port: 8888
    targetPort: 8000
    nodePort: 31000

dhivyamalathirajasekaran$ kubectl apply -f 04-services-handson/service-deployment-python-demo.yaml 
deployment.apps/sample-python-app unchanged
service/sample-python-app-service created

dhivyamalathirajasekaran$ kubectl get all -o wide
NAME                                      READY   STATUS    RESTARTS      AGE   IP           NODE                     NOMINATED NODE   READINESS GATES
pod/deployment-handson-7d6d5d5d88-6bcrq   1/1     Running   0             25m   10.244.1.4   vignesh-vm-cluster-m03   <none>           <none>
pod/deployment-handson-7d6d5d5d88-6j7mr   1/1     Running   2 (27m ago)   25h   10.244.0.3   vignesh-vm-cluster       <none>           <none>
pod/deployment-handson-7d6d5d5d88-n2vkp   1/1     Running   0             25m   10.244.2.2   vignesh-vm-cluster-m04   <none>           <none>
pod/deployment-handson-7d6d5d5d88-wcncb   1/1     Running   0             26m   10.244.1.2   vignesh-vm-cluster-m03   <none>           <none>
pod/sample-python-app-7ddbdd9945-fmf4z    1/1     Running   0             24m   10.244.1.5   vignesh-vm-cluster-m03   <none>           <none>
pod/sample-python-app-7ddbdd9945-lcxmr    1/1     Running   0             24m   10.244.2.4   vignesh-vm-cluster-m04   <none>           <none>

NAME                                TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)                         AGE     SELECTOR
service/kubernetes                  ClusterIP   10.96.0.1        <none>        443/TCP                         29h     <none>
service/sample-python-app-service   NodePort    10.110.191.12    <none>        8888:31000/TCP                  3m56s   app=sample-python-app
service/service-handson             NodePort    10.107.231.120   <none>        8080:32000/TCP,8081:32001/TCP   22h     team=int

NAME                                 READY   UP-TO-DATE   AVAILABLE   AGE   CONTAINERS               IMAGES                                 SELECTOR
deployment.apps/deployment-handson   4/4     4            4           29h   deployment-handson-con   nginx:1.18                             team=int
deployment.apps/sample-python-app    2/2     2            2           24m   sample-python-app        abhishekf5/python-sample-app-demo:v1   app=sample-python-app

NAME                                            DESIRED   CURRENT   READY   AGE   CONTAINERS               IMAGES                                 SELECTOR
replicaset.apps/deployment-handson-5d4d56577c   0         0         0       26h   deployment-handson-con   nginx:1.20                             pod-template-hash=5d4d56577c,team=int
replicaset.apps/deployment-handson-5d54b9f9c    0         0         0       26h   deployment-handson-con   nginx:1.19                             pod-template-hash=5d54b9f9c,team=int
replicaset.apps/deployment-handson-5d5c489556   0         0         0       26h   deployment-handson-con   nginx:1.21                             pod-template-hash=5d5c489556,team=int
replicaset.apps/deployment-handson-645fdb6957   0         0         0       26h   deployment-handson-con   nginx:1.21.3                           pod-template-hash=645fdb6957,team=int
replicaset.apps/deployment-handson-7d6d5d5d88   4         4         4       26h   deployment-handson-con   nginx:1.18                             pod-template-hash=7d6d5d5d88,team=int
replicaset.apps/deployment-handson-85b5ccd5f5   0         0         0       29h   deployment-handson-con   nginx:latest                           pod-template-hash=85b5ccd5f5,team=int
replicaset.apps/sample-python-app-7ddbdd9945    2         2         2       24m   sample-python-app        abhishekf5/python-sample-app-demo:v1   app=sample-python-app,pod-template-hash=7ddbdd9945

dhivyamalathirajasekaran$ curl -L 192.168.64.3:31000/demo
SUCCESS
```
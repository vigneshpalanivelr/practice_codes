- [Deployment Hands-On](#deployment-hands-on)
  * [Delete all the exsisting resources](#delete-all-the-exsisting-resources)
  * [Checl all the resources and get App name for deployment](#checl-all-the-resources-and-get-app-name-for-deployment)
  * [Create Deployment YAMl and Apply](#create-deployment-yaml-and-apply)
  * [Update replicas in deployment YAML and apply](#update-replicas-in-deployment-yaml-and-apply)
  * [Update replicas in CLI](#update-replicas-in-cli)
  * [Apply deployment YAML again](#apply-deployment-yaml-again)
  * [Check history of replica sets](#check-history-of-replica-sets)
  * [Change the image version to 1.21.3](#change-the-image-version-to-1213)
  * [Change the image version to 1.20 via CLI](#change-the-image-version-to-120-via-cli)
  * [History of deployments](#history-of-deployments)
  * [Change the image version to 1.20 via CLI with repord](#change-the-image-version-to-120-via-cli-with-repord)
  * [Add Anotation in YAML and Apply](#add-anotation-in-yaml-and-apply)
  * [Undo the rollout and check](#undo-the-rollout-and-check)
  * [Rollout status](#rollout-status)

<small><i><a href='http://ecotrust-canada.github.io/markdown-toc/'>Table of contents generated with markdown-toc</a></i></small>


# Deployment Hands-On
```
1) Delete all the exsisting resources
kubectl delete all --all

2) Checl all the resources and get App name for deployment
kubectl get all
kubectl api-resources | grep dep

3) Create Deployment YAMl and Apply
kubectl apply -f 03-deployment-handson/deployment-handson.yaml 
kubectl get all -owide

4) Update replicas in deployment YAML and apply
kubectl get all -owide

5) Update replicas in CLI
kubectl scale --replicas=2 deployment/deployment-handson
kubectl get all -owide

7) Apply deployment YAML again
8) Check history of replica sets
kubectl get rs

9) Change the image version to 1.21.3
kubectl get rs

10) Change the image version to 1.20 via CLI
kubectl set image deployment/deployment-handson deployment-handson-con=nginx:1.20

11) History of deployments
kubectl rollout history deployments

12) Change the image version to 1.20 via CLI with repord
kubectl set image deployment/vignesh-deployment vignesh-con=nginx:1.19 --record
kubectl rollout history deployments

13) Add Anotation in YAML and Apply
kubectl apply -f 03-deployment-handson/deployment-handson.yaml
kubectl rollout history deployments

14) Undo the rollout and check
kubectl rollout undo deployment --to-revision=6
kubectl get all -o wide

15) Status of the rollout
kubectl rollout status deployment/deployment-handson
```
-------

## Delete all the exsisting resources
- kubectl delete all --all
```
dhivyamalathirajasekaran$ kubectl delete all --all
pod "rs-handson-f2mrv" deleted
pod "rs-handson-q4qjf" deleted
pod "rs-handson-wdmww" deleted
service "kubernetes" deleted
replicaset.apps "rs-handson" deleted
```

## Checl all the resources and get App name for deployment
- kubectl get all
- kubectl api-resources | grep dep
```
dhivyamalathirajasekaran$ kubectl get all
NAME                 TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
service/kubernetes   ClusterIP   10.96.0.1    <none>        443/TCP   26s

dhivyamalathirajasekaran$ kubectl api-resources | grep dep
deployments                       deploy       apps/v1                                true         Deployment
```

## Create Deployment YAMl and Apply
- kubectl apply -f 03-deployment-handson/deployment-handson.yaml 
- kubectl get all -owide
```
dhivyamalathirajasekaran$ cat 03-deployment-handson/deployment-handson.yaml 
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name:  deployment-handson
  namespace: default
  labels:
    team: int
spec:
  replicas: 3
  selector:
    matchLabels:
      team: int
  template:
    metadata:
      name: deployment-handson-pod
      labels:
        team: int
    spec:
      containers:
      - name:  deployment-handson-con
        image:  nginx:latest
        ports:
        - containerPort: 80

dhivyamalathirajasekaran$ kubectl apply -f 03-deployment-handson/deployment-handson.yaml 
deployment.apps/deployment-handson created

dhivyamalathirajasekaran$ kubectl get all -owide
NAME                                      READY   STATUS    RESTARTS   AGE   IP            NODE                     NOMINATED NODE   READINESS GATES
pod/deployment-handson-85b5ccd5f5-5kjxz   1/1     Running   0          95s   10.244.4.10   vignesh-vm-cluster-m05   <none>           <none>
pod/deployment-handson-85b5ccd5f5-ch99x   1/1     Running   0          95s   10.244.3.16   vignesh-vm-cluster-m04   <none>           <none>
pod/deployment-handson-85b5ccd5f5-lz9r8   1/1     Running   0          95s   10.244.2.17   vignesh-vm-cluster-m03   <none>           <none>

NAME                 TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE     SELECTOR
service/kubernetes   ClusterIP   10.96.0.1    <none>        443/TCP   8m23s   <none>

NAME                                 READY   UP-TO-DATE   AVAILABLE   AGE   CONTAINERS               IMAGES         SELECTOR
deployment.apps/deployment-handson   3/3     3            3           96s   deployment-handson-con   nginx:latest   team=int

NAME                                            DESIRED   CURRENT   READY   AGE   CONTAINERS               IMAGES         SELECTOR
replicaset.apps/deployment-handson-85b5ccd5f5   3         3         3       96s   deployment-handson-con   nginx:latest   pod-template-hash=85b5ccd5f5,team=int
```

## Update replicas in deployment YAML and apply
- kubectl get all -owide
```
dhivyamalathirajasekaran$ cat 03-deployment-handson/deployment-handson.yaml 
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name:  deployment-handson
  namespace: default
  labels:
    team: int
spec:
  replicas: 4
  selector:
    matchLabels:
      team: int
  template:
    metadata:
      name: deployment-handson-pod
      labels:
        team: int
    spec:
      containers:
      - name:  deployment-handson-con
        image:  nginx:latest
        ports:
        - containerPort: 80

dhivyamalathirajasekaran$ kubectl apply -f 03-deployment-handson/deployment-handson.yaml 
deployment.apps/deployment-handson configured

dhivyamalathirajasekaran$ kubectl get all -owide
NAME                                      READY   STATUS              RESTARTS   AGE    IP            NODE                     NOMINATED NODE   READINESS GATES
pod/deployment-handson-85b5ccd5f5-5kjxz   1/1     Running             0          111s   10.244.4.10   vignesh-vm-cluster-m05   <none>           <none>
pod/deployment-handson-85b5ccd5f5-ch99x   1/1     Running             0          111s   10.244.3.16   vignesh-vm-cluster-m04   <none>           <none>
pod/deployment-handson-85b5ccd5f5-gtpps   0/1     ContainerCreating   0          2s     <none>        vignesh-vm-cluster       <none>           <none>
pod/deployment-handson-85b5ccd5f5-lz9r8   1/1     Running             0          111s   10.244.2.17   vignesh-vm-cluster-m03   <none>           <none>

NAME                 TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE     SELECTOR
service/kubernetes   ClusterIP   10.96.0.1    <none>        443/TCP   8m39s   <none>

NAME                                 READY   UP-TO-DATE   AVAILABLE   AGE    CONTAINERS               IMAGES         SELECTOR
deployment.apps/deployment-handson   3/4     4            3           112s   deployment-handson-con   nginx:latest   team=int

NAME                                            DESIRED   CURRENT   READY   AGE    CONTAINERS               IMAGES         SELECTOR
replicaset.apps/deployment-handson-85b5ccd5f5   4         4         3       112s   deployment-handson-con   nginx:latest   pod-template-hash=85b5ccd5f5,team=int
```

## Update replicas in CLI
- kubectl scale --replicas=2 deployment/deployment-handson
- kubectl get all -owide
```
dhivyamalathirajasekaran$ kubectl scale --replicas=2 deployment/deployment-handson
deployment.apps/deployment-handson scaled

dhivyamalathirajasekaran$ kubectl get all -owide
NAME                                      READY   STATUS    RESTARTS   AGE     IP            NODE                     NOMINATED NODE   READINESS GATES
pod/deployment-handson-85b5ccd5f5-ch99x   1/1     Running   0          3m25s   10.244.3.16   vignesh-vm-cluster-m04   <none>           <none>
pod/deployment-handson-85b5ccd5f5-lz9r8   1/1     Running   0          3m25s   10.244.2.17   vignesh-vm-cluster-m03   <none>           <none>

NAME                 TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE   SELECTOR
service/kubernetes   ClusterIP   10.96.0.1    <none>        443/TCP   10m   <none>

NAME                                 READY   UP-TO-DATE   AVAILABLE   AGE     CONTAINERS               IMAGES         SELECTOR
deployment.apps/deployment-handson   2/2     2            2           3m26s   deployment-handson-con   nginx:latest   team=int

NAME                                            DESIRED   CURRENT   READY   AGE     CONTAINERS               IMAGES         SELECTOR
replicaset.apps/deployment-handson-85b5ccd5f5   2         2         2       3m26s   deployment-handson-con   nginx:latest   pod-template-hash=85b5ccd5f5,team=int
```

## Apply deployment YAML again
```
dhivyamalathirajasekaran$ kubectl apply -f 03-deployment-handson/deployment-handson.yaml 
deployment.apps/deployment-handson configured

dhivyamalathirajasekaran$ kubectl get all -owide
NAME                                      READY   STATUS              RESTARTS   AGE     IP            NODE                     NOMINATED NODE   READINESS GATES
pod/deployment-handson-85b5ccd5f5-47lvq   0/1     ContainerCreating   0          2s      <none>        vignesh-vm-cluster-m05   <none>           <none>
pod/deployment-handson-85b5ccd5f5-ch99x   1/1     Running             0          3m38s   10.244.3.16   vignesh-vm-cluster-m04   <none>           <none>
pod/deployment-handson-85b5ccd5f5-dzskm   0/1     ContainerCreating   0          2s      <none>        vignesh-vm-cluster       <none>           <none>
pod/deployment-handson-85b5ccd5f5-lz9r8   1/1     Running             0          3m38s   10.244.2.17   vignesh-vm-cluster-m03   <none>           <none>

NAME                 TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE   SELECTOR
service/kubernetes   ClusterIP   10.96.0.1    <none>        443/TCP   10m   <none>

NAME                                 READY   UP-TO-DATE   AVAILABLE   AGE     CONTAINERS               IMAGES         SELECTOR
deployment.apps/deployment-handson   2/4     4            2           3m39s   deployment-handson-con   nginx:latest   team=int

NAME                                            DESIRED   CURRENT   READY   AGE     CONTAINERS               IMAGES         SELECTOR
replicaset.apps/deployment-handson-85b5ccd5f5   4         4         2       3m39s   deployment-handson-con   nginx:latest   pod-template-hash=85b5ccd5f5,team=int
```

## Check history of replica sets
- kubectl get rs
```
dhivyamalathirajasekaran$ kubectl get rs
NAME                            DESIRED   CURRENT   READY   AGE
deployment-handson-85b5ccd5f5   4         4         4       140m
```

## Change the image version to 1.21.3
- kubectl get rs
```
dhivyamalathirajasekaran$ cat 03-deployment-handson/deployment-handson.yaml 
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name:  deployment-handson
  namespace: default
  labels:
    team: int
spec:
  replicas: 4
  selector:
    matchLabels:
      team: int
  template:
    metadata:
      name: deployment-handson-pod
      labels:
        team: int
    spec:
      containers:
      - name:  deployment-handson-con
        image:  nginx:1.21.3
        ports:
        - containerPort: 80

dhivyamalathirajasekaran$ kubectl get rs
NAME                            DESIRED   CURRENT   READY   AGE
deployment-handson-645fdb6957   4         4         4       5m52s
deployment-handson-85b5ccd5f5   0         0         0       156m
```

## Change the image version to 1.20 via CLI
- kubectl set image deployment/deployment-handson deployment-handson-con=nginx:1.20
```
dhivyamalathirajasekaran$ kubectl set image deployment/deployment-handson deployment-handson-con=nginx:1.20
deployment.apps/deployment-handson image updated

dhivyamalathirajasekaran$ kubectl get rs
NAME                            DESIRED   CURRENT   READY   AGE
deployment-handson-5d4d56577c   2         2         0       5s
deployment-handson-5d5c489556   3         3         3       11m
deployment-handson-645fdb6957   0         0         0       22m
deployment-handson-85b5ccd5f5   0         0         0       173m
```

## History of deployments
- kubectl rollout history deployments
```
dhivyamalathirajasekaran$ kubectl rollout history deployments
deployment.apps/deployment-handson 
REVISION  CHANGE-CAUSE
1         <none>
2         <none>
3         <none>
4         <none>
```

## Change the image version to 1.20 via CLI with repord
- kubectl set image deployment/vignesh-deployment vignesh-con=nginx:1.19 --record
- kubectl rollout history deployments
```
dhivyamalathirajasekaran$ kubectl set image deployment/deployment-handson deployment-handson-con=nginx:1.18 --record
deployment.apps/deployment-handson image updated

dhivyamalathirajasekaran$ kubectl rollout history deployments
deployment.apps/deployment-handson 
REVISION  CHANGE-CAUSE
1         <none>
2         <none>
3         <none>
4         <none>
5         <none>
6         kubectl set image deployment/deployment-handson deployment-handson-con=nginx:1.18 --record=true

dhivyamalathirajasekaran$ kubectl get all -o wide
NAME                                      READY   STATUS    RESTARTS   AGE     IP            NODE                     NOMINATED NODE   READINESS GATES
pod/deployment-handson-7d6d5d5d88-lfs86   1/1     Running   0          6m2s    10.244.0.14   vignesh-vm-cluster       <none>           <none>
pod/deployment-handson-7d6d5d5d88-tmxfj   1/1     Running   0          6m14s   10.244.3.21   vignesh-vm-cluster-m04   <none>           <none>
pod/deployment-handson-7d6d5d5d88-tztl9   1/1     Running   0          7m13s   10.244.4.15   vignesh-vm-cluster-m05   <none>           <none>
pod/deployment-handson-7d6d5d5d88-v6fn7   1/1     Running   0          7m14s   10.244.2.22   vignesh-vm-cluster-m03   <none>           <none>

NAME                 TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE     SELECTOR
service/kubernetes   ClusterIP   10.96.0.1    <none>        443/TCP   3h11m   <none>

NAME                                 READY   UP-TO-DATE   AVAILABLE   AGE    CONTAINERS               IMAGES       SELECTOR
deployment.apps/deployment-handson   4/4     4            4           3h4m   deployment-handson-con   nginx:1.18   team=int

NAME                                            DESIRED   CURRENT   READY   AGE     CONTAINERS               IMAGES         SELECTOR
replicaset.apps/deployment-handson-5d4d56577c   0         0         0       11m     deployment-handson-con   nginx:1.20     pod-template-hash=5d4d56577c,team=int
replicaset.apps/deployment-handson-5d54b9f9c    0         0         0       7m39s   deployment-handson-con   nginx:1.19     pod-template-hash=5d54b9f9c,team=int
replicaset.apps/deployment-handson-5d5c489556   0         0         0       22m     deployment-handson-con   nginx:1.21     pod-template-hash=5d5c489556,team=int
replicaset.apps/deployment-handson-645fdb6957   0         0         0       33m     deployment-handson-con   nginx:1.21.3   pod-template-hash=645fdb6957,team=int
replicaset.apps/deployment-handson-7d6d5d5d88   4         4         4       7m14s   deployment-handson-con   nginx:1.18     pod-template-hash=7d6d5d5d88,team=int
replicaset.apps/deployment-handson-85b5ccd5f5   0         0         0       3h4m    deployment-handson-con   nginx:latest   pod-template-hash=85b5ccd5f5,team=int
```

## Add Anotation in YAML and Apply
- kubectl apply -f 03-deployment-handson/deployment-handson.yaml
- kubectl rollout history deployments
```
dhivyamalathirajasekaran$ kubectl apply -f 03-deployment-handson/deployment-handson.yaml 
deployment.apps/deployment-handson configured

dhivyamalathirajasekaran$ cat 03-deployment-handson/deployment-handson.yaml 
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name:  deployment-handson
  namespace: default
  labels:
    team: int
  annotations:
    kubernetes.io/change-cause: "Updating Nginx Version to 1.21"
spec:
  replicas: 4
  selector:
    matchLabels:
      team: int
  template:
    metadata:
      name: deployment-handson-pod
      labels:
        team: int
    spec:
      containers:
      - name:  deployment-handson-con
        image:  nginx:latest
        ports:
        - containerPort: 80

dhivyamalathirajasekaran$ kubectl rollout history deployments
deployment.apps/deployment-handson 
REVISION  CHANGE-CAUSE
2         <none>
3         <none>
4         <none>
5         <none>
6         kubectl set image deployment/deployment-handson deployment-handson-con=nginx:1.18 --record=true
7         Updating Nginx Version to 1.21

dhivyamalathirajasekaran$ kubectl get all -o wide
NAME                                      READY   STATUS    RESTARTS   AGE     IP            NODE                     NOMINATED NODE   READINESS GATES
pod/deployment-handson-85b5ccd5f5-f4m6t   1/1     Running   0          2m28s   10.244.4.16   vignesh-vm-cluster-m05   <none>           <none>
pod/deployment-handson-85b5ccd5f5-gdx7z   1/1     Running   0          2m34s   10.244.2.23   vignesh-vm-cluster-m03   <none>           <none>
pod/deployment-handson-85b5ccd5f5-s8jsm   1/1     Running   0          2m27s   10.244.0.15   vignesh-vm-cluster       <none>           <none>
pod/deployment-handson-85b5ccd5f5-zwl4j   1/1     Running   0          2m33s   10.244.3.22   vignesh-vm-cluster-m04   <none>           <none>

NAME                 TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE     SELECTOR
service/kubernetes   ClusterIP   10.96.0.1    <none>        443/TCP   3h16m   <none>

NAME                                 READY   UP-TO-DATE   AVAILABLE   AGE    CONTAINERS               IMAGES         SELECTOR
deployment.apps/deployment-handson   4/4     4            4           3h9m   deployment-handson-con   nginx:latest   team=int

NAME                                            DESIRED   CURRENT   READY   AGE    CONTAINERS               IMAGES         SELECTOR
replicaset.apps/deployment-handson-5d4d56577c   0         0         0       16m    deployment-handson-con   nginx:1.20     pod-template-hash=5d4d56577c,team=int
replicaset.apps/deployment-handson-5d54b9f9c    0         0         0       12m    deployment-handson-con   nginx:1.19     pod-template-hash=5d54b9f9c,team=int
replicaset.apps/deployment-handson-5d5c489556   0         0         0       27m    deployment-handson-con   nginx:1.21     pod-template-hash=5d5c489556,team=int
replicaset.apps/deployment-handson-645fdb6957   0         0         0       38m    deployment-handson-con   nginx:1.21.3   pod-template-hash=645fdb6957,team=int
replicaset.apps/deployment-handson-7d6d5d5d88   0         0         0       12m    deployment-handson-con   nginx:1.18     pod-template-hash=7d6d5d5d88,team=int
replicaset.apps/deployment-handson-85b5ccd5f5   4         4         4       3h9m   deployment-handson-con   nginx:latest   pod-template-hash=85b5ccd5f5,team=int
(base) Dhivyamalathis-MacBook-Pro:Kubernetes 
```

## Undo the rollout and check
- kubectl rollout undo deployment --to-revision=6
- kubectl get all -o wide
```
dhivyamalathirajasekaran$ kubectl rollout undo deployment --to-revision=6
deployment.apps/deployment-handson rolled back

dhivyamalathirajasekaran$ kubectl get all -o wide
NAME                                      READY   STATUS    RESTARTS   AGE   IP            NODE                     NOMINATED NODE   READINESS GATES
pod/deployment-handson-7d6d5d5d88-6j7mr   1/1     Running   0          7s    10.244.0.16   vignesh-vm-cluster       <none>           <none>
pod/deployment-handson-7d6d5d5d88-n7bnv   1/1     Running   0          8s    10.244.3.23   vignesh-vm-cluster-m04   <none>           <none>
pod/deployment-handson-7d6d5d5d88-p6wtw   1/1     Running   0          13s   10.244.2.24   vignesh-vm-cluster-m03   <none>           <none>
pod/deployment-handson-7d6d5d5d88-vf4f6   1/1     Running   0          13s   10.244.4.17   vignesh-vm-cluster-m05   <none>           <none>

NAME                 TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE     SELECTOR
service/kubernetes   ClusterIP   10.96.0.1    <none>        443/TCP   3h18m   <none>

NAME                                 READY   UP-TO-DATE   AVAILABLE   AGE     CONTAINERS               IMAGES       SELECTOR
deployment.apps/deployment-handson   4/4     4            4           3h11m   deployment-handson-con   nginx:1.18   team=int

NAME                                            DESIRED   CURRENT   READY   AGE     CONTAINERS               IMAGES         SELECTOR
replicaset.apps/deployment-handson-5d4d56577c   0         0         0       18m     deployment-handson-con   nginx:1.20     pod-template-hash=5d4d56577c,team=int
replicaset.apps/deployment-handson-5d54b9f9c    0         0         0       14m     deployment-handson-con   nginx:1.19     pod-template-hash=5d54b9f9c,team=int
replicaset.apps/deployment-handson-5d5c489556   0         0         0       29m     deployment-handson-con   nginx:1.21     pod-template-hash=5d5c489556,team=int
replicaset.apps/deployment-handson-645fdb6957   0         0         0       40m     deployment-handson-con   nginx:1.21.3   pod-template-hash=645fdb6957,team=int
replicaset.apps/deployment-handson-7d6d5d5d88   4         4         4       14m     deployment-handson-con   nginx:1.18     pod-template-hash=7d6d5d5d88,team=int
replicaset.apps/deployment-handson-85b5ccd5f5   0         0         0       3h11m   deployment-handson-con   nginx:latest   pod-template-hash=85b5ccd5f5,team=int
```

## Rollout status
- kubectl rollout status deployment/deployment-handson
```
Waiting for deployment "deployment-handson" rollout to finish: 2 out of 4 new replicas have been updated...
Waiting for deployment "deployment-handson" rollout to finish: 2 out of 4 new replicas have been updated...
Waiting for deployment "deployment-handson" rollout to finish: 2 out of 4 new replicas have been updated...
Waiting for deployment "deployment-handson" rollout to finish: 2 out of 4 new replicas have been updated...
Waiting for deployment "deployment-handson" rollout to finish: 3 out of 4 new replicas have been updated...
Waiting for deployment "deployment-handson" rollout to finish: 1 old replicas are pending termination...
deployment "deployment-handson" successfully rolled out
```
- [Pods Commands - Hands-On](#pods-commands---hands-on)
  * [Create Pods via CLI](#create-pods-via-cli)
  * [Check the pods](#check-the-pods)
  * [Create Pods via YAML with labels](#create-pods-via-yaml-with-labels)
  * [Create one more pod](#create-one-more-pod)
  * [Delete a pods and check if it is re-creating](#delete-a-pods-and-check-if-it-is-re-creating)
  * [List pods using tags](#list-pods-using-tags)
  * [Connect to container/minikube in the pod and hit nginx server](#connect-to-container-minikube-in-the-pod-and-hit-nginx-server)
  * [Enable port-forwording and hit localhost:8080 in browser](#enable-port-forwording-and-hit-localhost-8080-in-browser)
  * [Check the logs of a pod](#check-the-logs-of-a-pod)
  * [Delete all the pods](#delete-all-the-pods)

<small><i><a href='http://ecotrust-canada.github.io/markdown-toc/'>Table of contents generated with markdown-toc</a></i></small>


# Pods Commands - Hands-On
```
1) Create Pods via CLI
kubectl config get-contexts
kubectl get nodes
kubectl run nginx-pod --image=nginx

2) Check/List the pods
kubectl get pods -l team=int -o wide
watch "kubectl get pods -o wide"

3) Create Pods via YAML with labels
kubectl api-resources | grep -i pod
kubectl apply -f nginx-pod.yaml
watch "kubectl get pods -owide"

4) Create one more pod
5) Delete a pods and check if it is re-creating
kubectl delete pod nginx-pod-1

6) List pods using tags
kubectl get pods -l team=int

7) Connect to container in the pod and hit nginx server
kubectl exec -it nginx-pod-2 -c nginx-con-2 -- bash
minikube ssh
minikube dashboard

8) Enable port-forwording and hit localhost:8080 in browser
kubectl port-forward nginx-pod-2 8080:80

9) Check the logs of a pod
kubectl logs nginx-pod-2

10) Delete all the pods
kubectl delete all --all
```


-------------
## Create Pods via CLI
- kubectl config get-contexts
- kubectl get nodes
- kubectl run nginx-pod --image=nginx
```
dhivyamalathirajasekaran$ kubectl config get-contexts
CURRENT   NAME            CLUSTER         AUTHINFO        NAMESPACE
*         local-cluster   local-cluster   local-cluster   default

dhivyamalathirajasekaran$ kubectl get nodes
NAME                STATUS   ROLES           AGE     VERSION
local-cluster       Ready    control-plane   6m38s   v1.28.3
local-cluster-m02   Ready    <none>          5m35s   v1.28.3
local-cluster-m03   Ready    <none>          4m23s   v1.28.3
local-cluster-m04   Ready    <none>          2m24s   v1.28.3

dhivyamalathirajasekaran$ kubectl run nginx-pod --image=nginx
pod/nginx-pod created
```

## Check the pods
- watch "kubectl get pods -o wide"
```
dhivyamalathirajasekaran$ watch "kubectl get pods -o wide"
NAME        READY   STATUS    RESTARTS   AGE   IP           NODE                NOMINATED NODE   READINESS GATES
nginx-pod   1/1     Running   0          84s   10.244.1.2   local-cluster-m02   <none>           <none>
```

## Create Pods via YAML with labels
- kubectl api-resources | grep -i pod
- kubectl apply -f nginx-pod.yaml
- watch "kubectl get pods -owide"
```
dhivyamalathirajasekaran$ kubectl api-resources | grep -i pod
pods                              po           v1                                     true         Pod
podtemplates                                   v1                                     true         PodTemplate
horizontalpodautoscalers          hpa          autoscaling/v2                         true         HorizontalPodAutoscaler
poddisruptionbudgets              pdb          policy/v1                              true         PodDisruptionBudget

dhivyamalathirajasekaran$ cat nginx-pod.yaml 
---
apiVersion: v1
kind: Pod
metadata:
  name: nginx-pod-1
  labels:
    team: int
    type: app
spec:
  containers:
  - name: nginx-con-1
    image: nginx:latest
    ports:
    - containerPort: 80

dhivyamalathirajasekaran$ kubectl apply -f nginx-pod.yaml 
pod/nginx-pod-1 created

dhivyamalathirajasekaran$ watch "kubectl get pods -owide"
NAME          READY   STATUS    RESTARTS   AGE   IP           NODE                NOMINATED NODE   READINESS GATES
nginx-pod     1/1     Running   0          14m   10.244.1.2   local-cluster-m02   <none>           <none>
nginx-pod-1   1/1     Running   0          28s   10.244.4.2   local-cluster-m05   <none>           <none>
```

## Create one more pod
```
dhivyamalathirajasekaran$ cat nginx-pod.yaml 
---
apiVersion: v1
kind: Pod
metadata:
  name: nginx-pod-2
  labels:
    team: int
    type: app
spec:
  containers:
  - name: nginx-con-2
    image: nginx:latest
    ports:
    - containerPort: 80

dhivyamalathirajasekaran$ kubectl apply -f nginx-pod.yaml 
pod/nginx-pod-2 created

dhivyamalathirajasekaran$ kubectl get pods -owide
NAME          READY   STATUS              RESTARTS   AGE    IP           NODE                NOMINATED NODE   READINESS GATES
nginx-pod     1/1     Running             0          16m    10.244.1.2   local-cluster-m02   <none>           <none>
nginx-pod-1   1/1     Running             0          2m8s   10.244.4.2   local-cluster-m05   <none>           <none>
nginx-pod-2   0/1     ContainerCreating   0          6s     <none>       local-cluster-m03   <none>           <none>
```

## Delete a pods and check if it is re-creating
- kubectl delete pod nginx-pod-1
```
dhivyamalathirajasekaran$ kubectl delete pod nginx-pod-1
pod "nginx-pod-1" deleted

dhivyamalathirajasekaran$ kubectl get pods -owide
NAME          READY   STATUS    RESTARTS   AGE    IP           NODE                NOMINATED NODE   READINESS GATES
nginx-pod     1/1     Running   0          24s    10.244.1.3   local-cluster-m02   <none>           <none>
nginx-pod-2   1/1     Running   0          2m3s   10.244.2.2   local-cluster-m03   <none>           <none>
```

## List pods using tags
- kubectl get pods -l team=int
```
dhivyamalathirajasekaran$ kubectl get pods -l team=int
NAME          READY   STATUS    RESTARTS   AGE
nginx-pod-2   1/1     Running   0          2m16s
```

## Connect to container/minikube in the pod and hit nginx server
- kubectl exec -it nginx-pod-2 -c nginx-con-2 -- bash
- minikube ssh
- minikube dashboard
```
dhivyamalathirajasekaran$ kubectl exec -it nginx-pod-2 -c nginx-con-2 -- bash
curl http://nginx-pod-2:80

dhivyamalathirajasekaran$ minikube ssh
curl 10.244.2.2:80
```

## Enable port-forwording and hit localhost:8080 in browser
- kubectl port-forward nginx-pod-2 8080:80
```
dhivyamalathirajasekaran$ kubectl port-forward nginx-pod-2 8080:80
Forwarding from 127.0.0.1:8080 -> 80
Forwarding from [::1]:8080 -> 80
Handling connection for 8080
^C
```

## Check the logs of a pod
- kubectl logs nginx-pod-2
```
dhivyamalathirajasekaran$ kubectl logs nginx-pod-2
```

## Delete all the pods
- kubectl delete all --all
```
dhivyamalathirajasekaran$ kubectl delete all --all
pod "nginx-pod" deleted
pod "nginx-pod-2" deleted
```
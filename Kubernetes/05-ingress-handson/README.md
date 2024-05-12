# Ingress Controller Hands-On
```
1) Makesure the pods are available
deployment.apps/deployment-handson
deployment.apps/sample-python-app 

service/sample-python-app-service
service/service-handson 

2) Enable Ingress controller in Minikube
minikube addons enable ingress
kubectl get all -A | grep ingress-nginx

3) Create Ingress resource in the cluster
kubectl api-resources | grep ingress
kubectl apply -f 05-ingress-handson/ingress-handson.yaml 
kubectl get ing

4) Add to the hosts file for DNS Resolution
sudo vi /etc/hosts
curl http://ingress-nginx.com/
curl -L http://ingress-nginx.com/demo
```

## Enable Ingress controller in Minikube
- minikube addons enable ingress
- kubectl get svc -A | grep controller
```
dhivyamalathirajasekaran$ minikube addons enable ingress 
💡  ingress is an addon maintained by Kubernetes. For any concerns contact minikube on GitHub.
You can view the list of minikube maintainers at: https://github.com/kubernetes/minikube/blob/master/OWNERS
    ▪ Using image registry.k8s.io/ingress-nginx/kube-webhook-certgen:v20231011-8b53cabe0
    ▪ Using image registry.k8s.io/ingress-nginx/kube-webhook-certgen:v20231011-8b53cabe0
    ▪ Using image registry.k8s.io/ingress-nginx/controller:v1.9.4
🔎  Verifying ingress addon...
🌟  The 'ingress' addon is enabled

dhivyamalathirajasekaran$ kubectl get all -A | grep ingress-nginx
ingress-nginx          pod/ingress-nginx-admission-create-whc28         0/1     Completed   0                 14m
ingress-nginx          pod/ingress-nginx-admission-patch-x9nwh          0/1     Completed   1                 14m
ingress-nginx          pod/ingress-nginx-controller-7c6974c4d8-6r6n8    1/1     Running     0                 14m
ingress-nginx          service/ingress-nginx-controller             NodePort    10.96.32.35      <none>        80:31632/TCP,443:32707/TCP      14m
ingress-nginx          service/ingress-nginx-controller-admission   ClusterIP   10.101.76.151    <none>        443/TCP                         14m
ingress-nginx          deployment.apps/ingress-nginx-controller    1/1     1            1           14m
ingress-nginx          replicaset.apps/ingress-nginx-controller-7c6974c4d8    1         1         1       14m
ingress-nginx   job.batch/ingress-nginx-admission-create   1/1           17s        14m
ingress-nginx   job.batch/ingress-nginx-admission-patch    1/1           19s        14m

dhivyamalathirajasekaran$ kubectl get all -A
NAMESPACE              NAME                                             READY   STATUS      RESTARTS          AGE
default                pod/deployment-handson-7d6d5d5d88-6bcrq          1/1     Running     0                 6d8h
default                pod/deployment-handson-7d6d5d5d88-6j7mr          1/1     Running     2 (6d8h ago)      7d9h
default                pod/deployment-handson-7d6d5d5d88-n2vkp          1/1     Running     0                 6d8h
default                pod/deployment-handson-7d6d5d5d88-wcncb          1/1     Running     0                 6d8h
default                pod/sample-python-app-7ddbdd9945-fmf4z           1/1     Running     0                 6d8h
default                pod/sample-python-app-7ddbdd9945-lcxmr           1/1     Running     0                 6d8h
ingress-nginx          pod/ingress-nginx-admission-create-whc28         0/1     Completed   0                 9m22s
ingress-nginx          pod/ingress-nginx-admission-patch-x9nwh          0/1     Completed   1                 9m22s
ingress-nginx          pod/ingress-nginx-controller-7c6974c4d8-6r6n8    1/1     Running     0                 9m22s
kube-system            pod/coredns-5dd5756b68-cq6k6                     1/1     Running     37 (5d15h ago)    21d
kube-system            pod/etcd-vignesh-vm-cluster                      1/1     Running     10 (6d8h ago)     21d
kube-system            pod/kindnet-6q6rs                                1/1     Running     177 (5d16h ago)   21d
kube-system            pod/kindnet-f489k                                1/1     Running     182               21d
kube-system            pod/kindnet-ftrm6                                1/1     Running     61 (5d16h ago)    21d
kube-system            pod/kindnet-rzjfw                                1/1     Running     181               21d
kube-system            pod/kube-apiserver-vignesh-vm-cluster            1/1     Running     34 (5d15h ago)    21d
kube-system            pod/kube-controller-manager-vignesh-vm-cluster   1/1     Running     59 (5d13h ago)    21d
kube-system            pod/kube-proxy-8f8nb                             1/1     Running     5 (6d8h ago)      21d
kube-system            pod/kube-proxy-db2fm                             1/1     Running     3 (6d8h ago)      21d
kube-system            pod/kube-proxy-pjgsb                             1/1     Running     3 (6d8h ago)      21d
kube-system            pod/kube-proxy-wt4ch                             1/1     Running     3 (6d8h ago)      21d
kube-system            pod/kube-scheduler-vignesh-vm-cluster            1/1     Running     26 (5d16h ago)    21d
kube-system            pod/storage-provisioner                          1/1     Running     88 (11h ago)      21d
kubernetes-dashboard   pod/dashboard-metrics-scraper-7fd5cb4ddc-l6bxw   1/1     Running     0                 6d8h
kubernetes-dashboard   pod/kubernetes-dashboard-8694d4445c-mvt9l        1/1     Running     45 (5d16h ago)    6d8h

NAMESPACE              NAME                                         TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)                         AGE
default                service/kubernetes                           ClusterIP   10.96.0.1        <none>        443/TCP                         7d13h
default                service/sample-python-app-service            NodePort    10.110.191.12    <none>        8888:31000/TCP                  6d8h
default                service/service-handson                      NodePort    10.107.231.120   <none>        8080:32000/TCP,8081:32001/TCP   7d6h
ingress-nginx          service/ingress-nginx-controller             NodePort    10.96.32.35      <none>        80:31632/TCP,443:32707/TCP      9m23s
ingress-nginx          service/ingress-nginx-controller-admission   ClusterIP   10.101.76.151    <none>        443/TCP                         9m23s
kube-system            service/kube-dns                             ClusterIP   10.96.0.10       <none>        53/UDP,53/TCP,9153/TCP          21d
kubernetes-dashboard   service/dashboard-metrics-scraper            ClusterIP   10.109.12.81     <none>        8000/TCP                        7d19h
kubernetes-dashboard   service/kubernetes-dashboard                 ClusterIP   10.100.230.24    <none>        80/TCP                          7d19h

NAMESPACE     NAME                        DESIRED   CURRENT   READY   UP-TO-DATE   AVAILABLE   NODE SELECTOR            AGE
kube-system   daemonset.apps/kindnet      4         4         4       4            4           <none>                   21d
kube-system   daemonset.apps/kube-proxy   4         4         4       4            4           kubernetes.io/os=linux   21d

NAMESPACE              NAME                                        READY   UP-TO-DATE   AVAILABLE   AGE
default                deployment.apps/deployment-handson          4/4     4            4           7d13h
default                deployment.apps/sample-python-app           2/2     2            2           6d8h
ingress-nginx          deployment.apps/ingress-nginx-controller    1/1     1            1           9m22s
kube-system            deployment.apps/coredns                     1/1     1            1           21d
kubernetes-dashboard   deployment.apps/dashboard-metrics-scraper   1/1     1            1           7d19h
kubernetes-dashboard   deployment.apps/kubernetes-dashboard        1/1     1            1           7d19h

NAMESPACE              NAME                                                   DESIRED   CURRENT   READY   AGE
default                replicaset.apps/deployment-handson-5d4d56577c          0         0         0       7d10h
default                replicaset.apps/deployment-handson-5d54b9f9c           0         0         0       7d10h
default                replicaset.apps/deployment-handson-5d5c489556          0         0         0       7d10h
default                replicaset.apps/deployment-handson-645fdb6957          0         0         0       7d10h
default                replicaset.apps/deployment-handson-7d6d5d5d88          4         4         4       7d10h
default                replicaset.apps/deployment-handson-85b5ccd5f5          0         0         0       7d13h
default                replicaset.apps/sample-python-app-7ddbdd9945           2         2         2       6d8h
ingress-nginx          replicaset.apps/ingress-nginx-controller-7c6974c4d8    1         1         1       9m22s
kube-system            replicaset.apps/coredns-5dd5756b68                     1         1         1       21d
kubernetes-dashboard   replicaset.apps/dashboard-metrics-scraper-7fd5cb4ddc   1         1         1       7d19h
kubernetes-dashboard   replicaset.apps/kubernetes-dashboard-8694d4445c        1         1         1       7d19h

NAMESPACE       NAME                                       COMPLETIONS   DURATION   AGE
ingress-nginx   job.batch/ingress-nginx-admission-create   1/1           17s        9m22s
ingress-nginx   job.batch/ingress-nginx-admission-patch    1/1           19s        9m22s
```

## Create Ingress resource in the cluster
- kubectl api-resources | grep ingress
- kubectl apply -f 05-ingress-handson/ingress-handson.yaml 
- kubectl get ing
```
dhivyamalathirajasekaran$ kubectl api-resources | grep ingress
ingressclasses                                 networking.k8s.io/v1                   false        IngressClass
ingresses                         ing          networking.k8s.io/v1                   true         Ingress

dhivyamalathirajasekaran$ cat 05-ingress-handson/ingress-handson.yaml 
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ingress-handson
spec:
  rules:
  - host: ingress-nginx.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: service-handson
            port:
              number: 8080
      - path: /demo
        pathType: Prefix
        backend:
          service:
            name: sample-python-app-service
            port:
              number: 8888

dhivyamalathirajasekaran$ kubectl apply -f 05-ingress-handson/ingress-handson.yaml 
ingress.networking.k8s.io/ingress-handson created

dhivyamalathirajasekaran$ kubectl get ing
NAME              CLASS   HOSTS               ADDRESS        PORTS   AGE
ingress-handson   nginx   ingress-nginx.com   192.168.64.3   80      86s
```

## Add to the hosts file for DNS Resolution
- sudo vi /etc/hosts
- curl http://ingress-nginx.com/
- curl -L http://ingress-nginx.com/demo
```
dhivyamalathirajasekaran$ sudo vi /etc/hosts
192.168.64.3    ingress-nginx.com

dhivyamalathirajasekaran$ curl http://ingress-nginx.com/
SUCCESS

dhivyamalathirajasekaran$ curl -L http://ingress-nginx.com/demo
SUCCESS
```


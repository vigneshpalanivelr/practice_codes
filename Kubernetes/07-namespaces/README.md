# Namespaces - HandsOn
- Default
User default namespace, resources will get deployed if not explicitely mentioned
- kube-node-lease
Lease object in every node sends heartbeat to control plane
- kube-public
Public resources allow access for all users with read-only access
- kube-system
Resources created by kubernetes cluster

```
dhivyamalathirajasekaran$ kubectl get ns -A
NAME                   STATUS   AGE
default                Active   28d
ingress-nginx          Active   6d8h
kube-node-lease        Active   28d
kube-public            Active   28d
kube-system            Active   28d
kubernetes-dashboard   Active   14d
```

```

```
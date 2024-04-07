---


---

<h1 id="kubectl-commands">KubeCTL commands</h1>
<p><strong>Table of Contents</strong></p>
<p>[TOCM]</p>
<p>[TOC]</p>
<h2 id="nodes">nodes</h2>
<pre class=" language-sh"><code class="prism  language-sh">kubectl get nodes
kubectl describe node &lt;node&gt;

--Ex:------------------------------------------------
controlplane $ kubectl get nodes    
NAME           STATUS   ROLES           AGE   VERSION
controlplane   Ready    control-plane   33d   v1.29.0
node01         Ready    &lt;none&gt;          33d   v1.29.0
</code></pre>
<h2 id="namespace">namespace</h2>
<ul>
<li>By default all the resources will be created under <strong>default</strong> namesapce</li>
<li>Always set namespace before doing anything</li>
</ul>
<pre class=" language-sh"><code class="prism  language-sh">kubectl get namespace
kubectl create namespace &lt;ns&gt;
kubectl config set-context --current --namespace=&lt;ns&gt;
kubectl delete namespace &lt;ns&gt;
kubectl describe namespace &lt;ns&gt;

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
</code></pre>
<pre class=" language-yaml"><code class="prism  language-yaml"><span class="token punctuation">---</span>
<span class="token key atrule">apiVersion</span><span class="token punctuation">:</span> v1
<span class="token key atrule">kind</span><span class="token punctuation">:</span> Namespace
<span class="token key atrule">metadata</span><span class="token punctuation">:</span>
  <span class="token key atrule">name</span><span class="token punctuation">:</span> vignesh<span class="token punctuation">-</span>ns
</code></pre>
<pre class=" language-sh"><code class="prism  language-sh">--Ex:------------------------------------------------
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
</code></pre>
<h2 id="pods">pods</h2>
<ul>
<li>There are 12 system pods under <strong>kube-system</strong> namespace</li>
<li>4 Important controlplane pods
<ul>
<li>kube-apiserver</li>
<li>etcd</li>
<li>kube-controller-manager</li>
<li>kube-scheduler</li>
</ul>
</li>
<li>6 other pods
<ul>
<li>kube-proxy (2)</li>
<li>coredns(2)</li>
<li>canal(2)</li>
<li>calico-kube-controllers</li>
<li>local-path-provisioner</li>
</ul>
</li>
</ul>
<pre class=" language-sh"><code class="prism  language-sh">kubectl get pods
kubectl get pods -A
kubectl get pods -A -o wide
kubectl get pods -n vignesh-ns
kubectl get pods --selector &lt;key=value&gt; --namespace=vignesh-ns
kubectl create -f vignesh-pod.yaml
kubectl create -f vignesh-pod.yaml --namespace=vignesh-ns
kubectl describe pod &lt;pod&gt;
kubectl delete pods &lt;pod&gt;


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
kube-system          calico-kube-controllers-9d57d8f49-jvt8w   1/1     Running   3 (8m14s ago)   33d   192.168.0.2   controlplane   &lt;none&gt;           &lt;none&gt;
kube-system          canal-gjxwj                               2/2     Running   2 (8m13s ago)   33d   172.30.2.2    node01         &lt;none&gt;           &lt;none&gt;
kube-system          canal-j6pwg                               2/2     Running   2 (8m14s ago)   33d   172.30.1.2    controlplane   &lt;none&gt;           &lt;none&gt;
kube-system          coredns-86b698fbb6-8q542                  1/1     Running   1 (8m13s ago)   33d   192.168.1.3   node01         &lt;none&gt;           &lt;none&gt;
kube-system          coredns-86b698fbb6-hqpmj                  1/1     Running   1 (8m13s ago)   33d   192.168.1.2   node01         &lt;none&gt;           &lt;none&gt;
kube-system          etcd-controlplane                         1/1     Running   2 (8m14s ago)   33d   172.30.1.2    controlplane   &lt;none&gt;           &lt;none&gt;
kube-system          kube-apiserver-controlplane               1/1     Running   2 (8m14s ago)   33d   172.30.1.2    controlplane   &lt;none&gt;           &lt;none&gt;
kube-system          kube-controller-manager-controlplane      1/1     Running   2 (8m14s ago)   33d   172.30.1.2    controlplane   &lt;none&gt;           &lt;none&gt;
kube-system          kube-proxy-85drq                          1/1     Running   2 (8m14s ago)   33d   172.30.1.2    controlplane   &lt;none&gt;           &lt;none&gt;
kube-system          kube-proxy-lhxdd                          1/1     Running   1 (8m13s ago)   33d   172.30.2.2    node01         &lt;none&gt;           &lt;none&gt;
kube-system          kube-scheduler-controlplane               1/1     Running   2 (8m14s ago)   33d   172.30.1.2    controlplane   &lt;none&gt;           &lt;none&gt;
local-path-storage   local-path-provisioner-5d854bc5c4-h55kw   1/1     Running   2 (8m14s ago)   33d   192.168.0.3   controlplane   &lt;none&gt;           &lt;none&gt;

--Ex:---------------------------------------------------------------------------------------------------------------------------------------------------------------
controlplane $ vi vignesh-pod.yaml
</code></pre>
<pre class=" language-yaml"><code class="prism  language-yaml"><span class="token punctuation">---</span>
<span class="token key atrule">apiVersion</span><span class="token punctuation">:</span> v1
<span class="token key atrule">kind</span><span class="token punctuation">:</span> Pod
<span class="token key atrule">metadata</span><span class="token punctuation">:</span>
  <span class="token key atrule">name</span><span class="token punctuation">:</span> vignesh<span class="token punctuation">-</span>pod<span class="token punctuation">-</span><span class="token number">1</span>
  <span class="token key atrule">labels</span><span class="token punctuation">:</span>
    <span class="token key atrule">app</span><span class="token punctuation">:</span> bank<span class="token punctuation">-</span>app
    <span class="token key atrule">type</span><span class="token punctuation">:</span> front<span class="token punctuation">-</span>end
<span class="token key atrule">spec</span><span class="token punctuation">:</span>
  <span class="token key atrule">containers</span><span class="token punctuation">:</span>
  <span class="token punctuation">-</span> <span class="token key atrule">name</span><span class="token punctuation">:</span> vignesh<span class="token punctuation">-</span>pod<span class="token punctuation">-</span><span class="token number">1</span>
    <span class="token key atrule">image</span><span class="token punctuation">:</span> nginx<span class="token punctuation">:</span>1.14.2
    <span class="token key atrule">ports</span><span class="token punctuation">:</span>
    <span class="token punctuation">-</span> <span class="token key atrule">containerPort</span><span class="token punctuation">:</span> <span class="token number">80</span>
</code></pre>
<pre class=" language-sh"><code class="prism  language-sh">--Ex:---------------------------------------------------------------------------------------------------------------------------------------------------------------
controlplane $ kubectl create -f vignesh-pod.yaml  
pod/vignesh-pod-1 created

--Ex:---------------------------------------------------------------------------------------------------------------------------------------------------------------
controlplane $ kubectl get pods -A | grep vignesh-pod-1
NAMESPACE            NAME                                      READY   STATUS    RESTARTS       AGE
default              vignesh-pod-1                             0/1     ContainerCreating   0             5s

--Ex:---------------------------------------------------------------------------------------------------------------------------------------------------------------
controlplane $ kubectl create -f vignesh-pod.yaml 
pod/vignesh-pod-1 created
</code></pre>
<pre class=" language-yaml"><code class="prism  language-yaml"><span class="token punctuation">---</span>
<span class="token key atrule">apiVersion</span><span class="token punctuation">:</span> v1
<span class="token key atrule">kind</span><span class="token punctuation">:</span> Pod
<span class="token key atrule">metadata</span><span class="token punctuation">:</span>
  <span class="token key atrule">name</span><span class="token punctuation">:</span> vignesh<span class="token punctuation">-</span>pod<span class="token punctuation">-</span><span class="token number">2</span>
  <span class="token key atrule">namespace</span><span class="token punctuation">:</span> vignesh<span class="token punctuation">-</span>ns
  <span class="token key atrule">labels</span><span class="token punctuation">:</span>
    <span class="token key atrule">app</span><span class="token punctuation">:</span> bank<span class="token punctuation">-</span>db
    <span class="token key atrule">type</span><span class="token punctuation">:</span> back<span class="token punctuation">-</span>end
<span class="token key atrule">spec</span><span class="token punctuation">:</span>
  <span class="token key atrule">containers</span><span class="token punctuation">:</span>
  <span class="token punctuation">-</span> <span class="token key atrule">name</span><span class="token punctuation">:</span> vignesh<span class="token punctuation">-</span>pod<span class="token punctuation">-</span><span class="token number">2</span>
    <span class="token key atrule">image</span><span class="token punctuation">:</span> nginx<span class="token punctuation">:</span>1.14.2
    <span class="token key atrule">ports</span><span class="token punctuation">:</span>
    <span class="token punctuation">-</span> <span class="token key atrule">containerPort</span><span class="token punctuation">:</span> <span class="token number">80</span>
</code></pre>
<pre class=" language-sh"><code class="prism  language-sh">--Ex:---------------------------------------------------------------------------------------------------------------------------------------------------------------
controlplane $ kubectl create -f vignesh-pod.yaml 
pod/vignesh-pod-1 created

--Ex:---------------------------------------------------------------------------------------------------------------------------------------------------------------
controlplane $ kubectl get pods -A | grep vignesh-pod
NAMESPACE            NAME                                      READY   STATUS    RESTARTS      AGE    IP            NODE           NOMINATED NODE   READINESS GATES
default              vignesh-pod-1                             1/1     Running   0             118s   192.168.1.4   node01         &lt;none&gt;           &lt;none&gt;
vignesh-ns           vignesh-pod-2                             1/1     Running   0             7s     192.168.1.5   node01         &lt;none&gt;           &lt;none&gt;

--Ex:---------------------------------------------------------------------------------------------------------------------------------------------------------------
controlplane $ kubectl get pods --selector app=bank-db --namespace=vignesh-ns
NAME            READY   STATUS    RESTARTS   AGE
vignesh-pod-2   1/1     Running   0          4m45s
</code></pre>
<h2 id="service">service</h2>


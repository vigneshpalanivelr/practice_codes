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
---
apiVersion: v1
kind: Namespace
metadata:
  name: vignesh-ns

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
controlplane $ vi vignesh-pod.yaml
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

--Ex:---------------------------------------------------------------------------------------------------------------------------------------------------------------
controlplane $ kubectl create -f vignesh-pod.yaml  
pod/vignesh-pod-1 created

--Ex:---------------------------------------------------------------------------------------------------------------------------------------------------------------
controlplane $ kubectl get pods -A | grep vignesh-pod-1
NAMESPACE            NAME                                      READY   STATUS    RESTARTS       AGE
default              vignesh-pod-1                             0/1     ContainerCreating   0             5s

--Ex:---------------------------------------------------------------------------------------------------------------------------------------------------------------
controlplane $ vi vignesh-pod.yaml
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

--Ex:---------------------------------------------------------------------------------------------------------------------------------------------------------------
controlplane $ kubectl create -f vignesh-pod.yaml 
pod/vignesh-pod-1 created

--Ex:---------------------------------------------------------------------------------------------------------------------------------------------------------------
NAMESPACE            NAME                                      READY   STATUS    RESTARTS      AGE    IP            NODE           NOMINATED NODE   READINESS GATES
default              vignesh-pod-1                             1/1     Running   0             118s   192.168.1.4   node01         <none>           <none>
vignesh-ns           vignesh-pod-2                             1/1     Running   0             7s     192.168.1.5   node01         <none>           <none>

--Ex:---------------------------------------------------------------------------------------------------------------------------------------------------------------
controlplane $ kubectl get pods --selector app=bank-db --namespace=vignesh-ns
NAME            READY   STATUS    RESTARTS   AGE
vignesh-pod-2   1/1     Running   0          4m45s
```
# Welcome to StackEdit!

Hi! I'm your first Markdown file in **StackEdit**. If you want to learn about StackEdit, you can read me. If you want to play with Markdown, you can edit me. Once you have finished with me, you can create new files by opening the **file explorer** on the left corner of the navigation bar.


# Files

StackEdit stores your files in your browser, which means all your files are automatically saved locally and are accessible **offline!**

## Create files and folders

The file explorer is accessible using the button in left corner of the navigation bar. You can create a new file by clicking the **New file** button in the file explorer. You can also create folders by clicking the **New folder** button.

## Switch to another file

All your files and folders are presented as a tree in the file explorer. You can switch from one to another by clicking a file in the tree.

## Rename a file

You can rename the current file by clicking the file name in the navigation bar or by clicking the **Rename** button in the file explorer.

## Delete a file

You can delete the current file by clicking the **Remove** button in the file explorer. The file will be moved into the **Trash** folder and automatically deleted after 7 days of inactivity.

## Export a file

You can export the current file by clicking **Export to disk** in the menu. You can choose to export the file as plain Markdown, as HTML using a Handlebars template or as a PDF.


# Synchronization

Synchronization is one of the biggest features of StackEdit. It enables you to synchronize any file in your workspace with other files stored in your **Google Drive**, your **Dropbox** and your **GitHub** accounts. This allows you to keep writing on other devices, collaborate with people you share the file with, integrate easily into your workflow... The synchronization mechanism takes place every minute in the background, downloading, merging, and uploading file modifications.

There are two types of synchronization and they can complement each other:

- The workspace synchronization will sync all your files, folders and settings automatically. This will allow you to fetch your workspace on any other device.
	> To start syncing your workspace, just sign in with Google in the menu.

- The file synchronization will keep one file of the workspace synced with one or multiple files in **Google Drive**, **Dropbox** or **GitHub**.
	> Before starting to sync files, you must link an account in the **Synchronize** sub-menu.

## Open a file

You can open a file from **Google Drive**, **Dropbox** or **GitHub** by opening the **Synchronize** sub-menu and clicking **Open from**. Once opened in the workspace, any modification in the file will be automatically synced.

## Save a file

You can save any file of the workspace to **Google Drive**, **Dropbox** or **GitHub** by opening the **Synchronize** sub-menu and clicking **Save on**. Even if a file in the workspace is already synced, you can save it to another location. StackEdit can sync one file with multiple locations and accounts.

## Synchronize a file

Once your file is linked to a synchronized location, StackEdit will periodically synchronize it by downloading/uploading any modification. A merge will be performed if necessary and conflicts will be resolved.

If you just have modified your file and you want to force syncing, click the **Synchronize now** button in the navigation bar.

> **Note:** The **Synchronize now** button is disabled if you have no file to synchronize.

## Manage file synchronization

Since one file can be synced with multiple locations, you can list and manage synchronized locations by clicking **File synchronization** in the **Synchronize** sub-menu. This allows you to list and remove synchronized locations that are linked to your file.


# Publication

Publishing in StackEdit makes it simple for you to publish online your files. Once you're happy with a file, you can publish it to different hosting platforms like **Blogger**, **Dropbox**, **Gist**, **GitHub**, **Google Drive**, **WordPress** and **Zendesk**. With [Handlebars templates](http://handlebarsjs.com/), you have full control over what you export.

> Before starting to publish, you must link an account in the **Publish** sub-menu.

## Publish a File

You can publish your file by opening the **Publish** sub-menu and by clicking **Publish to**. For some locations, you can choose between the following formats:

- Markdown: publish the Markdown text on a website that can interpret it (**GitHub** for instance),
- HTML: publish the file converted to HTML via a Handlebars template (on a blog for example).

## Update a publication

After publishing, StackEdit keeps your file linked to that publication which makes it easy for you to re-publish it. Once you have modified your file and you want to update your publication, click on the **Publish now** button in the navigation bar.

> **Note:** The **Publish now** button is disabled if your file has not been published yet.

## Manage file publication

Since one file can be published to multiple locations, you can list and manage publish locations by clicking **File publication** in the **Publish** sub-menu. This allows you to list and remove publication locations that are linked to your file.


# Markdown extensions

StackEdit extends the standard Markdown syntax by adding extra **Markdown extensions**, providing you with some nice features.

> **ProTip:** You can disable any **Markdown extension** in the **File properties** dialog.


## SmartyPants

SmartyPants converts ASCII punctuation characters into "smart" typographic punctuation HTML entities. For example:

|                |ASCII                          |HTML                         |
|----------------|-------------------------------|-----------------------------|
|Single backticks|`'Isn't this fun?'`            |'Isn't this fun?'            |
|Quotes          |`"Isn't this fun?"`            |"Isn't this fun?"            |
|Dashes          |`-- is en-dash, --- is em-dash`|-- is en-dash, --- is em-dash|


## KaTeX

You can render LaTeX mathematical expressions using [KaTeX](https://khan.github.io/KaTeX/):

The *Gamma function* satisfying $\Gamma(n) = (n-1)!\quad\forall n\in\mathbb N$ is via the Euler integral

$$
\Gamma(z) = \int_0^\infty t^{z-1}e^{-t}dt\,.
$$

> You can find more information about **LaTeX** mathematical expressions [here](http://meta.math.stackexchange.com/questions/5020/mathjax-basic-tutorial-and-quick-reference).


## UML diagrams

You can render UML diagrams using [Mermaid](https://mermaidjs.github.io/). For example, this will produce a sequence diagram:

```mermaid
sequenceDiagram
Alice ->> Bob: Hello Bob, how are you?
Bob-->>John: How about you John?
Bob--x Alice: I am good thanks!
Bob-x John: I am good thanks!
Note right of John: Bob thinks a long<br/>long time, so long<br/>that the text does<br/>not fit on a row.

Bob-->Alice: Checking with John...
Alice->John: Yes... John, how are you?
```

And this will produce a flow chart:

```mermaid
graph LR
A[Square Rect] -- Link text --> B((Circle))
A --> C(Round Rect)
B --> D{Rhombus}
C --> D
```
<!--stackedit_data:
eyJoaXN0b3J5IjpbMTI2MTgxOTAsLTE4MjU1MDUyNjUsLTE3MD
E2NDg5OV19
-->
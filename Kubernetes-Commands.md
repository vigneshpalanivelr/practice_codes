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
<pre class=" language-sh"><code class="prism  language-sh">---
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
controlplane $ vi vignesh-pod.yaml
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
<pre class=" language-sh"><code class="prism  language-sh">---
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
default              vignesh-pod-1                             1/1     Running   0             118s   192.168.1.4   node01         &lt;none&gt;           &lt;none&gt;
vignesh-ns           vignesh-pod-2                             1/1     Running   0             7s     192.168.1.5   node01         &lt;none&gt;           &lt;none&gt;

--Ex:---------------------------------------------------------------------------------------------------------------------------------------------------------------
controlplane $ kubectl get pods --selector app=bank-db --namespace=vignesh-ns
NAME            READY   STATUS    RESTARTS   AGE
vignesh-pod-2   1/1     Running   0          4m45s
</code></pre>
<h1 id="welcome-to-stackedit">Welcome to StackEdit!</h1>
<p>Hi! I’m your first Markdown file in <strong>StackEdit</strong>. If you want to learn about StackEdit, you can read me. If you want to play with Markdown, you can edit me. Once you have finished with me, you can create new files by opening the <strong>file explorer</strong> on the left corner of the navigation bar.</p>
<h1 id="files">Files</h1>
<p>StackEdit stores your files in your browser, which means all your files are automatically saved locally and are accessible <strong>offline!</strong></p>
<h2 id="create-files-and-folders">Create files and folders</h2>
<p>The file explorer is accessible using the button in left corner of the navigation bar. You can create a new file by clicking the <strong>New file</strong> button in the file explorer. You can also create folders by clicking the <strong>New folder</strong> button.</p>
<h2 id="switch-to-another-file">Switch to another file</h2>
<p>All your files and folders are presented as a tree in the file explorer. You can switch from one to another by clicking a file in the tree.</p>
<h2 id="rename-a-file">Rename a file</h2>
<p>You can rename the current file by clicking the file name in the navigation bar or by clicking the <strong>Rename</strong> button in the file explorer.</p>
<h2 id="delete-a-file">Delete a file</h2>
<p>You can delete the current file by clicking the <strong>Remove</strong> button in the file explorer. The file will be moved into the <strong>Trash</strong> folder and automatically deleted after 7 days of inactivity.</p>
<h2 id="export-a-file">Export a file</h2>
<p>You can export the current file by clicking <strong>Export to disk</strong> in the menu. You can choose to export the file as plain Markdown, as HTML using a Handlebars template or as a PDF.</p>
<h1 id="synchronization">Synchronization</h1>
<p>Synchronization is one of the biggest features of StackEdit. It enables you to synchronize any file in your workspace with other files stored in your <strong>Google Drive</strong>, your <strong>Dropbox</strong> and your <strong>GitHub</strong> accounts. This allows you to keep writing on other devices, collaborate with people you share the file with, integrate easily into your workflow… The synchronization mechanism takes place every minute in the background, downloading, merging, and uploading file modifications.</p>
<p>There are two types of synchronization and they can complement each other:</p>
<ul>
<li>
<p>The workspace synchronization will sync all your files, folders and settings automatically. This will allow you to fetch your workspace on any other device.</p>
<blockquote>
<p>To start syncing your workspace, just sign in with Google in the menu.</p>
</blockquote>
</li>
<li>
<p>The file synchronization will keep one file of the workspace synced with one or multiple files in <strong>Google Drive</strong>, <strong>Dropbox</strong> or <strong>GitHub</strong>.</p>
<blockquote>
<p>Before starting to sync files, you must link an account in the <strong>Synchronize</strong> sub-menu.</p>
</blockquote>
</li>
</ul>
<h2 id="open-a-file">Open a file</h2>
<p>You can open a file from <strong>Google Drive</strong>, <strong>Dropbox</strong> or <strong>GitHub</strong> by opening the <strong>Synchronize</strong> sub-menu and clicking <strong>Open from</strong>. Once opened in the workspace, any modification in the file will be automatically synced.</p>
<h2 id="save-a-file">Save a file</h2>
<p>You can save any file of the workspace to <strong>Google Drive</strong>, <strong>Dropbox</strong> or <strong>GitHub</strong> by opening the <strong>Synchronize</strong> sub-menu and clicking <strong>Save on</strong>. Even if a file in the workspace is already synced, you can save it to another location. StackEdit can sync one file with multiple locations and accounts.</p>
<h2 id="synchronize-a-file">Synchronize a file</h2>
<p>Once your file is linked to a synchronized location, StackEdit will periodically synchronize it by downloading/uploading any modification. A merge will be performed if necessary and conflicts will be resolved.</p>
<p>If you just have modified your file and you want to force syncing, click the <strong>Synchronize now</strong> button in the navigation bar.</p>
<blockquote>
<p><strong>Note:</strong> The <strong>Synchronize now</strong> button is disabled if you have no file to synchronize.</p>
</blockquote>
<h2 id="manage-file-synchronization">Manage file synchronization</h2>
<p>Since one file can be synced with multiple locations, you can list and manage synchronized locations by clicking <strong>File synchronization</strong> in the <strong>Synchronize</strong> sub-menu. This allows you to list and remove synchronized locations that are linked to your file.</p>
<h1 id="publication">Publication</h1>
<p>Publishing in StackEdit makes it simple for you to publish online your files. Once you’re happy with a file, you can publish it to different hosting platforms like <strong>Blogger</strong>, <strong>Dropbox</strong>, <strong>Gist</strong>, <strong>GitHub</strong>, <strong>Google Drive</strong>, <strong>WordPress</strong> and <strong>Zendesk</strong>. With <a href="http://handlebarsjs.com/">Handlebars templates</a>, you have full control over what you export.</p>
<blockquote>
<p>Before starting to publish, you must link an account in the <strong>Publish</strong> sub-menu.</p>
</blockquote>
<h2 id="publish-a-file">Publish a File</h2>
<p>You can publish your file by opening the <strong>Publish</strong> sub-menu and by clicking <strong>Publish to</strong>. For some locations, you can choose between the following formats:</p>
<ul>
<li>Markdown: publish the Markdown text on a website that can interpret it (<strong>GitHub</strong> for instance),</li>
<li>HTML: publish the file converted to HTML via a Handlebars template (on a blog for example).</li>
</ul>
<h2 id="update-a-publication">Update a publication</h2>
<p>After publishing, StackEdit keeps your file linked to that publication which makes it easy for you to re-publish it. Once you have modified your file and you want to update your publication, click on the <strong>Publish now</strong> button in the navigation bar.</p>
<blockquote>
<p><strong>Note:</strong> The <strong>Publish now</strong> button is disabled if your file has not been published yet.</p>
</blockquote>
<h2 id="manage-file-publication">Manage file publication</h2>
<p>Since one file can be published to multiple locations, you can list and manage publish locations by clicking <strong>File publication</strong> in the <strong>Publish</strong> sub-menu. This allows you to list and remove publication locations that are linked to your file.</p>
<h1 id="markdown-extensions">Markdown extensions</h1>
<p>StackEdit extends the standard Markdown syntax by adding extra <strong>Markdown extensions</strong>, providing you with some nice features.</p>
<blockquote>
<p><strong>ProTip:</strong> You can disable any <strong>Markdown extension</strong> in the <strong>File properties</strong> dialog.</p>
</blockquote>
<h2 id="smartypants">SmartyPants</h2>
<p>SmartyPants converts ASCII punctuation characters into “smart” typographic punctuation HTML entities. For example:</p>

<table>
<thead>
<tr>
<th></th>
<th>ASCII</th>
<th>HTML</th>
</tr>
</thead>
<tbody>
<tr>
<td>Single backticks</td>
<td><code>'Isn't this fun?'</code></td>
<td>‘Isn’t this fun?’</td>
</tr>
<tr>
<td>Quotes</td>
<td><code>"Isn't this fun?"</code></td>
<td>“Isn’t this fun?”</td>
</tr>
<tr>
<td>Dashes</td>
<td><code>-- is en-dash, --- is em-dash</code></td>
<td>– is en-dash, — is em-dash</td>
</tr>
</tbody>
</table><h2 id="katex">KaTeX</h2>
<p>You can render LaTeX mathematical expressions using <a href="https://khan.github.io/KaTeX/">KaTeX</a>:</p>
<p>The <em>Gamma function</em> satisfying <span class="katex--inline"><span class="katex"><span class="katex-mathml"><math xmlns="http://www.w3.org/1998/Math/MathML"><semantics><mrow><mi mathvariant="normal">Γ</mi><mo stretchy="false">(</mo><mi>n</mi><mo stretchy="false">)</mo><mo>=</mo><mo stretchy="false">(</mo><mi>n</mi><mo>−</mo><mn>1</mn><mo stretchy="false">)</mo><mo stretchy="false">!</mo><mspace width="1em"></mspace><mi mathvariant="normal">∀</mi><mi>n</mi><mo>∈</mo><mi mathvariant="double-struck">N</mi></mrow><annotation encoding="application/x-tex">\Gamma(n) = (n-1)!\quad\forall n\in\mathbb N</annotation></semantics></math></span><span class="katex-html" aria-hidden="true"><span class="base"><span class="strut" style="height: 1em; vertical-align: -0.25em;"></span><span class="mord">Γ</span><span class="mopen">(</span><span class="mord mathnormal">n</span><span class="mclose">)</span><span class="mspace" style="margin-right: 0.277778em;"></span><span class="mrel">=</span><span class="mspace" style="margin-right: 0.277778em;"></span></span><span class="base"><span class="strut" style="height: 1em; vertical-align: -0.25em;"></span><span class="mopen">(</span><span class="mord mathnormal">n</span><span class="mspace" style="margin-right: 0.222222em;"></span><span class="mbin">−</span><span class="mspace" style="margin-right: 0.222222em;"></span></span><span class="base"><span class="strut" style="height: 1em; vertical-align: -0.25em;"></span><span class="mord">1</span><span class="mclose">)!</span><span class="mspace" style="margin-right: 1em;"></span><span class="mord">∀</span><span class="mord mathnormal">n</span><span class="mspace" style="margin-right: 0.277778em;"></span><span class="mrel">∈</span><span class="mspace" style="margin-right: 0.277778em;"></span></span><span class="base"><span class="strut" style="height: 0.68889em; vertical-align: 0em;"></span><span class="mord mathbb">N</span></span></span></span></span> is via the Euler integral</p>
<p><span class="katex--display"><span class="katex-display"><span class="katex"><span class="katex-mathml"><math xmlns="http://www.w3.org/1998/Math/MathML" display="block"><semantics><mrow><mi mathvariant="normal">Γ</mi><mo stretchy="false">(</mo><mi>z</mi><mo stretchy="false">)</mo><mo>=</mo><msubsup><mo>∫</mo><mn>0</mn><mi mathvariant="normal">∞</mi></msubsup><msup><mi>t</mi><mrow><mi>z</mi><mo>−</mo><mn>1</mn></mrow></msup><msup><mi>e</mi><mrow><mo>−</mo><mi>t</mi></mrow></msup><mi>d</mi><mi>t</mi> <mi mathvariant="normal">.</mi></mrow><annotation encoding="application/x-tex">
\Gamma(z) = \int_0^\infty t^{z-1}e^{-t}dt\,.
</annotation></semantics></math></span><span class="katex-html" aria-hidden="true"><span class="base"><span class="strut" style="height: 1em; vertical-align: -0.25em;"></span><span class="mord">Γ</span><span class="mopen">(</span><span class="mord mathnormal" style="margin-right: 0.04398em;">z</span><span class="mclose">)</span><span class="mspace" style="margin-right: 0.277778em;"></span><span class="mrel">=</span><span class="mspace" style="margin-right: 0.277778em;"></span></span><span class="base"><span class="strut" style="height: 2.32624em; vertical-align: -0.91195em;"></span><span class="mop"><span class="mop op-symbol large-op" style="margin-right: 0.44445em; position: relative; top: -0.001125em;">∫</span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 1.41429em;"><span class="" style="top: -1.78805em; margin-left: -0.44445em; margin-right: 0.05em;"><span class="pstrut" style="height: 2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight">0</span></span></span><span class="" style="top: -3.8129em; margin-right: 0.05em;"><span class="pstrut" style="height: 2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight">∞</span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.91195em;"><span class=""></span></span></span></span></span></span><span class="mspace" style="margin-right: 0.166667em;"></span><span class="mord"><span class="mord mathnormal">t</span><span class="msupsub"><span class="vlist-t"><span class="vlist-r"><span class="vlist" style="height: 0.864108em;"><span class="" style="top: -3.113em; margin-right: 0.05em;"><span class="pstrut" style="height: 2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight"><span class="mord mathnormal mtight" style="margin-right: 0.04398em;">z</span><span class="mbin mtight">−</span><span class="mord mtight">1</span></span></span></span></span></span></span></span></span><span class="mord"><span class="mord mathnormal">e</span><span class="msupsub"><span class="vlist-t"><span class="vlist-r"><span class="vlist" style="height: 0.843556em;"><span class="" style="top: -3.113em; margin-right: 0.05em;"><span class="pstrut" style="height: 2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight"><span class="mord mtight">−</span><span class="mord mathnormal mtight">t</span></span></span></span></span></span></span></span></span><span class="mord mathnormal">d</span><span class="mord mathnormal">t</span><span class="mspace" style="margin-right: 0.166667em;"></span><span class="mord">.</span></span></span></span></span></span></p>
<blockquote>
<p>You can find more information about <strong>LaTeX</strong> mathematical expressions <a href="http://meta.math.stackexchange.com/questions/5020/mathjax-basic-tutorial-and-quick-reference">here</a>.</p>
</blockquote>
<h2 id="uml-diagrams">UML diagrams</h2>
<p>You can render UML diagrams using <a href="https://mermaidjs.github.io/">Mermaid</a>. For example, this will produce a sequence diagram:</p>
<pre class=" language-mermaid"><svg id="mermaid-svg-hERjxT0fiwNnQUN4" width="100%" xmlns="http://www.w3.org/2000/svg" height="531" style="max-width: 815px;" viewBox="-50 -10 815 531"><style>#mermaid-svg-hERjxT0fiwNnQUN4{font-family:"trebuchet ms",verdana,arial,sans-serif;font-size:16px;fill:#000000;}#mermaid-svg-hERjxT0fiwNnQUN4 .error-icon{fill:#552222;}#mermaid-svg-hERjxT0fiwNnQUN4 .error-text{fill:#552222;stroke:#552222;}#mermaid-svg-hERjxT0fiwNnQUN4 .edge-thickness-normal{stroke-width:2px;}#mermaid-svg-hERjxT0fiwNnQUN4 .edge-thickness-thick{stroke-width:3.5px;}#mermaid-svg-hERjxT0fiwNnQUN4 .edge-pattern-solid{stroke-dasharray:0;}#mermaid-svg-hERjxT0fiwNnQUN4 .edge-pattern-dashed{stroke-dasharray:3;}#mermaid-svg-hERjxT0fiwNnQUN4 .edge-pattern-dotted{stroke-dasharray:2;}#mermaid-svg-hERjxT0fiwNnQUN4 .marker{fill:#666;stroke:#666;}#mermaid-svg-hERjxT0fiwNnQUN4 .marker.cross{stroke:#666;}#mermaid-svg-hERjxT0fiwNnQUN4 svg{font-family:"trebuchet ms",verdana,arial,sans-serif;font-size:16px;}#mermaid-svg-hERjxT0fiwNnQUN4 .actor{stroke:hsl(0,0%,83%);fill:#eee;}#mermaid-svg-hERjxT0fiwNnQUN4 text.actor > tspan{fill:#333;stroke:none;}#mermaid-svg-hERjxT0fiwNnQUN4 .actor-line{stroke:#666;}#mermaid-svg-hERjxT0fiwNnQUN4 .messageLine0{stroke-width:1.5;stroke-dasharray:none;stroke:#333;}#mermaid-svg-hERjxT0fiwNnQUN4 .messageLine1{stroke-width:1.5;stroke-dasharray:2,2;stroke:#333;}#mermaid-svg-hERjxT0fiwNnQUN4 #arrowhead path{fill:#333;stroke:#333;}#mermaid-svg-hERjxT0fiwNnQUN4 .sequenceNumber{fill:white;}#mermaid-svg-hERjxT0fiwNnQUN4 #sequencenumber{fill:#333;}#mermaid-svg-hERjxT0fiwNnQUN4 #crosshead path{fill:#333;stroke:#333;}#mermaid-svg-hERjxT0fiwNnQUN4 .messageText{fill:#333;stroke:#333;}#mermaid-svg-hERjxT0fiwNnQUN4 .labelBox{stroke:hsl(0,0%,83%);fill:#eee;}#mermaid-svg-hERjxT0fiwNnQUN4 .labelText,#mermaid-svg-hERjxT0fiwNnQUN4 .labelText > tspan{fill:#333;stroke:none;}#mermaid-svg-hERjxT0fiwNnQUN4 .loopText,#mermaid-svg-hERjxT0fiwNnQUN4 .loopText > tspan{fill:#333;stroke:none;}#mermaid-svg-hERjxT0fiwNnQUN4 .loopLine{stroke-width:2px;stroke-dasharray:2,2;stroke:hsl(0,0%,83%);fill:hsl(0,0%,83%);}#mermaid-svg-hERjxT0fiwNnQUN4 .note{stroke:hsl(60,100%,23.3333333333%);fill:#ffa;}#mermaid-svg-hERjxT0fiwNnQUN4 .noteText,#mermaid-svg-hERjxT0fiwNnQUN4 .noteText > tspan{fill:#333;stroke:none;}#mermaid-svg-hERjxT0fiwNnQUN4 .activation0{fill:#f4f4f4;stroke:#666;}#mermaid-svg-hERjxT0fiwNnQUN4 .activation1{fill:#f4f4f4;stroke:#666;}#mermaid-svg-hERjxT0fiwNnQUN4 .activation2{fill:#f4f4f4;stroke:#666;}#mermaid-svg-hERjxT0fiwNnQUN4:root{--mermaid-font-family:"trebuchet ms",verdana,arial,sans-serif;}#mermaid-svg-hERjxT0fiwNnQUN4 sequence{fill:apa;}</style><g></g><g><line id="actor15" x1="75" y1="5" x2="75" y2="520" class="actor-line" stroke-width="0.5px" stroke="#999"></line><rect x="0" y="0" fill="#eaeaea" stroke="#666" width="150" height="65" rx="3" ry="3" class="actor"></rect><text x="75" y="32.5" dominant-baseline="central" alignment-baseline="central" class="actor" style="text-anchor: middle; font-size: 14px; font-weight: 400; font-family: Open-Sans, &quot;sans-serif&quot;;"><tspan x="75" dy="0">Alice</tspan></text></g><g><line id="actor16" x1="318" y1="5" x2="318" y2="520" class="actor-line" stroke-width="0.5px" stroke="#999"></line><rect x="243" y="0" fill="#eaeaea" stroke="#666" width="150" height="65" rx="3" ry="3" class="actor"></rect><text x="318" y="32.5" dominant-baseline="central" alignment-baseline="central" class="actor" style="text-anchor: middle; font-size: 14px; font-weight: 400; font-family: Open-Sans, &quot;sans-serif&quot;;"><tspan x="318" dy="0">Bob</tspan></text></g><g><line id="actor17eA0IhGW2o2KUq9dBG5gbswYPLL0IQIi6tM3f7dilwZK4TUHQ" width="100%" xmlns="http://www.w3.org/2000/svg" height="531" style="max-width: 815px;" viewBox="-50 -10 815 531"><style>#mermaid-svg-eA0IhGW2o2KUq9dBG5gbswYPLL0IQIi6tM3f7dilwZK4TUHQ{font-family:"trebuchet ms",verdana,arial,sans-serif;font-size:16px;fill:#000000;}#mermaid-svg-eA0IhGW2o2KUq9dBG5gbswYPLL0IQIi6tM3f7dilwZK4TUHQ .error-icon{fill:#552222;}#mermaid-svg-eA0IhGW2o2KUq9dBG5gbswYPLL0IQIi6tM3f7dilwZK4TUHQ .error-text{fill:#552222;stroke:#552222;}#mermaid-svg-eA0IhGW2o2KUq9dBG5gbswYPLL0IQIi6tM3f7dilwZK4TUHQ .edge-thickness-normal{stroke-width:2px;}#mermaid-svg-eA0IhGW2o2KUq9dBG5gbswYPLL0IQIi6tM3f7dilwZK4TUHQ .edge-thickness-thick{stroke-width:3.5px;}#mermaid-svg-eA0IhGW2o2KUq9dBG5gbswYPLL0IQIi6tM3f7dilwZK4TUHQ .edge-pattern-solid{stroke-dasharray:0;}#mermaid-svg-eA0IhGW2o2KUq9dBG5gbswYPLL0IQIi6tM3f7dilwZK4TUHQ .edge-pattern-dashed{stroke-dasharray:3;}#mermaid-svg-eA0IhGW2o2KUq9dBG5gbswYPLL0IQIi6tM3f7dilwZK4TUHQ .edge-pattern-dotted{stroke-dasharray:2;}#mermaid-svg-eA0IhGW2o2KUq9dBG5gbswYPLL0IQIi6tM3f7dilwZK4TUHQ .marker{fill:#666;stroke:#666;}#mermaid-svg-eA0IhGW2o2KUq9dBG5gbswYPLL0IQIi6tM3f7dilwZK4TUHQ .marker.cross{stroke:#666;}#mermaid-svg-eA0IhGW2o2KUq9dBG5gbswYPLL0IQIi6tM3f7dilwZK4TUHQ svg{font-family:"trebuchet ms",verdana,arial,sans-serif;font-size:16px;}#mermaid-svg-eA0IhGW2o2KUq9dBG5gbswYPLL0IQIi6tM3f7dilwZK4TUHQ .actor{stroke:hsl(0,0%,83%);fill:#eee;}#mermaid-svg-eA0IhGW2o2KUq9dBG5gbswYPLL0IQIi6tM3f7dilwZK4TUHQ text.actor > tspan{fill:#333;stroke:none;}#mermaid-svg-eA0IhGW2o2KUq9dBG5gbswYPLL0IQIi6tM3f7dilwZK4TUHQ .actor-line{stroke:#666;}#mermaid-svg-eA0IhGW2o2KUq9dBG5gbswYPLL0IQIi6tM3f7dilwZK4TUHQ .messageLine0{stroke-width:1.5;stroke-dasharray:none;stroke:#333;}#mermaid-svg-eA0IhGW2o2KUq9dBG5gbswYPLL0IQIi6tM3f7dilwZK4TUHQ .messageLine1{stroke-width:1.5;stroke-dasharray:2,2;stroke:#333;}#mermaid-svg-eA0IhGW2o2KUq9dBG5gbswYPLL0IQIi6tM3f7dilwZK4TUHQ #arrowhead path{fill:#333;stroke:#333;}#mermaid-svg-eA0IhGW2o2KUq9dBG5gbswYPLL0IQIi6tM3f7dilwZK4TUHQ .sequenceNumber{fill:white;}#mermaid-svg-eA0IhGW2o2KUq9dBG5gbswYPLL0IQIi6tM3f7dilwZK4TUHQ #sequencenumber{fill:#333;}#mermaid-svg-eA0IhGW2o2KUq9dBG5gbswYPLL0IQIi6tM3f7dilwZK4TUHQ #crosshead path{fill:#333;stroke:#333;}#mermaid-svg-eA0IhGW2o2KUq9dBG5gbswYPLL0IQIi6tM3f7dilwZK4TUHQ .messageText{fill:#333;stroke:#333;}#mermaid-svg-eA0IhGW2o2KUq9dBG5gbswYPLL0IQIi6tM3f7dilwZK4TUHQ .labelBox{stroke:hsl(0,0%,83%);fill:#eee;}#mermaid-svg-eA0IhGW2o2KUq9dB .labelText,#mermaid-svg-eA0IhGW2o2KUq9dB .labelText > tspan{fill:#333;stroke:none;}#mermaid-svg-eA0IhGW2o2KUq9dB .loopText,#mermaid-svg-eA0IhGW2o2KUq9dBG5gbswYPLL0IQIi6tM3f7dilwZK4TUHQ .labelText,#mermaid-svg-G5gbswYPLL0IQIi6tM3f7dilwZK4TUHQ .labelText > tspan{fill:#333;stroke:none;}#mermaid-svg-G5gbswYPLL0IQIi6tM3f7dilwZK4TUHQ .loopText,#mermaid-svg-G5gbswYPLL0IQIi6tM3f7dilwZK4TUHQ .loopText > tspan{fill:#333;stroke:none;}#mermaid-svg-eA0IhGW2o2KUq9dBG5gbswYPLL0IQIi6tM3f7dilwZK4TUHQ .loopLine{stroke-width:2px;stroke-dasharray:2,2;stroke:hsl(0,0%,83%);fill:hsl(0,0%,83%);}#mermaid-svg-eA0IhGW2o2KUq9dBG5gbswYPLL0IQIi6tM3f7dilwZK4TUHQ .note{stroke:hsl(60,100%,23.3333333333%);fill:#ffa;}#mermaid-svg-eA0IhGW2o2KUq9dB .noteText,#mermaid-svg-eA0IhGW2o2KUq9dBG5gbswYPLL0IQIi6tM3f7dilwZK4TUHQ .noteText,#mermaid-svg-G5gbswYPLL0IQIi6tM3f7dilwZK4TUHQ .noteText > tspan{fill:#333;stroke:none;}#mermaid-svg-eA0IhGW2o2KUq9dBG5gbswYPLL0IQIi6tM3f7dilwZK4TUHQ .activation0{fill:#f4f4f4;stroke:#666;}#mermaid-svg-eA0IhGW2o2KUq9dBG5gbswYPLL0IQIi6tM3f7dilwZK4TUHQ .activation1{fill:#f4f4f4;stroke:#666;}#mermaid-svg-eA0IhGW2o2KUq9dBG5gbswYPLL0IQIi6tM3f7dilwZK4TUHQ .activation2{fill:#f4f4f4;stroke:#666;}#mermaid-svg-eA0IhGW2o2KUq9dBG5gbswYPLL0IQIi6tM3f7dilwZK4TUHQ:root{--mermaid-font-family:"trebuchet ms",verdana,arial,sans-serif;}#mermaid-svg-eA0IhGW2o2KUq9dBG5gbswYPLL0IQIi6tM3f7dilwZK4TUHQ sequence{fill:apa;}</style><g></g><g><line id="actor1239" x1="75" y1="5" x2="75" y2="520" class="actor-line" stroke-width="0.5px" stroke="#999"></line><rect x="0" y="0" fill="#eaeaea" stroke="#666" width="150" height="65" rx="3" ry="3" class="actor"></rect><text x="75" y="32.5" dominant-baseline="central" alignment-baseline="central" class="actor" style="text-anchor: middle; font-size: 14px; font-weight: 400; font-family: Open-Sans, &quot;sans-serif&quot;;"><tspan x="75" dy="0">Alice</tspan></text></g><g><line id="actor13410" x1="318" y1="5" x2="318" y2="520" class="actor-line" stroke-width="0.5px" stroke="#999"></line><rect x="243" y="0" fill="#eaeaea" stroke="#666" width="150" height="65" rx="3" ry="3" class="actor"></rect><text x="318" y="32.5" dominant-baseline="central" alignment-baseline="central" class="actor" style="text-anchor: middle; font-size: 14px; font-weight: 400; font-family: Open-Sans, &quot;sans-serif&quot;;"><tspan x="318" dy="0">Bob</tspan></text></g><g><line id="actor5114" x1="540" y1="5" x2="540" y2="520" class="actor-line" stroke-width="0.5px" stroke="#999"></line><rect x="465" y="0" fill="#eaeaea" stroke="#666" width="150" height="65" rx="3" ry="3" class="actor"></rect><text x="540" y="32.5" dominant-baseline="central" alignment-baseline="central" class="actor" style="text-anchor: middle; font-size: 14px; font-weight: 400; font-family: Open-Sans, &quot;sans-serif&quot;;"><tspan x="540" dy="0">John</tspan></text></g><defs><marker id="arrowhead" refX="9" refY="5" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="12" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z"></path></marker></defs><defs><marker id="crosshead" markerWidth="15" markerHeight="8" orient="auto" refX="16" refY="4"><path fill="black" stroke="#000000" stroke-width="1px" d="M 9,2 V 6 L16,4 Z" style="stroke-dasharray: 0, 0;"></path><path fill="none" stroke="#000000" stroke-width="1px" d="M 0,1 L 6,7 M 6,1 L 0,7" style="stroke-dasharray: 0, 0;"></path></marker></defs><defs><marker id="filled-head" refX="18" refY="7" markerWidth="20" markerHeight="28" orient="auto"><path d="M 18,7 L9,13 L14,7 L9,1 Z"></path></marker></defs><defs><marker id="sequencenumber" refX="15" refY="15" markerWidth="60" markerHeight="40" orient="auto"><circle cx="15" cy="15" r="6"></circle></marker></defs><text x="197" y="80" text-anchor="middle" dominant-baseline="middle" alignment-baseline="middle" class="messageText" dy="1em" style="font-family: &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 16px; font-weight: 400;">Hello Bob, how are you?</text><line x1="75" y1="111" x2="318" y2="111" class="messageLine0" stroke-width="2" stroke="none" marker-end="url(#arrowhead)" style="fill: none;"></line><text x="429" y="126" text-anchor="middle" dominant-baseline="middle" alignment-baseline="middle" class="messageText" dy="1em" style="font-family: &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 16px; font-weight: 400;">How about you John?</text><line x1="318" y1="157" x2="540" y2="157" class="messageLine1" stroke-width="2" stroke="none" marker-end="url(#arrowhead)" style="stroke-dasharray: 3, 3; fill: none;"></line><text x="197" y="172" text-anchor="middle" dominant-baseline="middle" alignment-baseline="middle" class="messageText" dy="1em" style="font-family: &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 16px; font-weight: 400;">I am good thanks!</text><line x1="318" y1="203" x2="75" y2="203" class="messageLine1" stroke-width="2" stroke="none" marker-end="url(#crosshead)" style="stroke-dasharray: 3, 3; fill: none;"></line><text x="429" y="218" text-anchor="middle" dominant-baseline="middle" alignment-baseline="middle" class="messageText" dy="1em" style="font-family: &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 16px; font-weight: 400;">I am good thanks!</text><line x1="318" y1="249" x2="540" y2="249" class="messageLine0" stroke-width="2" stroke="none" marker-end="url(#crosshead)" style="fill: none;"></line><g><rect x="565" y="259" fill="#EDF2AE" stroke="#666" width="150" height="84" rx="0" ry="0" class="note"></rect><text x="640" y="264" text-anchor="middle" dominant-baseline="middle" alignment-baseline="middle" class="noteText" dy="1em" style="font-family: &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 14px; font-weight: 400;"><tspan x="640">Bob thinks a long</tspan></text><text x="640" y="280" text-anchor="middle" dominant-baseline="middle" alignment-baseline="middle" class="noteText" dy="1em" style="font-family: &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 14px; font-weight: 400;"><tspan x="640">long time, so long</tspan></text><text x="640" y="296" text-anchor="middle" dominant-baseline="middle" alignment-baseline="middle" class="noteText" dy="1em" style="font-family: &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 14px; font-weight: 400;"><tspan x="640">that the text does</tspan></text><text x="640" y="312" text-anchor="middle" dominant-baseline="middle" alignment-baseline="middle" class="noteText" dy="1em" style="font-family: &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 14px; font-weight: 400;"><tspan x="640">not fit on a row.</tspan></text></g><text x="197" y="358" text-anchor="middle" dominant-baseline="middle" alignment-baseline="middle" class="messageText" dy="1em" style="font-family: &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 16px; font-weight: 400;">Checking with John...</text><line x1="318" y1="389" x2="75" y2="389" class="messageLine1" stroke-width="2" stroke="none" style="stroke-dasharray: 3, 3; fill: none;"></line><text x="308" y="404" text-anchor="middle" dominant-baseline="middle" alignment-baseline="middle" class="messageText" dy="1em" style="font-family: &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 16px; font-weight: 400;">Yes... John, how are you?</text><line x1="75" y1="435" x2="540" y2="435" class="messageLine0" stroke-width="2" stroke="none" style="fill: none;"></line><g><rect x="0" y="455" fill="#eaeaea" stroke="#666" width="150" height="65" rx="3" ry="3" class="actor"></rect><text x="75" y="487.5" dominant-baseline="central" alignment-baseline="central" class="actor" style="text-anchor: middle; font-size: 14px; font-weight: 400; font-family: Open-Sans, &quot;sans-serif&quot;;"><tspan x="75" dy="0">Alice</tspan></text></g><g><rect x="243" y="455" fill="#eaeaea" stroke="#666" width="150" height="65" rx="3" ry="3" class="actor"></rect><text x="318" y="487.5" dominant-baseline="central" alignment-baseline="central" class="actor" style="text-anchor: middle; font-size: 14px; font-weight: 400; font-family: Open-Sans, &quot;sans-serif&quot;;"><tspan x="318" dy="0">Bob</tspan></text></g><g><rect x="465" y="455" fill="#eaeaea" stroke="#666" width="150" height="65" rx="3" ry="3" class="actor"></rect><text x="540" y="487.5" dominant-baseline="central" alignment-baseline="central" class="actor" style="text-anchor: middle; font-size: 14px; font-weight: 400; font-family: Open-Sans, &quot;sans-serif&quot;;"><tspan x="540" dy="0">John</tspan></text></g></svg></pre>
<p>And this will produce a flow chart:</p>
<pre class=" language-mermaid"><svg id="mermaid-svg-3TrGUHc8fOb4mojXwQvVBwAaTz5Yf56Ttmf02bkeyMHK49ikxfLZ0DprHeHLAf3" width="100%" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" height="174.4375" style="max-width: 502.74749755859375px;" viewBox="0 0 502.74749755859375 174.4375"><style>#mermaid-svg-3TrGUHc8fOb4mojX{font-family:"trebuchet ms",verdana,arial,sans-serif;font-size:16px;fill:#000000;}#mermaid-svg-3TrGUHc8fOb4mojX .error-icon{fill:#552222;}#mermaid-svg-3TrGUHc8fOb4mojX .error-text{fill:#552222;stroke:#552222;}#mermaid-svg-3TrGUHc8fOb4mojX .edge-thickness-normal{stroke-width:2px;}#mermaid-svg-3TrGUHc8fOb4mojX .edge-thickness-thick{stroke-width:3.5px;}#mermaid-svg-3TrGUHc8fOb4mojX .edge-pattern-solid{stroke-dasharray:0;}#mermaid-svg-3TrGUHc8fOb4mojX .edge-pattern-dashed{stroke-dasharray:3;}#mermaid-svg-3TrGUHc8fOb4mojX .edge-pattern-dotted{stroke-dasharray:2;}#mermaid-svg-3TrGUHc8fOb4mojX .marker{fill:#666;stroke:#666;}#mermaid-svg-3TrGUHc8fOb4mojX .marker.cross{stroke:#666;}#mermaid-svg-3TrGUHc8fOb4mojX svg{font-family:"trebuchet ms",verdana,arial,sans-serif;font-size:16px;}#mermaid-svg-3TrGUHc8fOb4mojX .label{font-family:"trebuchet ms",verdana,arial,sans-serif;color:#000000;}#mermaid-svg-3TrGUHc8fOb4mojX .cluster-label text{fill:#333;}#mermaid-svg-3TrGUHc8fOb4mojX .cluster-label span{color:#333;}#mermaid-svg-3TrGUHc8fOb4mojX .label text,#mermaid-svg-3TrGUHc8fOb4mojX span{fill:#000000;color:#000000;}#mermaid-svg-3TrGUHc8fOb4mojX .node rect,#mermaid-svg-3TrGUHc8fOb4mojX .node circle,#mermaid-svg-3TrGUHc8fOb4mojX .node ellipse,#mermaid-svg-3TrGUHc8fOb4mojX .node polygon,#mermaid-svg-3TrGUHc8fOb4mojX .node path{fill:#eee;stroke:#999;stroke-width:1px;}#mermaid-svg-3TrGUHc8fOb4mojX .node .label{text-align:center;}#mermaid-svg-3TrGUHc8fOb4mojX .node.clickable{cursor:pointer;}#mermaid-svg-3TrGUHc8fOb4mojX .arrowheadPath{fill:#333333;}#mermaid-svg-3TrGUHc8fOb4mojX .edgePath .path{stroke:#666;stroke-width:1.5px;}#mermaid-svg-3TrGUHc8fOb4mojX .flowchart-link{stroke:#666;fill:none;}#mermaid-svg-3TrGUHc8fOb4mojX .edgeLabel{background-color:white;text-align:center;}#mermaid-svg-3TrGUHc8fOb4mojX .edgeLabel rect{opacity:0.5;background-color:white;fill:white;}#mermaid-svg-3TrGUHc8fOb4mojX .cluster rect{fill:hsl(210,66.6666666667%,95%);stroke:#26a;stroke-width:1px;}#mermaid-svg-3TrGUHc8fOb4mojX .cluster text{fill:#333;}#mermaid-svg-3TrGUHc8fOb4mojX .cluster span{color:#333;}#mermaid-svg-3TrGUHc8fOb4mojX div.mermaidTooltip{position:absolute;text-align:center;max-width:200px;padding:2px;font-family:"trebuchet ms",verdana,arial,sans-serif;font-size:12px;background:hsl(-160,0%,93.3333333333%);border:1px solid #26a;border-radius:2px;pointer-events:none;z-index:100;}#mermaid-svg-3TrGUHc8fOb4mojX:root{--mermaid-font-family:"trebuchet ms",verdana,arial,sans-serif;}#mermaid-svg-3TrGUHc8fOb4mojX flowchart{fill:apa;}</style><g><g class="output"><g class="clusters"></g><g class="edgePaths"><g class="edgePath LS-A LE-B" id="L-A-B" style="opacity: 1;"><path class="path" d="M109.65658351563049,67.6156234741211L170.05624961853027,38.86249923706055L246.12499809265137,38.86249923706055" marker-end="url(https://stackedit.io/app#arrowhead13)" style="fill:none"></path><defs><marker id="arrowhead13" viewBox="0 0 10 10" refX="9" refY="5" markerUnits="strokeWidth" markerWidth="8" markerHeight="6" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" class="arrowheadPath" style="stroke-width: 1; stroke-dasharray: 1, 0;"></path></marker></defs></g><g class="edgePath LS-A LE-C" id="L-A-C" style="opacity: 1;"><path class="path" d="M109.65658351563049,114.328125L170.05624961853027,143.08124923706055L226.92499923706055,143.08124923706055" marker-end="url(https://stackedit.io/app#arrowhead14)" style="fill:none"></path><defs><marker id="arrowhead14" viewBox="0 0 10 10" refX="9" refY="5" markerUnits="strokeWidth" markerWidth="8" markerHeight="6" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" class="arrowheadPath" style="stroke-width: 1; stroke-dasharray: 1, 0;"></path></marker></defs></g><g class="edgePath LS-B LE-D" id="L-B-D" style="opacity: 1;"><path class="path" d="M307.8500003814697,38.86249923706055L352.04999923706055,38.86249923706055L400.10526402645604,68.91660820788849" marker-end="url(https://stackedit.io/app#arrowhead15)" style="fill:none"></path><defs><marker id="arrowhead15" viewBox="0 0 10 10" refX="9" refY="5" markerUnits="strokeWidth" markerWidth="8" markerHeight="6" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" class="arrowheadPath" style="stroke-width: 1; stroke-dasharray: 1, 0;"></path></marker></defs></g><g class="edgePath LS-C LE-D" id="L-C-D" style="opacity: 1;"><path class="path" d="M327.04999923706055,143.08124923706055L352.04999923706055,143.08124923706055L400.105265555658,114.02713931588139" marker-end="url(https://stackedit.io/app#arrowhead16)" style="fill:none"></path><defs><marker id="arrowhead16" viewBox="0 0 10 10" refX="9" refY="5" markerUnits="strokeWidth" markerWidth="8" markerHeight="6" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" class="arrowheadPath" style="stroke-width: 1; stroke-dasharray: 1, 0;"></path></marker></defs></g></g><g class="edgeLabels"><g class="edgeLabel" transform="translate(170.05624961853027,38.86249923706055)" style="opacity: 1;"><g transform="translate(-31.868749618530273,-13.356249809265137)" class="label"><rect rx="0" ry="0" width="63.73749923706055" height="26.712499618530273"></rect><foreignObject width="63.73749923706055" height="26.712499618530273"><div xmlns="http://www.w3.org/1999/xhtml" style="display: inline-block; white-space: nowrap;"><span id="L-L-A-B" class="edgeLabel L-LS-A' L-LE-B">Link text</span></div></foreignObject></g></g><g class="edgeLabel" transform="" style="opacity: 1;"><g transform="translate(0,0)" class="label"><rect rx="0" ry="0" width="0" height="0"></rect><foreignObject width="0" height="0"><div xmlns="http://www.w3.org/1999/xhtml" style="display: inline-block; white-space: nowrap;"><span id="L-L-A-C" class="edgeLabel L-LS-A' L-LE-C"></span></div></foreignObject></g></g><g class="edgeLabel" transform="" style="opacity: 1;"><g transform="translate(0,0)" class="label"><rect rx="0" ry="0" width="0" height="0"></rect><foreignObject width="0" height="0"><div xmlns="http://www.w3.org/1999/xhtml" style="display: inline-block; white-space: nowrap;"><span id="L-L-B-D" class="edgeLabel L-LS-B' L-LE-D"></span></div></foreignObject></g></g><g class="edgeLabel" transform="" style="opacity: 1;"><g transform="translate(0,0)" class="label"><rect rx="0" ry="0" width="0" height="0"></rect><foreignObject width="0" height="0"><div xmlns="http://www.w3.org/1999/xhtml" style="display: inline-block; white-space: nowrap;"><span id="L-L-C-D" class="edgeLabel L-LS-C' L-LE-D"></span></div></foreignObject></g></g></g><g class="nodes"><g class="node default" id="flowchart-A-56" transform="translate(60.59375,90.97187423706055)" style="opacity: 1;"><rect rx="0" ry="0" x="-52.59375" y="-23.356249809265137" width="105.1875" height="46.71249961853027" class="label-container"></rect><g class="label" transform="translate(0,0)"><g transform="translate(-42.59375,-13.356249809265137)"><foreignObject width="85.1875" height="26.712499618530273"><div xmlns="http://www.w3.org/1999/xhtml" style="display: inline-block; white-space: nowrap;">Square Rect</div></foreignObject></g></g></g><g class="node default" id="flowchart-B-57" transform="translate(276.98749923706055,38.86249923706055)" style="opacity: 1;"><circle x="-30.86250114440918" y="-23.356249809265137" r="30.86250114440918" class="label-container"></circle><g class="label" transform="translate(0,0)"><g transform="translate(-20.86250114440918,-13.356249809265137)"><foreignObject width="41.72500228881836" height="26.712499618530273"><div xmlns="http://www.w3.org/1999/xhtml" style="display: inline-block; white-space: nowrap;">Circle</div></foreignObject></g></g></g><g class="node default" id="flowchart-C-59" transform="translate(276.98749923706055,143.08124923706055)" style="opacity: 1;"><rect rx="5" ry="5" x="-50.0625" y="-23.356249809265137" width="100.125" height="46.71249961853027" class="label-container"></rect><g class="label" transform="translate(0,0)"><g transform="translate(-40.0625,-13.356249809265137)"><foreignObject width="80.125" height="26.712499618530273"><div xmlns="http://www.w3.org/1999/xhtml" style="display: inline-block; white-space: nowrap;">Round Rect</div></foreignObject></g></g></g><g class="node default" id="flowchart-D-61wQvVBwAaTz5Yf56Ttmf02bkeyMHK49ikxfLZ0DprHeHLAf3{font-family:"trebuchet ms",verdana,arial,sans-serif;font-size:16px;fill:#000000;}#mermaid-svg-wQvVBwAaTz5Yf56Ttmf02bkeyMHK49ikxfLZ0DprHeHLAf3 .error-icon{fill:#552222;}#mermaid-svg-wQvVBwAaTz5Yf56Ttmf02bkeyMHK49ikxfLZ0DprHeHLAf3 .error-text{fill:#552222;stroke:#552222;}#mermaid-svg-wQvVBwAaTz5Yf56Ttmf02bkeyMHK49ikxfLZ0DprHeHLAf3 .edge-thickness-normal{stroke-width:2px;}#mermaid-svg-wQvVBwAaTz5Yf56Ttmf02bkeyMHK49ikxfLZ0DprHeHLAf3 .edge-thickness-thick{stroke-width:3.5px;}#mermaid-svg-wQvVBwAaTz5Yf56Ttmf02bkeyMHK49ikxfLZ0DprHeHLAf3 .edge-pattern-solid{stroke-dasharray:0;}#mermaid-svg-wQvVBwAaTz5Yf56Ttmf02bkeyMHK49ikxfLZ0DprHeHLAf3 .edge-pattern-dashed{stroke-dasharray:3;}#mermaid-svg-wQvVBwAaTz5Yf56Ttmf02bkeyMHK49ikxfLZ0DprHeHLAf3 .edge-pattern-dotted{stroke-dasharray:2;}#mermaid-svg-wQvVBwAaTz5Yf56Ttmf02bkeyMHK49ikxfLZ0DprHeHLAf3 .marker{fill:#666;stroke:#666;}#mermaid-svg-wQvVBwAaTz5Yf56Ttmf02bkeyMHK49ikxfLZ0DprHeHLAf3 .marker.cross{stroke:#666;}#mermaid-svg-wQvVBwAaTz5Yf56Ttmf02bkeyMHK49ikxfLZ0DprHeHLAf3 svg{font-family:"trebuchet ms",verdana,arial,sans-serif;font-size:16px;}#mermaid-svg-wQvVBwAaTz5Yf56Ttmf02bkeyMHK49ikxfLZ0DprHeHLAf3 .label{font-family:"trebuchet ms",verdana,arial,sans-serif;color:#000000;}#mermaid-svg-wQvVBwAaTz5Yf56Ttmf02bkeyMHK49ikxfLZ0DprHeHLAf3 .cluster-label text{fill:#333;}#mermaid-svg-wQvVBwAaTz5Yf56Ttmf02bkeyMHK49ikxfLZ0DprHeHLAf3 .cluster-label span{color:#333;}#mermaid-svg-wQvVBwAaTz5Yf56T .label text,#mermaid-svg-wQvVBwAaTz5Yf56T span{fill:#000000;color:#000000;}#mermaid-svg-wQvVBwAaTz5Yf56T .node rect,#mermaid-svg-wQvVBwAaTz5Yf56T .node circle,#mermaid-svg-wQvVBwAaTz5Yf56T .node ellipse,#mermaid-svg-wQvVBwAaTz5Yf56T .node polygon,#mermaid-svg-wQvVBwAaTz5Yf56Ttmf02bkeyMHK49ikxfLZ0DprHeHLAf3 .label text,#mermaid-svg-wtmf02bkeyMHK49ikxfLZ0DprHeHLAf3 span{fill:#000000;color:#000000;}#mermaid-svg-wtmf02bkeyMHK49ikxfLZ0DprHeHLAf3 .node rect,#mermaid-svg-wtmf02bkeyMHK49ikxfLZ0DprHeHLAf3 .node circle,#mermaid-svg-wtmf02bkeyMHK49ikxfLZ0DprHeHLAf3 .node ellipse,#mermaid-svg-wtmf02bkeyMHK49ikxfLZ0DprHeHLAf3 .node polygon,#mermaid-svg-wtmf02bkeyMHK49ikxfLZ0DprHeHLAf3 .node path{fill:#eee;stroke:#999;stroke-width:1px;}#mermaid-svg-wQvVBwAaTz5Yf56Ttmf02bkeyMHK49ikxfLZ0DprHeHLAf3 .node .label{text-align:center;}#mermaid-svg-wQvVBwAaTz5Yf56Ttmf02bkeyMHK49ikxfLZ0DprHeHLAf3 .node.clickable{cursor:pointer;}#mermaid-svg-wQvVBwAaTz5Yf56Ttmf02bkeyMHK49ikxfLZ0DprHeHLAf3 .arrowheadPath{fill:#333333;}#mermaid-svg-wQvVBwAaTz5Yf56Ttmf02bkeyMHK49ikxfLZ0DprHeHLAf3 .edgePath .path{stroke:#666;stroke-width:1.5px;}#mermaid-svg-wQvVBwAaTz5Yf56Ttmf02bkeyMHK49ikxfLZ0DprHeHLAf3 .flowchart-link{stroke:#666;fill:none;}#mermaid-svg-wQvVBwAaTz5Yf56Ttmf02bkeyMHK49ikxfLZ0DprHeHLAf3 .edgeLabel{background-color:white;text-align:center;}#mermaid-svg-wQvVBwAaTz5Yf56Ttmf02bkeyMHK49ikxfLZ0DprHeHLAf3 .edgeLabel rect{opacity:0.5;background-color:white;fill:white;}#mermaid-svg-wQvVBwAaTz5Yf56Ttmf02bkeyMHK49ikxfLZ0DprHeHLAf3 .cluster rect{fill:hsl(210,66.6666666667%,95%);stroke:#26a;stroke-width:1px;}#mermaid-svg-wQvVBwAaTz5Yf56Ttmf02bkeyMHK49ikxfLZ0DprHeHLAf3 .cluster text{fill:#333;}#mermaid-svg-wQvVBwAaTz5Yf56Ttmf02bkeyMHK49ikxfLZ0DprHeHLAf3 .cluster span{color:#333;}#mermaid-svg-wQvVBwAaTz5Yf56Ttmf02bkeyMHK49ikxfLZ0DprHeHLAf3 div.mermaidTooltip{position:absolute;text-align:center;max-width:200px;padding:2px;font-family:"trebuchet ms",verdana,arial,sans-serif;font-size:12px;background:hsl(-160,0%,93.3333333333%);border:1px solid #26a;border-radius:2px;pointer-events:none;z-index:100;}#mermaid-svg-wQvVBwAaTz5Yf56Ttmf02bkeyMHK49ikxfLZ0DprHeHLAf3:root{--mermaid-font-family:"trebuchet ms",verdana,arial,sans-serif;}#mermaid-svg-wQvVBwAaTz5Yf56Ttmf02bkeyMHK49ikxfLZ0DprHeHLAf3 flowchart{fill:apa;}</style><g><g class="output"><g class="clusters"></g><g class="edgePaths"><g class="edgePath LS-A LE-B" id="L-A-B" style="opacity: 1;"><path class="path" d="M109.65658351563049,67.6156234741211L170.05624961853027,38.86249923706055L246.12499809265137,38.86249923706055" marker-end="url(https://stackedit.io/app#arrowhead95)" style="fill:none"></path><defs><marker id="arrowhead95" viewBox="0 0 10 10" refX="9" refY="5" markerUnits="strokeWidth" markerWidth="8" markerHeight="6" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" class="arrowheadPath" style="stroke-width: 1; stroke-dasharray: 1, 0;"></path></marker></defs></g><g class="edgePath LS-A LE-C" id="L-A-C" style="opacity: 1;"><path class="path" d="M109.65658351563049,114.328125L170.05624961853027,143.08124923706055L226.92499923706055,143.08124923706055" marker-end="url(https://stackedit.io/app#arrowhead106)" style="fill:none"></path><defs><marker id="arrowhead106" viewBox="0 0 10 10" refX="9" refY="5" markerUnits="strokeWidth" markerWidth="8" markerHeight="6" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" class="arrowheadPath" style="stroke-width: 1; stroke-dasharray: 1, 0;"></path></marker></defs></g><g class="edgePath LS-B LE-D" id="L-B-D" style="opacity: 1;"><path class="path" d="M307.8500003814697,38.86249923706055L352.04999923706055,38.86249923706055L400.10526402645604,68.91660820788849" marker-end="url(https://stackedit.io/app#arrowhead117)" style="fill:none"></path><defs><marker id="arrowhead117" viewBox="0 0 10 10" refX="9" refY="5" markerUnits="strokeWidth" markerWidth="8" markerHeight="6" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" class="arrowheadPath" style="stroke-width: 1; stroke-dasharray: 1, 0;"></path></marker></defs></g><g class="edgePath LS-C LE-D" id="L-C-D" style="opacity: 1;"><path class="path" d="M327.04999923706055,143.08124923706055L352.04999923706055,143.08124923706055L400.105265555658,114.02713931588139" marker-end="url(https://stackedit.io/app#arrowhead128)" style="fill:none"></path><defs><marker id="arrowhead128" viewBox="0 0 10 10" refX="9" refY="5" markerUnits="strokeWidth" markerWidth="8" markerHeight="6" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" class="arrowheadPath" style="stroke-width: 1; stroke-dasharray: 1, 0;"></path></marker></defs></g></g><g class="edgeLabels"><g class="edgeLabel" transform="translate(170.05624961853027,38.86249923706055)" style="opacity: 1;"><g transform="translate(-31.868749618530273,-13.356249809265137)" class="label"><rect rx="0" ry="0" width="63.73749923706055" height="26.712499618530273"></rect><foreignObject width="63.73749923706055" height="26.712499618530273"><div xmlns="http://www.w3.org/1999/xhtml" style="display: inline-block; white-space: nowrap;"><span id="L-L-A-B" class="edgeLabel L-LS-A' L-LE-B">Link text</span></div></foreignObject></g></g><g class="edgeLabel" transform="" style="opacity: 1;"><g transform="translate(0,0)" class="label"><rect rx="0" ry="0" width="0" height="0"></rect><foreignObject width="0" height="0"><div xmlns="http://www.w3.org/1999/xhtml" style="display: inline-block; white-space: nowrap;"><span id="L-L-A-C" class="edgeLabel L-LS-A' L-LE-C"></span></div></foreignObject></g></g><g class="edgeLabel" transform="" style="opacity: 1;"><g transform="translate(0,0)" class="label"><rect rx="0" ry="0" width="0" height="0"></rect><foreignObject width="0" height="0"><div xmlns="http://www.w3.org/1999/xhtml" style="display: inline-block; white-space: nowrap;"><span id="L-L-B-D" class="edgeLabel L-LS-B' L-LE-D"></span></div></foreignObject></g></g><g class="edgeLabel" transform="" style="opacity: 1;"><g transform="translate(0,0)" class="label"><rect rx="0" ry="0" width="0" height="0"></rect><foreignObject width="0" height="0"><div xmlns="http://www.w3.org/1999/xhtml" style="display: inline-block; white-space: nowrap;"><span id="L-L-C-D" class="edgeLabel L-LS-C' L-LE-D"></span></div></foreignObject></g></g></g><g class="nodes"><g class="node default" id="flowchart-A-240" transform="translate(60.59375,90.97187423706055)" style="opacity: 1;"><rect rx="0" ry="0" x="-52.59375" y="-23.356249809265137" width="105.1875" height="46.71249961853027" class="label-container"></rect><g class="label" transform="translate(0,0)"><g transform="translate(-42.59375,-13.356249809265137)"><foreignObject width="85.1875" height="26.712499618530273"><div xmlns="http://www.w3.org/1999/xhtml" style="display: inline-block; white-space: nowrap;">Square Rect</div></foreignObject></g></g></g><g class="node default" id="flowchart-B-4125" transform="translate(276.98749923706055,38.86249923706055)" style="opacity: 1;"><circle x="-30.86250114440918" y="-23.356249809265137" r="30.86250114440918" class="label-container"></circle><g class="label" transform="translate(0,0)"><g transform="translate(-20.86250114440918,-13.356249809265137)"><foreignObject width="41.72500228881836" height="26.712499618530273"><div xmlns="http://www.w3.org/1999/xhtml" style="display: inline-block; white-space: nowrap;">Circle</div></foreignObject></g></g></g><g class="node default" id="flowchart-C-4327" transform="translate(276.98749923706055,143.08124923706055)" style="opacity: 1;"><rect rx="5" ry="5" x="-50.0625" y="-23.356249809265137" width="100.125" height="46.71249961853027" class="label-container"></rect><g class="label" transform="translate(0,0)"><g transform="translate(-40.0625,-13.356249809265137)"><foreignObject width="80.125" height="26.712499618530273"><div xmlns="http://www.w3.org/1999/xhtml" style="display: inline-block; white-space: nowrap;">Round Rect</div></foreignObject></g></g></g><g class="node default" id="flowchart-D-4529" transform="translate(435.8987503051758,90.97187423706055)" style="opacity: 1;"><polygon points="58.848749828338626,0 117.69749965667725,-58.848749828338626 58.848749828338626,-117.69749965667725 0,-58.848749828338626" transform="translate(-58.848749828338626,58.848749828338626)" class="label-container"></polygon><g class="label" transform="translate(0,0)"><g transform="translate(-32.03125,-13.356249809265137)"><foreignObject width="64.0625" height="26.712499618530273"><div xmlns="http://www.w3.org/1999/xhtml" style="display: inline-block; white-space: nowrap;">Rhombus</div></foreignObject></g></g></g></g></g></g></svg></pre>

<!--stackedit_data:
eyJoaXN0b3J5IjpbLTE0NDg4OTI5MjhdfQ==
-->
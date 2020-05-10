# Big Data Platform

Big Data Platform (PoC) to run a Corona App .... whatever

## TODO
Description of idea, architecture, design and screenshots of demo  
Licence for code (Apache) for documentation (Creative Commons)
....

### Prerequisites

TODO: What things you need to install the software and how to install them

```
Docker
minikube
helm
```
## Starting minikube on Win 10

Start minicube with Hyper V driver (make sure Hyper V is enabled)
```
minikube start --driver=hyperv --memory 4096 --cpus 4
```
Pointing Docker daemon to minicube regestry
```
minikube docker-env
minikube -p minikube docker-env | Invoke-Expression
```

## Trying to deploy HDFS and Apache Spark on K8S:
### Deploying HDFS

Add helm stable repo and 
install chart for stable hadoop cluster
```
helm repo add stable https://kubernetes-charts.storage.googleapis.com/
# if unsing helm for the first time run "helm init"
helm install --namespace=default --set hdfs.dataNode.replicas=2 --set yarn.nodeManager.replicas=2 --set hdfs.webhdfs.enabled=true --name my-hadoop-cluster stable/hadoop
```

Install Apache Knox - REST API and Application Gateway
using helm chart pfisterer/apache-knox-helm

```
helm repo add pfisterer-knox https://pfisterer.github.io/apache-knox-helm/
helm install  --set "knox.hadoop.nameNodeUrl=hdfs://my-hadoop-cluster-hadoop-hdfs-nn:9000/" --set "knox.hadoop.resourceManagerUrl=http://my-hadoop-cluster-hadoop-yarn-rm:8088/ws"  --set "knox.hadoop.webHdfsUrl=http://my-hadoop-cluster-hadoop-hdfs-nn:50070/webhdfs/" --set "knox.hadoop.hdfsUIUrl=http://my-hadoop-cluster-hadoop-hdfs-nn:50070" --set "knox.hadoop.yarnUIUrl=http://my-hadoop-cluster-hadoop-yarn-ui:8088" --set "knox.servicetype=LoadBalancer" --name knox pfisterer-knox/apache-knox-helm
```

To be able to PUT your files to HDFS via REST API need to know IP/webhdfs/v1
### TODO: put a data file and a pyspark program into hdfs and run it with spark-submit using csturm/spark-py image




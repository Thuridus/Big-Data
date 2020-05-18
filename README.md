# Big Data Platform :poop:

Big Data Platform (PoC) to run a Corona App .... whatever

## TODO
Description of idea, architecture, design and screenshots of demo  
Licence for documentation (Creative Commons)
....

### Prerequisites

TODO: What things you need to install the software and how to install them

```
Docker
minikube
helm
? python3 spark pyspark 
```
## Starting minikube

Start minicube with Hyper V driver (make sure Hyper V is enabled)
```
#on Win 10
minikube start --driver=hyperv --memory 5120 --cpus 4

#on Mac
minikube start --vm-driver=hyperkit --memory 5120 --cpus 4
```
Pointing Docker daemon to minicube regestry
```
#on Win 10
minikube docker-env
minikube -p minikube docker-env | Invoke-Expression

#on Mac
eval $(minikube docker-env)
```

## Deploy HDFS and Apache Spark on K8S:
### Deploying HDFS

Add helm stable repo and 
install chart for stable hadoop cluster
```
helm repo add stable https://kubernetes-charts.storage.googleapis.com/
# if unsing helm for the first time run "helm init"
helm install --namespace=default --set hdfs.dataNode.replicas=2 --set yarn.nodeManager.replicas=1 --set hdfs.webhdfs.enabled=true hadoop stable/hadoop
```

Adjust user rights on root folder to be able to acces filesystem via WEBHDFS
```
kubectl exec -ti hadoop-hadoop-yarn-rm-0 bash
hdfs dfs -chmod  777 /
exit
```

Install Apache Knox - REST API and Application Gateway
using helm chart pfisterer/apache-knox-helm
```
helm repo add pfisterer-knox https://pfisterer.github.io/apache-knox-helm/
helm install --set "knox.hadoop.nameNodeUrl=hdfs://hadoop-hadoop-hdfs-nn:9000/" --set "knox.hadoop.resourceManagerUrl=http://hadoop-hadoop-yarn-rm:8088/ws" --set "knox.hadoop.webHdfsUrl=http://hadoop-hadoop-hdfs-nn:50070/webhdfs/" --set "knox.hadoop.hdfsUIUrl=http://hadoop-hadoop-hdfs-nn:50070" --set "knox.hadoop.yarnUIUrl=http://hadoop-hadoop-yarn-ui:8088" --set "knox.servicetype=LoadBalancer" knox pfisterer-knox/apache-knox-helm
```

## Deploy the periodic import pod
### Create necessary docker image for Data import POD
```
# After running the docker-env command, navigate to the python_hdfs directory (it contains one dockerfile)
# the created image will connect to the knox-apache-knox-helm-svc via DNS Lookup within the K8S cluster
docker build -t python_download .
```
Apply the import deployment
```
#navigate to the python_hdfs directory
kubectl apply -f python_import_deployment.yml
```

To be able to PUT your files to HDFS via REST API need to know IP/webhdfs/v1
```
# This command returns the external web address of the service that's hosting the knox service for the webhdfs API
minikube service knox-apache-knox-helm-svc --url
```

### TODO: put a pyspark program into hdfs and run it with spark-submit using csturm/spark-py image



## Connection to the Database

### Create necessary POD

Build a connection to the my-database folder
```cd my-database
```

Apply the import deployment
```
#navigate to the folder my-database
kubectl apply -f my-mysql-deployment.yml
```
```
#To be sure that the POD is running and to get the POD-name, enter
kubectl get pods -o wide
```

```
#Enter the pod to check if its working
kubectl exec -ti [POD-name] -- mysql -u root --password=mysecretpw
```
Build a connection to the database "my-database.sql" and get the entries
```kubectl exec -ti [POD-name] -- mysql -u root --password=mysecretpw
   USE mysqldb
```

```
#Get all entries from database
Select * from infects"
```



# Big Data Platform :poop:

Big Data Platform (PoC) to run a Corona App .... whatever


## Big Data Architecture


### Grundsätzliche Idee und Architektur:
* HDFS speicher Daten zu Börse und Covid
* Über Kafka Cluster wird von HDFS eine msg an Appache Spark über neue Daten gesendet
* Appache Spark fordert Daten von HDFS an (?) über Schnittstelle (?)
* Appache Spark verarbeitet die Daten und sendet diese an den DB-Server
* DB Server speichert die Daten in einer rationalen Datenbank
* Web-Server ruft über Schnittstelle die Daten aus der rationalen Datenbank ab
* Web-Frontend zeigt dem Nutzer Covid und Börsen Daten
* Nutzer kann Betrachtungszeitraum einstellen
* Details zu den Komponenten siehe unten

Hier ist die Abbildung

### HDFS:
* Daten aus Börse (Quelle Link) und Daten aus Covid (Quelle Link) werden gespeichert
* Daten Covid werden alle X aktualisiert.
* Daten Börse werden alle Y aktualisiert.
* HDFS ist Kafka Producer: Sendet msg über Kafka Cluster an Appache Spark Consumer, wenn neue Daten verfügbar sind.

### Kafka:
* Messaging System zwischen Appache Spark und HDFS.
* Kafka Cluster wird über Helm hochgefahren (?).
* Kafka Producer: HDFS
* Kafka Consumer: Appache Spark
* Topic: X
* Replikation: Y
* Bootstrap:
* Mögliche Erweiterung:
  * Web Servcer Producer Nutzungsdaten sendet Nutzungsdaten der Weboberfläche an Data Lake Consumer.
* ...

### Appache Spark:
* Dient dem Data Processing der Daten aus HDFS
* Wenn Appache Spark Consumer msg erhält dass neue Daten in HDFS sind dann (Was passiert dann?)
* ...
* Appache Spark verarbeitet Daten (wie?)

### Database Server:
* Rationale Datenbank speichert von Appache Kafka aufbereitete Daten.
* Tabelle sieht so aus: ....

### Web Server: 
* Frontend:
  * Zeigt Grafik zu den Daten Covid und Börse an (X-Achse Zeit und Y-Achse Ansteckungen / Kurs)
  * Nutzer können Zeitraum auswählen in denen Korrelationen angezeigt werden
* Backend:
  * Daten werden aus DB gezogen (Was passiert genau?)
  * ...

### Cache Server:
* ?

### Load Balancer:
* ? 


 

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
## Spark on K8S
### TODO: not fully working yet :/
Put the pyspark program into hdfs and run it with spark-submit using csturm/spark-py image
```
kubectl exec -ti hadoop-hadoop-yarn-rm-0 -- bash

hdfs dfs -mkdir -p app
hdfs dfs -mkdir -p input
hdfs dfs -mkdir -p input/fse
hdfs dfs -mkdir -p input/infections
hdfs dfs -mkdir -p tmp
hdfs dfs -mkdir -p tmp/results
hdfs dfs -mkdir -p tmp/results/corona
hdfs dfs -mkdir -p tmp/results/dax

# not working, trying to find a workround
curl https://github.com/Thuridus/Big-Data/blob/develop/pyspark-app/pyspark_driver.py| hdfs dfs -put - app/
Curl https://github.com/Thuridus/Big-Data/blob/develop/python_hdfs/infections.csv| hdfs dfs -put - input/infections
Curl https://github.com/Thuridus/Big-Data/blob/develop/python_hdfs/quandl_fse.csv| hdfs dfs -put - input/fse
```
Get IP of kubernetes master 
```
kubectl cluster-info
```
Start Spark using IP of kubernetes master 
```
spark-submit --master k8s://https://{Kubernetes-master-IP:Port} --deploy-mode cluster --name pyspark_driver --conf spark.executor.instances=2 --conf spark.kubernetes.container.image=csturm/spark-py:v2.4.4  hdfs://hadoop-hadoop-hdfs-nn:9000/app/pyspark_driver.py
```

## Connection to the Database

### Create necessary POD

Build a connection to the "my-database" folder
```
#navigate to the folder my-database
cd my-database
```

Create a POD and deploy it to minikube
```
kubectl apply -f my-mysql-deployment.yml
```
```
#To be sure that the POD is running and to get the POD-name, enter
kubectl get pods -o wide
#You have to choose the POD with the name my-mysql-deployment-xxxxxxxxx-xxxxx (x=numbers/characters)
```

```
#Enter the pod to check if its working
kubectl exec -ti [my-mysql-deployment-xxxxxxxxx-xxxxx] -- mysql -u root --password=mysecretpw
```

### Create Connection to database

Build a connection to the database "my-database.sql" and get the entries
```
#kubectl exec -ti [my-mysql-deployment-xxxxxxxxx-xxxxx] -- mysql -u root --password=mysecretpw
USE mysqldb
```

```
#Get all entries from database (e.x from the table infects) with a sql-statement
Select * from infects;
```

```
#Leave the database
exit
```



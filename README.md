# :fireworks: Big Data Platform :fireworks:

Big Data Platform to run a Corona App via Web. The aim of the project is to provide an correlative illustration between the index "Deutsche Aktien Index" (DAX) and the COVID-19 infections or deaths.

Check "Big Data Architecture" for further information about the functionality and the file Big-Data/LICENCE for lincensification.

## Inhaltsverzeichnis
1. [Big Data Architecture](#architecture)
2. [Funktionsweise der Benutzeroberfläche](#oberfläche)
3. [Starting minikube](#minikube)
4. [Deploy HDFS on K8S](#k8s)
5. [Deploy the periodic import pod on K8S](#deplox)
6. [Deploy Kafka cluster on K8S](#kafkacluser)
7. [Deploy Spark on K8S](#sparkk8s)
8. [Deploy the database](#deploydb)
9. [Start User-Interface](#deployinterface)

## :paperclip: Unsere To-Do-Liste (wird später gelöscht)
Unsere to-dos aus dem Pfisterer PDF https://elearning.cas.dhbw.de/pluginfile.php?forcedownload=1&file=%2F%2F69764%2Fblock_quickmail%2Fattachment_log%2F1700%2FAufgabenstellung%20Big%20Data%20Vorlesung%20April%202020.pdf

- [X] Komponente: Data-Lake (HDFS)
- [X] Komponente: Big Data Messaging (Kafka)
- [ ] Komponente: Big Data Processing (Apache Spark)=> Integration fehlt
- [X] Komponente: DB Server (mysql)
- [X] Komponente: Load Balancer (Ingress)
- [ ] Komponente: Web Server => Fehlerbehebung läuft
- [ ] Komponente: Cache Server => Fehlerbehebung läuft
- [X] Daten werden entweder in das System gestreamt oder wiederholt per Batch abgearbeitet
- [ ] Das Ergebnis der Berechnungen im Big Data-System werden in der Datenbank gespeichert
- [X] Der Web Server liefert diese Ergebnisse aus
- [X] Lizenz Quellcode (Apache)
- [X] Quellcode der Anwendung, der zum Start und Betrieb der Gesamtanwendung notwendig ist
- [ ] Dokumentation der Anwendung
- [ ] Screencast => Erstellt FG
- [ ] Dokumentation Architektur
- [ ] Code kommentiert und formatiert und nachvollziehbar
- [X] Grundsätzliche Idee der Anwendung erklären
- [ ] Repo aufräumen
- [ ] Abgabe des Git Repository


## Big Data Architecture :house:<a name="architecture"></a>

### Overview Architektur:
* HDFS speichert Daten zur Börse (Frankfurt Stock Exchange) und Covid-19 (Ansteckungen und Verstorbene pro Tag)
* Die Daten werden durch einen Standalone Python-Import-Pod zyklisch aktualisiert
* Über das Kafka Cluster wird vom Python-Import-Pod eine Benachrichtigung an Apache Spark über neue Daten gesendet
* Apache Spark greift daraufhin auf die Daten im HDFS Cluster zu
* Apache Spark verarbeitet die Daten und sendet diese an den Datenbank-Server
* Der Datenbank-Server speichert die Daten in einer MySQL-DB
* Der Web-Server ruft über eine Schnittstelle zur MySQL-DB die Daten ab
* Das Web-Frontend zeigt dem Nutzer die Daten in einer grafischen Darstellung
* Der Nutzer kann verschieden Parameter ändern, die zu einem entsprechenden Abruf bei der MySQL-DB führt
* Bevor ein Abruf der Daten bei der MySQL-DB erfolgt, wird geprüft, ob das SQL-Statement bereits in Memchached verfügbar ist
* Für weitere Details zu den Komponenten siehe unten

![](images/architecture.png)

### Python-Import-Pod:
* Importiert stündlich die neuesten Daten aus folgenden Quellen:
  * Frankfurt Stock Exchange: https://www.quandl.com/data/FSE-Frankfurt-Stock-Exchange
  * Infektionsdaten COVID-19: https://opendata.ecdc.europa.eu/covid19/casedistribution/json/
* Daten werden im CSV-Format auf dem HDFS abgelegt
* Nach Import wird über Kafka eine Benachrichtigung an den Spark Driver Pod gesendet. *(Anmerkung: Integration von Apache Hadoop als Kafka Producer zu aufwendig)*
* PyWebHDFS wird zur Interaktion mit dem HDFS verwendet

### Data Lake (HDFS):
* Daten aus Börse (link siehe Python-Import-Pod) und Daten aus Covid (link siehe Python-Import-Pod) werden als CSV gespeichert
* Daten Covid werden alle 1h aktualisiert. *(Anmerkung: Datenquelle aktualisiert sich jedoch nur täglich)*
* Daten Börse werden alle 1h aktualisiert.
* Apache Knox wird zur Interaktion mit HDFS verwendet.

### Big Data Messaging (Kafka Cluster):
* Messaging System zwischen Apache Spark und HDFS
* Kafka Cluster wird über Helm hochgefahren (siehe: https://strimzi.io/charts/index.yaml)
* Kafka Producer: Python-Import-Pod
* Kafka Consumer: Spark-Driver-Pod
* Topic: spark_notification
* Replikation: 1 *(Anmerkung: Es werden grds. 3 bis 5 broker in einem Kafka Cluster für eine hohe Verfügbarkeit und einen schnellen Durchlauf empfohlen)*
* Mögliche Erweiterung: Web Servcer Producer Nutzungsdaten sendet Nutzungsdaten der Weboberfläche an Data Lake Consumer.

### Big Data&Science Processing (Apache Spark):
* Dient dem Data Processing der Daten aus HDFS
* Wenn Apache Spark Consumer msg erhält dass neue Daten in HDFS sind dann greift Apache Spark auf die Daten in HDFS zu
* Apache Spark verarbeitet die Daten und sendet an die Datenbank
* Bevor die Daten an die MySQL-DB gesendet werden, werden die Daten vorbereitet:
  * Unnötige Daten werden aussortiert
  * Aktienkurse werden zu DAX aufsummiert
  * Absolute und relative Veränderungen zwischen den Tagen werden kalkuliert

### Datenbank (MySQL-Datenbank): 
* Rationale Datenbank speichert von Apache Kafka aufbereitete Daten.
* Tabelle sieht so aus: ....

### Web Server (Node.js):
* Zeigt Grafik zu den Daten Covid und Börse an (X-Achse Zeit und Y-Achse Ansteckungen / Kurs)
* Nutzer können Parameter einstellen, die zu einer SQL-Abfrage bei der MySQL-Datenbank führen
* In Memcached werden die bisherigen SQL-Abfragen gespeichert (siehe dazu Memcached)
* Web Server prüft die Verfügbarkeit im Cache bevor er eine SQL-Abfrage bei der MySQL-Dantenbank durchführt (siehe dazu Memcached)

### Cache-Server (Memcached):
* Aus den SQL-Abfragen des Web Servers an den MySQL-Server wird ein Key erstellt und in Memchached abgelegt
* Wenn ein Key nicht vorhanden ist wird die SQL-Abfrage an den MySQL-Server gesendet und in Memcached als Key abgelegt
* In Memcached wird neben dem Key das jeweilige Ergebnis der Abfrage gespeichert
* In Memcached werden Daten maximal X Minuten gespeichert

### Load Balancer (Ingress):
* Ingress => ML ergänzt

## Funktionsweise der Benutzeroberfläche <a name="oberfläche"></a>
Die Benutzeroberfläche entspricht dem Endpunkt der Architektur, über welchen der Enduser in der Regel Daten der Anwendung abfragt. Hierzu kann nach dem Start der unterschiedlichen Architekturkomponenten (min. nach dem Start des Webservers (webapp.js)) die Adresse localhost:8080 über einen beliebigen Internetbrowser aufgerufen werden.

### Anwendungslogik der Oberfläche 
Die Anwendungslogik validiert und Verarbeitet die jeweiligen Nutzeranfragen und aktualisert die auf der Oberfläche angezeigten Grafen. Bei den Parametern der Nutzeranfrage werden folgende unterschieden:

#### Auswahl eines Datumbereichs
Es muss in jedem Fall ein Datumsbereich ausgwählt werden. Je nach größe des Bereichs wird der Graf auf Monate, Kalenderwochen oder Tage skaliert.
* Monate: Datumsrange größer 4 Monate
* Wochen: Datumsrange zwischen 4 Wochen und 4 Monaten
* Tage: Datumsrange kleiner 28 Tage (4 Wochen) 

#### Auswahl der Betrachtungsländer 
Unter Verwendung einer Checkbox-Liste können die Länder ausgewählt werden, deren Coronadaten für den Vergleich herangezogen werden sollen. Das Land "Deutschland" ist standardmäßig ausgewählt

#### Relative Veränderung zum Vortag
Bei den Coronadaten können wahlweise entweder die tatsächliche Tagesveränderung (Neuerkrankungen bzw. Todesfälle) oder die relative Veränderung zum Vortag angezeigt werden.

#### Art der Coronadaten
Bei den Coronadaten können entweder die Neuerkrankungen oder die Todesfälle in Relation zum Aktienkurs angezeigt werden. 


### Prerequisites 

TODO: What things you need to install the software and how to install them

```
Docker
minikube
helm
python3 spark pyspark 
```


## Starting minikube <a name="minikube"></a>

Start minicube with Hyper V driver (make sure Hyper V is enabled)
```
#on Win 10
minikube start --driver=hyperv --memory 5120 --cpus 4

#on Mac
minikube start --vm-driver=hyperkit --memory 5120 --cpus 4

#on Ubuntu
minikube start --driver=none
```
Pointing Docker daemon to minicube regestry
```
#on Win 10
minikube docker-env
minikube -p minikube docker-env | Invoke-Expression

#on Mac
eval $(minikube docker-env)
```
Enable Load Balancer (Ingress)
```
minikube addons enable ingress
```


## Deploy HDFS on K8S: <a name="k8s"></a>
### Deploying HDFS 

Add helm stable repo and install chart for stable hadoop cluster
```
helm repo add stable https://kubernetes-charts.storage.googleapis.com/
# if using helm for the first time run "helm init"
helm install --namespace=default --set hdfs.dataNode.replicas=2 --set yarn.nodeManager.replicas=1 --set hdfs.webhdfs.enabled=true hadoop stable/hadoop
```

Adjust user rights on root folder to be able to acces filesystem via WEBHDFS
```
kubectl exec -ti hadoop-hadoop-yarn-rm-0 bash
hdfs dfs -chmod  777 /
exit
```

### Install Apache Knox - REST API and Application Gateway

using helm chart pfisterer/apache-knox-helm
```
helm repo add pfisterer-knox https://pfisterer.github.io/apache-knox-helm/
helm install --set "knox.hadoop.nameNodeUrl=hdfs://hadoop-hadoop-hdfs-nn:9000/" --set "knox.hadoop.resourceManagerUrl=http://hadoop-hadoop-yarn-rm:8088/ws" --set "knox.hadoop.webHdfsUrl=http://hadoop-hadoop-hdfs-nn:50070/webhdfs/" --set "knox.hadoop.hdfsUIUrl=http://hadoop-hadoop-hdfs-nn:50070" --set "knox.hadoop.yarnUIUrl=http://hadoop-hadoop-yarn-ui:8088" --set "knox.servicetype=LoadBalancer" knox pfisterer-knox/apache-knox-helm
```


## Deploy the periodic import pod on K8S:<a name="deplox"></a>
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


## Deploy Kafka cluster on K8S: <a name="kafkacluser"></a>
### Install Strimzi operator
Install strimzi operator via Helm
```
helm repo add strimzi http://strimzi.io/charts/
helm install kafka-operator strimzi/strimzi-kafka-operator
```
### Apply Kafka Cluster Deployment
Navigate shell into 'kafka-config' folder
```
kubectl apply -f kafka-cluster-def.yaml
```


## Deploy Spark on K8S <a name="sparkk8s"></a>

The pyspark app is put into hdfs /app/ 

### Spark Operator in separate workspace
Create a namespace with the name ‘spark-operator’
```
#navigate to the folder "pyspark-app"
kubectl create -f namespaces-spark.yml

#create a service account with the name ‘spark’
kubectl create serviceaccount spark --namespace=default

#create RBAC role for svc spar
kubectl create clusterrolebinding spark-operator-role --clusterrole=cluster-admin --serviceaccount=default:spark --namespace=default

#install helm repo
helm repo add incubator http://storage.googleapis.com/kubernetes-charts-incubator

helm install spark incubator/sparkoperator --namespace spark-operator --set sparkJobNamespace=default
```


## Deploy the database <a name="deploydb"></a>
### Create necessary DB-Pod

Build a connection to the "my-database" folder
```
#navigate to the folder my-database
cd my-database
```

Create a POD and deploy it to minikube
```
kubectl apply -f config-app.yml
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
### Create necessary Memcached-Pod

Create a POD and deploy it to minikube
```
kubectl apply -f my-memcache-deployment.yml
```


## Start User-Interface <a name="deployinterface"></a>

Check if service is running on minikube
```
minikube dashboard
```

Navigate to /app/
```
cd ../app/
```

Build Interface-Dockerfile and run interface-deployment
```
docker build -t interface .
```

Run interface-Deployment
```
kubectl apply -f interface-deployment.yml
```

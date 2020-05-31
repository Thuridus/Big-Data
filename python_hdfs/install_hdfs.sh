#!/bin/bash
# Add helm repo hadoop
helm repo add stable https://kubernetes-charts.storage.googleapis.com/
# Install chart for hdfs with datanodes 2 replicas and 1 nodemanager replicas
helm install --namespace=default --set hdfs.dataNode.replicas=2 --set yarn.nodeManager.replicas=1 --set hdfs.webhdfs.enabled=true hadoop stable/hadoop
# Add helm repo pfisterer knox
helm repo add pfisterer-knox https://pfisterer.github.io/apache-knox-helm/
# Install chart for apache knox
helm install --set "knox.hadoop.nameNodeUrl=hdfs://hadoop-hadoop-hdfs-nn:9000/" --set "knox.hadoop.resourceManagerUrl=http://hadoop-hadoop-yarn-rm:8088/ws" --set "knox.hadoop.webHdfsUrl=http://hadoop-hadoop-hdfs-nn:50070/webhdfs/" --set "knox.hadoop.hdfsUIUrl=http://hadoop-hadoop-hdfs-nn:50070" --set "knox.hadoop.yarnUIUrl=http://hadoop-hadoop-yarn-ui:8088" --set "knox.servicetype=LoadBalancer" knox pfisterer-knox/apache-knox-helm
# Build Dockerfile for periodic import pod
docker build -t python_download .
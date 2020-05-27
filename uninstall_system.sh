#!/bin/bash
# This scipt uninstalls previously installed components of the BIG-Data environment
# Uninstall the Spark component
echo 'Installing Spark component'
cd ./pyspark_app
sh ./install_pyspark.sh
cd ..
# Uninstall the Hadoop Filesystem components
echo 'Uninstalling HDFS Component'
cd ./python_hdfs
sh ./uninstall_hdfs.sh
cd ..
# Uninstall MYSQL DB components
echo 'Uninstalling MYSQL DB Component'
cd ./my-database
sh ./uninstall_db.sh
cd ..
# Uninstall the Kafka components
echo 'Installing Kafka Component'
cd ./kafka-config
sh ./uninstall_kafka.sh
cd ..
kubectl get all
echo 'System successfully uninstalled'

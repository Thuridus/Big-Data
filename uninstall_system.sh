#!/bin/bash
# This scipt uninstalls previously installed components of the BIG-Data environment
# Uninstall the Web Component
echo 'Uninstalling Web component'
cd ./app
sh ./uninstall_app.sh || true
cd ..
# Uninstall the Spark component
echo 'Uninstalling Spark component'
cd ./pyspark-app
sh ./uninstall_pyspark.sh || true
cd ..
# Uninstall the Hadoop Filesystem components
echo 'Uninstalling HDFS Component'
cd ./python_hdfs
sh ./uninstall_hdfs.sh || true
cd ..
# Uninstall MYSQL DB components
echo 'Uninstalling MYSQL DB Component'
cd ./my-database
sh ./uninstall_db.sh || true
cd ..
# Uninstall the Kafka components
echo 'Installing Kafka Component'
cd ./kafka-config
sh ./uninstall_kafka.sh || true
cd ..
echo 'System successfully uninstalled'
#See it all disappear
watch kubectl get all

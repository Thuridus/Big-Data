#!/bin/bash
# This scipt installs the necessary environment to run the Big-Data application
# Install MYSQL DB components
echo 'Installing MYSQL DB Component'
cd ./my-database
sh ./install_db.sh
cd ..
# Install the Kafka components
echo 'Installing Kafka Component'
cd ./kafka-config
sh ./install_kafka.sh
cd ..
# Install the Hadoop Filesystem components
echo 'Installing HDFS Component'
cd ./python_hdfs
sh ./install_hdfs.sh
cd ..
# Install the Spark component
echo 'Installing Spark component'
cd ./pyspark_app
sh ./install_pyspark.sh
cd ..
echo 'System install finished'
# See it all rising
watch kubectl get all
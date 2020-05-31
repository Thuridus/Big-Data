# Apply custom Kafka Config
kubectl apply -f ./kafka-config/kafka-cluster-def.yml
# Wait for hdfs to be ready
echo 'Waiting for hdfs pods to start up'
kubectl wait --for condition=ready pod/hadoop-hadoop-yarn-nm-0 --timeout=60s
kubectl wait --for condition=ready pod/hadoop-hadoop-yarn-rm-0 --timeout=60s
kubectl wait --for condition=ready pod/hadoop-hadoop-hdfs-nn-0 --timeout=60s
kubectl wait --for condition=ready pod/hadoop-hadoop-hdfs-dn-0 --timeout=60s
kubectl wait --for condition=ready pod/hadoop-hadoop-hdfs-dn-1 --timeout=60s
# Change access rights for base directory in HDFS
kubectl exec -ti hadoop-hadoop-yarn-rm-0 -- hdfs dfs -chmod  777 /
# Apply deployment for import pod
kubectl apply -f ./python_hdfs/python_import_deployment.yml
# run deployment for Spark
kubectl apply -f ./pyspark-app/spark_control_deployment.yml
# run deployment for app interface
kubectl apply -f ./app/interface-deployment.yml
echo "Load Balancer avialble on"
kubectl cluster-info
echo 'Installing helm repo'
helm repo add stable https://kubernetes-charts.storage.googleapis.com/
echo 'starting hadoop cluster'
helm install --namespace=default --set hdfs.dataNode.replicas=2 --set yarn.nodeManager.replicas=1 --set hdfs.webhdfs.enabled=true hadoop stable/hadoop
echo 'starting apache knox'
helm repo add pfisterer-knox https://pfisterer.github.io/apache-knox-helm/
helm install --set "knox.hadoop.nameNodeUrl=hdfs://hadoop-hadoop-hdfs-nn:9000/" --set "knox.hadoop.resourceManagerUrl=http://hadoop-hadoop-yarn-rm:8088/ws" --set "knox.hadoop.webHdfsUrl=http://hadoop-hadoop-hdfs-nn:50070/webhdfs/" --set "knox.hadoop.hdfsUIUrl=http://hadoop-hadoop-hdfs-nn:50070" --set "knox.hadoop.yarnUIUrl=http://hadoop-hadoop-yarn-ui:8088" --set "knox.servicetype=LoadBalancer" knox pfisterer-knox/apache-knox-helm


# Writing address of WEBHDFS API in Environment Variable		
#echo 'getting address of knox webhdfs api'
#$env:KNOX_ADDRESS=minikube service knox-apache-knox-helm-svc --url
#[System.Environment]::SetEnvironmentVariable('KNOX_ADDRESS',$env:KNOX_ADDRESS,[System.EnvironmentVariableTarget]::Machine)
#echo 'Adress is available on :$env:KNOX_ADDRESS'

echo 'Changing access rights for filesystem to 777'
kubectl exec -ti hadoop-hadoop-yarn-rm-0 bash
hdfs dfs -chmod  777 /
echo 'finished webhdfs and hadoop cluster are running'
exit
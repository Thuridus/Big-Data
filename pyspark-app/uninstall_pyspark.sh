#Delete  deployment
kubectl delete -f spark_control_deployment.yml
#Delete  clusterrolebinding for subscriber pod
kubectl delete clusterrolebinding default-edit-role
#Uninstall incubator to K8s
helm uninstall spark
#Delete clusterrolebinding for spark user
kubectl delete clusterrolebinding spark-operator-role
#Delete serviceaccount for spark operator
kubectl delete serviceaccount spark
#Delete namespace for spark operator
kubectl delete namespace spark-operator
#Delete  docker image for driver
docker image rm spark_control

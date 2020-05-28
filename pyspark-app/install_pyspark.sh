#Create namespace for spark operator
kubectl create namespace spark-operator
#Create serviceaccount for spark operator
kubectl create serviceaccount spark --namespace=default
#Create clusterrolebinding for spark user
kubectl create clusterrolebinding spark-operator-role --clusterrole=cluster-admin --serviceaccount=default:spark --namespace=default
#Add incubator helm repo
helm repo add incubator http://storage.googleapis.com/kubernetes-charts-incubator
#Install incubator to K8s
helm install spark incubator/sparkoperator --namespace spark-operator --set sparkJobNamespace=default
# Create clusterrolebinding for subscriber pod
kubectl create clusterrolebinding default-edit-role --clusterrole=cluster-admin --serviceaccount=default:default --namespace=default
# Create docker image for driver
docker build -t spark_control .
# run deployment
kubectl apply -f spark_control_deployment.yml

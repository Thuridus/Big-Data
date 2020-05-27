minikube start --vm-driver=hyperkit --memory 5120 --cpus 4
eval $(minikube docker-env)
minikube addons enable ingress
cd ../my-database
kubectl apply -f config-app.yml
kubectl apply -f my-memcache-deployment.yml
kubectl apply -f my-mysql-deployment.yml
echo "waiting for my-sql Pod to get ready"
while [[ $(kubectl get pods -l app=my-mysql -o 'jsonpath={..status.conditions[?(@.type=="Ready")].status}') != "True" ]]; do sleep 1; done
cd ../app 
docker build -t interface .
kubectl apply -f interface-deployment.yml
echo "Waiting for Load Balancer to get ready"
while [$(kubectl get ingress -o 'jsonpath={..status.loadBalancer.ingress[0].ip}') = ""]; do sleep 1; done
open http://$(kubectl get ingress -o 'jsonpath={..status.loadBalancer.ingress[0].ip}')
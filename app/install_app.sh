cd ../my-database
kubectl apply -f my-memcache-deployment.yml
cd ../app 
docker build -t interface .
kubectl apply -f interface-deployment.yml
echo "Waiting for Load Balancer to get ready"
sleep 20s
#while [$(kubectl get ingress -o 'jsonpath={..status.loadBalancer.ingress[0].ip}') = ""]; do sleep 1; done
open http://$(kubectl get ingress -o 'jsonpath={..status.loadBalancer.ingress[0].ip}')

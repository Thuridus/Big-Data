# Delete UI Deployment
kubectl delete -f interface-deployment.yml
cd ../my-database
# Delete MemcacheD Deployment
kubectl delete -f my-memcache-deployment.yml

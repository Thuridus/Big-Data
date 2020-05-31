cd ../my-database
kubectl apply -f my-memcache-deployment.yml
cd ../app 
docker build -t interface .

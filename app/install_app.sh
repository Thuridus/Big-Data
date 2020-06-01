cd ../my-database
# Apply MemcacheD Deployment
kubectl apply -f my-memcache-deployment.yml
cd ../app
# Build container image for UI
docker build -t interface .
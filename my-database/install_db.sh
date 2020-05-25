#!/bin/bash
# Apply custom config for mysql db
kubectl apply -f config-app.yml
# Install mysql deloyment
kubectl apply -f my-mysql-deployment.yml

#!/bin/bash
# Add strimzi repo
helm repo add strimzi http://strimzi.io/charts/
# Install stimzi operator
helm install kafka-operator strimzi/strimzi-kafka-operator
# quick hack because we cant you kubectl wait on random named pods
echo 'Sleeping 1m to wait for kafka cluster to start up'
sleep 1m
# Apply custom Kafka Config
kubectl apply -f kafka-cluster-def.yml

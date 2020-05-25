#!/bin/bash
# Delete custom kafka cluster
kubectl delete -f kafka-cluster-def.yml
# Uninstall strimzi operator
helm uninstall kafka-operator

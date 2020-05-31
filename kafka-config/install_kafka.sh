#!/bin/bash
# Add strimzi repo
helm repo add strimzi http://strimzi.io/charts/
# Install stimzi operator
helm install kafka-operator strimzi/strimzi-kafka-operator
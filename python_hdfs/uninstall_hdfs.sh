#!/bin/bash
# uninstall knox
helm uninstall knox
# uninstall hadoop
helm uninstall hadoop
# remove download pod
kubectl delete pod python-download-pod

#!/bin/bash

source /usr/local/bin/deployment-helpers-v1.sh

authenticateToAKS

# the dhos-url-api runs on its own namespace -
# the plan is to have microservices run on their own namespaces in a pure multi-tenanted deployment
DHOS_URL_API_NAMESPACE=dhos-url-api
kubectl get ns ${DHOS_URL_API_NAMESPACE} /dev/null 2>&1

# create our namespace if it doesn't exist
if [[ "$?" -ne "0" ]]; then
  kubectl create ns ${DHOS_URL_API_NAMESPACE}
fi

## check helm version - we need helm 3
helm version --client --short | grep "v3." > /dev/null 2>&1

if [[ "$?" -ne "0" ]]; then
  echo "error: incorrect helm version helm3."
  echo "error: need helm3 (ensure circleci-build-image has helm binaries on it)"
  exit 1
fi

echo Installing or upgrading helm chart

helm upgrade --install --namespace ${DHOS_URL_API_NAMESPACE} dhos-url-api $(dirname ${BASH_SOURCE})/helm-chart/dhos-url-api \
     -f $(dirname ${BASH_SOURCE})/helm-chart/dhos-url-api/values.yaml \
     -f $(dirname ${BASH_SOURCE})/helm-chart/dhos-url-api/values-dev.yaml \
     -f <(sops --decrypt $(dirname ${BASH_SOURCE})/helm-chart/dhos-url-api/values-dev-secrets-sops.yaml) \
     --recreate-pods

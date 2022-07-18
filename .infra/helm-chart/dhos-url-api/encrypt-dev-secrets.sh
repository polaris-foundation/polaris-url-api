#!/bin/bash

echo Encrypting dev secrets file
sops --encrypt --azure-kv https://uk-dev-keyvault.vault.azure.net/keys/dhos-url-api-sops/6943708a39ab4874b4e8ee4b64ba419a values-dev-secrets.yaml > values-dev-secrets-sops.yaml
sops -r -i --add-pgp 8872B8F99E83960708A51F9BA6B64CBF0636EFDA values-dev-secrets-sops.yaml

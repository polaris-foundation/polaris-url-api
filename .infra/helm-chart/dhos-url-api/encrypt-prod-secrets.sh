#!/bin/bash

## ensure we have the necessary whitelist set to access the keyvault in azure (https://portal.azure.com/#@sensynehealth.com/resource/subscriptions/63ad258a-0f7e-4336-8e52-52f29e5e4dd2/resourceGroups/ukprod/providers/Microsoft.KeyVault/vaults/uk-prod-keyvault/networking)
echo Encrypting prod secrets file
sops --encrypt --azure-kv https://uk-prod-keyvault.vault.azure.net/keys/dhos-url-api-sops/8105fc9ac9cc4b3593f1b44843857f84 values-az-uk-prod006-secrets.yaml > values-az-uk-prod006-secrets-sops.yaml
sops -r -i --add-pgp 8872B8F99E83960708A51F9BA6B64CBF0636EFDA values-az-uk-prod006-secrets-sops.yaml

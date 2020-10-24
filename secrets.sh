#!/bin/bash

eval $(op signin my)

# Terraform Cloud/Enterprise Creds
export TFC_URL="https://app.terraform.io"
export TFC_TOKEN=$(op get item "Terraform Cloud" | jq -r '.details.sections[1].fields[0].v')

# SSL config
export SSL_VERIFY="true"
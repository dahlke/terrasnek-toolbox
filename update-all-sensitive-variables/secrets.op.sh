#!/bin/bash

eval $(op signin hashicorp)

export TFC_URL="https://app.terraform.io"
export TFC_TOKEN=$(op get item "Terraform Cloud" | jq -r '.details.sections[1].fields[0].v')
export TFC_ORG="hc-se-tfe-demo-neil"

export SSL_VERIFY="true"


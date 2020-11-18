#!/bin/bash

eval $(op signin hashicorp)

export GCS_BUCKET="hc-neil"
export GCLOUD_KEYFILE_JSON=$(op get item "Google" | jq -r '.details.sections[1].fields[0].v' | jq -r .)
export GOOGLE_APPLICATION_CREDENTIALS="/Users/neil/.gcp/hashicorp-noproject.json"

export TFC_URL="https://app.terraform.io"
export TFC_ORG="hc-se-tfe-demo-neil"
export TFC_TOKEN=$(op get item "Terraform Cloud" | jq -r '.details.sections[1].fields[0].v')

export SSL_VERIFY="true"

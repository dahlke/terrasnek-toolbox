#!/bin/bash

eval $(op signin my)

export TFC_URL="https://app.terraform.io"
export TFC_TOKEN=$(op get item "Terraform Cloud" | jq -r '.details.sections[1].fields[0].v')

export SSL_VERIFY="true"

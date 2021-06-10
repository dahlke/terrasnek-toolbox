## Workaround for bad ingress modules

```bash
curl \
  --header "Authorization: Bearer $TOKEN" \
  --header "Content-Type: application/vnd.api+json" \
  --request DELETE \
  https://app.terraform.io/api/v2/organizations/terrasnek-unittest/registry-modules/private/terrasnek-unittest/terrasnek-unittest-module/tfe
```
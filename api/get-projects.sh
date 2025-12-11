#!/bin/bash

API="https://192.168.1.227/api/projects"
OUT="projects.json"

curl --insecure -X GET "$API" \
  -H "Authorization: Bearer $(jq -r .bearerToken token.json)" \
  -H "Accept: application/vnd.blackducksoftware.project-detail-7+json"\
  | jq '.items | map({proj_name: .name, proj_key: (._meta.href | sub(".*/projects/"; ""))})' > "$OUT"

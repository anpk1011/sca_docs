#!/bin/bash

PROJECT_ID=$1
API="https://192.168.1.227:443/api/projects/e31c43d8-0fd8-411f-825e-8ae020531ab2/versions"
OUT="versions.json"

curl --insecure -X GET "$API"  \
  -H "Authorization: Bearer $(jq -r .bearerToken token.json)"  \
  -H "Accept: application/vnd.blackducksoftware.project-detail-5+json"  \
  | jq '.items | map({version_name: .versionName, version_key: (._meta.href | sub(".*/versions/"; ""))})' > "$OUT"



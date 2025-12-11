#!/bin/bash

PROJECT_ID=$1
API="https://192.168.1.227/api/projects/$PROJECT_ID/versions"
OUT="projects.json"

curl --insecure -X GET "$API" \
  -H "Authorization: Bearer $(jq -r .bearerToken token.json)" \
  -H "Accept: application/vnd.blackducksoftware.project-detail-7+json"\
  | jq

#!/bin/bash

API="https://192.168.1.227:443/api/tokens/authenticate"
OUT="token.json"

curl --insecure -X POST "$API" \
    -H "Accept: application/vnd.blackducksoftware.user-4+json" \
    -H "Authorization: token NTYzMzM2OTItMDNkZC00OWVmLTgwMTYtZGQ2NWIzYzA3Y2JjOjBlODJlNjgzLWE4MjMtNDM4Yy05YTk4LTk2YTdkN2YyYzQ1ZA==" \
    | jq > "$OUT"

cat "$OUT" | jq
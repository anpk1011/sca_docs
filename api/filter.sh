#!/bin/bash

ALL="projects.json"
OUT="project_filter.json"
 
project_filter=( "webgoat" "crm-test" )
 
cond=""
first=1
for p in "${project_filter[@]}"; do
  if [ $first -eq 1 ]; then
    cond='.proj_name == "'"$p"'"'
    first=0
  else
    cond="$cond or .proj_name == \"$p\""
  fi
done
 
jq "[ .[] | select($cond) ]" "$ALL" > "$OUT"

cat "$OUT" | jq

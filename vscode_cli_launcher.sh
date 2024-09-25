#!/bin/bash
# allow node to fetch extension
export NODE_EXTRA_CA_CERTS=/etc/ssl/certs/ca-bundle.crt
# ensure directories exist
mkdir -p ~/.vscode/data ~/.vscode/server-data ~/.vscode/extensions
# get IP address
IPADDR=$(ip a | grep -v ' lo' | grep -v 'podman' | grep -oE 'inet [0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}' | sed 's/inet //')
# start server
code serve-web --port 8000 --host 127.0.0.1 \
  --user-data-dir ~/.vscode/data \
  --extensions-dir ~/.vscode/extensions \
  --server-data-dir ~/.vscode/server-data \
  --accept-server-license-terms $@ | sed "s|http://127.0.0.1:8000|https://${IPADDR}|g"

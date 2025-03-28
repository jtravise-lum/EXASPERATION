#!/bin/sh
set -e

# Get the domain and token from Caddy
DOMAIN=$1
TOKEN=$2

# Set API key from environment
API_KEY=$NS1_API_KEY

# Add TXT record for ACME challenge
curl -X PUT -H "X-NSONE-Key: $API_KEY"   -d '{"zone":"$DOMAIN", "domain":"_acme-challenge.$DOMAIN", "type":"TXT", "answers":[{"answer":["$TOKEN"]}]}'   https://api.nsone.net/v1/zones/$DOMAIN/records

# Wait for DNS propagation
sleep 60

# Return success
exit 0

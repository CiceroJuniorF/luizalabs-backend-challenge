#!/bin/bash

URL='http://127.0.0.1:8000/api/customer/create'
TOKEN='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJsdWl6YWxhYnMiLCJleHAiOjE3NDA2NzE0NTl9.SzscjqV7ilrkVtahZBw0Z9bsz60vkR5gANenHY3X-ws'

for i in {1..20}; do
  EMAIL="mail$i@mail.com"
  curl -X 'POST' "$URL" \
    -H 'accept: application/json' \
    -H "Authorization: Bearer $TOKEN" \
    -H 'Content-Type: application/json' \
    -d "{\"name\": \"Name SecondName\", \"email\": \"$EMAIL\"}"
  echo "Inserted: $EMAIL"
done

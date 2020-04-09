#!/bin/bash

model=$1
image=$2

(echo -n '{"image": "'; base64 $image; echo '"}') | curl -k -H "Content-Type: application/json" -d @- -X POST https://pcml.southcentralus.cloudapp.azure.com:8080/inference/$model

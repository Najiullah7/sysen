# test_requests.py
# POST request with JSON data
# Pairs with Docs requests
# Tim Fraser

# Sends a POST request to httpbin.org/post with JSON payload.
# Demonstrates how to set Content-Type and send JSON using the requests library.

# 0. Setup #################################

## 0.1 Load Packages ############################

import requests  # for HTTP requests

## 0.2 POST with JSON ###############################

url = "https://httpbin.org/post"
payload = {"name": "test"}

# requests.post(..., json=...) sets Content-Type: application/json
# and serializes the dict to JSON automatically
response = requests.post(url, json=payload)

print(response.status_code)
print(response.json())

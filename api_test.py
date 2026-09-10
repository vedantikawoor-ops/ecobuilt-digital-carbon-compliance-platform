import requests


url = "http://127.0.0.1:5000/api/analyze"

data = {
    "url": "https://example.com"
}


print("========================================")
print("       EcoBuilt API Test")
print("========================================")

print()
print("Sending website for analysis...")

response = requests.post(
    url,
    json=data
)

print()
print("HTTP Status:", response.status_code)

print()
print("----------- API RESPONSE -----------")

print(response.json())

print("------------------------------------")
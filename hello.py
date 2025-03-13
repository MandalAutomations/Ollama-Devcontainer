import requests

url = "https://organic-invention-4ggjv69r9vpcjv7q-8080.app.github.dev/"

response = requests.get(url).text

print(response)


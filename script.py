import requests

response = requests.get('http://127.0.0.1:8001/accounts/client_accounts?id_client=1')

print(response)
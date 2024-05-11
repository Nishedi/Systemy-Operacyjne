import requests
from requests.structures import CaseInsensitiveDict

url = "https://api.geoapify.com/v1/routing?waypoints=51.141713%2C17.082726%7C51.122456%2C16.932308&mode=drive&apiKey=99025096b03142509578fa708444aa39"

headers = CaseInsensitiveDict()
headers["Accept"] = "application/json"

resp = requests.get(url, headers=headers)

print(resp.status_code)
print(resp.text)
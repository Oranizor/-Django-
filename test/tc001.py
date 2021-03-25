import requests,pprint

payload={
    'username':'byhy',
    'password':'bsbsbsbs'
}

response=requests.post('http://127.0.0.1:8000/signin/',
                       data=payload)

pprint.pprint(response.json())
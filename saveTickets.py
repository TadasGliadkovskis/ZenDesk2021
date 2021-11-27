import requests
from requests.models import HTTPBasicAuth
import json

#curl https://zcctadas.zendesk.com/api/v2/tickets.json -v -u tadas2410@gmail.com:tRNhWPBeGc2hm7u! get JSON TICKETS
response = requests.get('https://zcctadas.zendesk.com/api/v2/tickets.json',auth=HTTPBasicAuth('tadas2410@gmail.com','tRNhWPBeGc2hm7u!')).json()

with open ('data.json','w') as outfile:
      json.dump(response, outfile)
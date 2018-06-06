import requests
from bs4 import BeautifulSoup
import json

meaningURL = "https://ejje.weblio.jp/content/"
synonymURL = "https://od-api.oxforddictionaries.com:443/api/v1/entries/en/"
synonym_API_key = None
synonym_API_id = None

def meaning(name):
	req = requests.get(meaningURL+name)
	soup = BeautifulSoup(req.text, 'lxml')
	mean = soup.find_all("td", attrs={"class": "content-explanation"})
	return mean[0].string.split('、')

def synonym(name):
	url = synonymURL+name+"/synonyms"
	header = {"Accept": "application/json", "app_id": synonym_API_id, "app_key": synonym_API_key}
	response = json.loads(requests.get(url, headers=header).text)
	response = response["results"][0]["lexicalEntries"][0]["entries"][0]["senses"][0]["subsenses"][0]["synonyms"]
	print(response)
	res = []
	for idx, x in enumerate(response["synonyms"]):
		if idx >= 10:
			break
		res.append([x, meaning(x)])
	print(res)
	return res
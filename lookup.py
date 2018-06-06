import requests
from bs4 import BeautifulSoup
import json

meaningURL = "https://ejje.weblio.jp/content/"
synonymURL = "https://od-api.oxforddictionaries.com:443/api/v1/entries/en/"
synonym_API_key = None
synonym_API_id = None

def take_from_json(arg, cond, key=None):
	res = []
	if cond(arg, key):
		res.append(arg)
	if isinstance(arg, list):
		for item in arg:
			res += take_from_json(item, cond)
	elif isinstance(arg, dict):
		for k, v in arg.items():
			res += take_from_json(v, cond, k)
	return res

def has_synonym_list(arg, key):
	if isinstance(arg, list):
		return key == "synonyms"

def meaning(name):
	req = requests.get(meaningURL+name)
	soup = BeautifulSoup(req.text, 'lxml')
	mean = soup.find_all("td", attrs={"class": "content-explanation"})
	res = []
	for x in mean:
		if not isinstance(x.string, str):
			continue
		res += x.string.split('、')
	return res

def synonym(name):
	url = synonymURL+name+"/synonyms"
	header = {"Accept": "application/json", "app_id": synonym_API_id, "app_key": synonym_API_key}
	response = json.loads(requests.get(url, headers=header).text)
	response = take_from_json(response, has_synonym_list)
	res = []
	for x in response:
		cnt = 0
		for y in x:
			s = y["text"]
			if '-' in s or ' ' in s or s.lower() != s or s in res:
				continue
			res.append((s, meaning(s)))
			cnt += 1
			if cnt >= 5:
				break
		if len(res) >= 20:
			break
	return res
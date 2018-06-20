import requests
from bs4 import BeautifulSoup
import json
import re

meaningURL = "https://ejje.weblio.jp/content/"
sentenceURL = "https://ejje.weblio.jp/sentence/content/"
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


def is_phrase(arg, key):
    if isinstance(arg, dict):
        return key == "phrase"


def is_example(arg, key):
    if isinstance(arg, list):
        return key == "examples"


def remove_tags(s):
    res = ""
    for x in s:
        if not isinstance(x.string, str):
            continue
        res += x.string
    return res


def meaning(name, lim=1000):
    req = requests.get(meaningURL + name)
    soup = BeautifulSoup(req.text, 'lxml')
    mean = soup.find_all("p", attrs={"class": "lvlB"})
    res = []
    count_char = 0
    for x in mean:
        if len(x) == 0:
            continue
        if count_char > lim:
            break
        res.append(re.sub("AVOID_CROSSLINK", "", remove_tags(x)))
        count_char += len(res[-1])
    return res


def meaning_fast(name, lim=1000):
    req = requests.get(meaningURL + name)
    soup = BeautifulSoup(req.text, 'lxml')
    mean = soup.find_all("td", attrs={"class": "content-explanation"})
    res = []
    count_char = 0
    for list_ in mean:
        list_ = list_.text.split('、')
        for x in list_:
            if len(x) == 0:
                continue
            if count_char > lim:
                break
            res.append(x)
            count_char += len(x)
    return res


# def sentence(name, lim=1000):
#     url = sentenceURL
#     param = {
#         "from": "eng",
#         "dest": "ja",
#         "phrase": name,
#         "format": "json",
#         "pretty": "true"
#     }
#     response = json.loads(requests.get(url, params=param).text)
#     response = take_from_json(response, is_example)[0]
#     response = [(x["first"], re.sub(r"[　\s]", "", x["second"]))
#                 for x in response if len(x["first"]) <= lim]
#     response[min(len(response), 10)] = ("", "")
#     return response


def sentence(name, lim=1000):
    req = requests.get(sentenceURL + name)
    soup = BeautifulSoup(req.text, 'lxml')
    sen_en = soup.find_all("p", attrs={"class": "qotCE"})
    sen_ja = soup.find_all("p", attrs={"class": "qotCJ"})
    res = []
    for i in range(len(sen_en)):
        sen, sja = sen_en[i], sen_ja[i].text
        sen = re.sub(r"AVOID_CROSSLINK|例文帳に追加", "", remove_tags(sen))
        idx = sja.find("\xa0")
        if idx != -1:
            sja = sja[:idx]
        if 30 <= len(sen) and len(sen) <= lim:
            res.append((sen, sja))

    res = res[:min(20, len(res))]
    res.append(("", ""))
    return res


def synonym(name):
    url = synonymURL + name + "/synonyms"
    header = {
        "Accept": "application/json",
        "app_id": synonym_API_id,
        "app_key": synonym_API_key
    }
    response = requests.get(url, headers=header).text
    try:
        response = json.loads(response)
        response = take_from_json(response, has_synonym_list)
    except json.decoder.JSONDecodeError:
        return [' ']
    res = []
    for x in response:
        cnt = 0
        for y in x:
            s = y["text"]
            if len(s) == 0:
                continue
            if '-' in s or ' ' in s or s.lower() != s or s in res:
                continue
            res.append((s, ','.join(meaning_fast(s, 50))))
            cnt += 1
            print(len(res), end=', ', flush=True)
            if cnt >= 5 or len(res) >= 15:
                break
        if len(res) >= 15:
            break
    print()
    if len(res) == 0:
        res.append(" ")
    return res

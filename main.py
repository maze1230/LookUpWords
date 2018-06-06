import csv
import requests
from bs4 import BeautifulSoup
import json

import lookup as lu
import word
import helper as hl

if __name__ == '__main__':
	hl.synonym_api_init()
	print("Look up meanings of the words.")
	name = input("Input a word(-1 to end) -> ")

	while name != "-1":
		w = word.Word(name)
		try:
			w.mean = hl.choose_from_list(lu.meaning(name))
			w.synonym = hl.choose_from_list(lu.synonym(name))
			w.synonym = list(map(hl.first, w.synonym))
			print(w.synonym)
		except LookupError:
			print("There isn't this word.")
			pass
		name = input("Input a word(-1 to end) -> ")

import csv
import requests
from bs4 import BeautifulSoup
import json
import lookup as lu
import word

def input_lint(): # Split numbers into list
	return map(int, input().split(','))

def choose_from_list(list_, num=20): # num -> max number of the item to show
	ret = []
	print()
	for idx, item in enumerate(list_):
		if idx >= num:
			break
		print(str(idx) + ": " + str(item))
	print("Choose numbers(separate by ,) : ", end='')
	x = input_lint()
	for i in x:
		ret.append(list_[i])
	return ret

def synonym_api_init():
	try:
		with open("./.synonym_key", mode='x') as f:
			id_ = input("Synonym API ID(OxFordDictionary): ")
			key = input("Synonym API Key                 : ")
			f.writelines(id_+"\n")
			f.writelines(key+"\n")
	except FileExistsError:
		with open("./.synonym_key") as f:
			l = f.readlines()
			l = [x[:-1] for x in l]
			(id_, key) = (l[0], l[1])
	lu.synonym_API_id = id_
	lu.synonym_API_key = key

if __name__ == '__main__':
	synonym_api_init()
	print("Look up meanings of the words.")
	name = input("Input a word(-1 to end) -> ")

	while name != "-1":
		w = word.Word(name)
		w.mean = choose_from_list(lu.meaning(name))
		w.synonym = choose_from_list(lu.synonym(name))
		name = input("Input a word(-1 to end) -> ")

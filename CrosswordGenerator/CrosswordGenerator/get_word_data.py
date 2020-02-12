import json
import requests

file_path = "word_lists/crime_words.txt"

with open(file_path) as file:
	word_list = file.readlines()
word_list = [word.strip() for word in word_list]

# Fetch the frequency, normalized frequency and definition
# of each word on the word list from Oxford dictionary.
for word_id in word_list:

	# Actual app_id and app_key are required here.
	app_id = '2d2deef6'
	app_key = '1a1aef1091348f1ff3299344df3b1802'

	language = 'en-us'
	filters = 'definitions'

	url = 'https://od-api.oxforddictionaries.com:443/api/v2/thesaurus/' + language + '/' + word_id.lower() + '/' + filters

	url2 = 'https://od-api.oxforddictionaries.com:443/api/v2/stats/frequency/word/' + language + '/?corpus=nmc&trueCase=' + word_id

	r = requests.get(url, headers = {'app_id': app_id, 'app_key': app_key})

	r2 = requests.get(url2, headers = {'app_id': app_id, 'app_key': app_key})

	if r.status_code != 200 or r2.status_code != 200:
		continue

	definition = r.json()['results'][0]['lexicalEntries'][0]
	definition = definition['entries'][0]['senses'][0]['definitions'][0]

	freq = r2.json()['result']
	frequency = freq['frequency']
	norm_freq = freq['normalizedFrequency']

	print(word_id)
	print(frequency)
	print(norm_freq)
	print(definition)
	print()
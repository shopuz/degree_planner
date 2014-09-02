import sys
sys.path.append('/Users/surendrashrestha/Projects/pyhcsvlab')
import hcsvlab
from collections import Counter
from nltk.tokenize import word_tokenize
import nltk
from nltk import *

def get_word_frequency(client, search_term=''):
	""" Get the word frequency for a given word in all the item lists owned by the client """
	if not search_term:
		print "Enter a word to count its frequency:"
		search_term = raw_input()

	lists = client.get_item_lists()

	primary_text = ''
	# Iterate through only the personal item list
	for l in lists['own']:
		item_list = client.get_item_list(l['item_list_url'])
		for i in item_list:
			# get item object from the item_url
			item = client.get_item(i)
			primary_text = primary_text + item.get_primary_text()

	words = word_tokenize(primary_text)

	word_frequency = words.count(search_term)
	print word_frequency
	return word_frequency


def get_word_frequency_table(client, item_list_name=''):
	""" Get the word frequncy table for all the words in all the item lists owned by the client """
	primary_text = ''
	if not item_list_name:
		lists = client.get_item_lists()

		
		for l in lists['own']:
			item_list = client.get_item_list(l['item_list_url'])

			for i in item_list:
				# get item object from the item_url
				item = client.get_item(i)
				primary_text = primary_text + item.get_primary_text()
	else:
		item_list = client.get_item_list_by_name(item_list_name)
		for i in item_list:
				# get item object from the item_url
				item = client.get_item(i)
				primary_text = primary_text + item.get_primary_text()

	words = word_tokenize(primary_text)

	c = Counter(words)
	# Get only 100 most frequent words for the demo to be fast
	word_frequency_table = list(c.iteritems())[:100]

	return  word_frequency_table


def compare_word_frequency_decade(client):
	""" Get the frequency of two words in COOEE text """

	print 'Input Search term: '
	search_term = raw_input()
	print "Enter first decade initial year"
	first_decade = raw_input()
	print "Enter second decade initial year"
	second_decade = raw_input()

	item_group1 = client.search_metadata('created:%s TO %s AND collection_name:cooee' % (first_decade, str(int(first_decade)+10)))
	item_group2 = client.search_metadata('created:%s TO %s AND collection_name:cooee' % (second_decade, str(int(second_decade)+10)))
	item_groups = [item_group1, item_group2]
	
	word_frequency = []
	for group in item_groups:
		primary_text = ''
		for i in group:
			# get item object from the item_url
			item = client.get_item(i)
			primary_text = primary_text + item.get_primary_text()

		words = word_tokenize(primary_text)

		word_frequency.append(words.count(search_term))

	return  word_frequency
		


def get_collocation_frequency(client, item_list_name='', search_words=[]):
	""" Get the collocation frequency of all the words in the item lists owned by the client 
		If the item list and search words are specified, then only the collocation of those 
		words are computed
		For the sake of demo, this function only returns the unique words for rows and columns

		TODO:
		 return the collocation frequency : 
		 (word1, word2): frequency
	"""
	#print search_words
	#print item_list_name

	primary_text = ''
	
	if not item_list_name:
		lists = client.get_item_lists()

		
		for l in lists['own']:
			item_list = client.get_item_list(l['item_list_url'])

			for i in item_list:
				# get item object from the item_url
				item = client.get_item(i)
				primary_text = primary_text + item.get_primary_text()
	else:
		item_list = client.get_item_list_by_name(item_list_name)
		for i in item_list:
				# get item object from the item_url
				item = client.get_item(i)
				primary_text = primary_text + item.get_primary_text()

	words = word_tokenize(primary_text)
	unique_words = list(set(words))
	row_unique = []
	col_unique = []
	#Create your bigrams
	bgs = nltk.bigrams(words)

	#compute frequency distribution for all the bigrams in the text
	fdist = nltk.FreqDist(bgs)
	file = open("./static/data.tsv", "w")
	file.write("day\thour\tvalue\n")
	# Calculates for only  50 items in the frequency distribution
	if not search_words:
		limit = 50
	else:
		limit = None

	for k,v in fdist.items()[1:limit]:
	    if ((not search_words) or (k[0] in search_words and k[1] in search_words)):
		    if k[0] not in row_unique:
		    	row_unique.append(k[0])
		    if k[1] not in col_unique:
		    	col_unique.append(k[1])

		    
		    file.write(str(row_unique.index(k[0]) + 1) + '\t' + str(col_unique.index(k[1]) + 1) + '\t'  + str(v) + '\n')

	for search_word in search_words:
		if ((search_word not in row_unique) and (search_word not in col_unique)):
			row_unique.append(search_word)
			
		
			file.write(str(row_unique.index(search_word)) + '\t' + str(row_unique.index(search_word)) + '\t0')

	return [row_unique, col_unique]


def get_word_frequency_per_year(client, search_term='', pos='', item_list_name=''):
	""" Get the frequency of a given word per year inside the item list given by item_list_name """
	
	if not search_term:
		print "Enter a word to count its frequency:"
		search_term = raw_input()

	lists = client.get_item_lists()

	primary_text = ''
	temp_result = []
	result = {}
	items = []

	if item_list_name:
		item_list = client.get_item_list_by_name(item_list_name)
		items = item_list.get_all()
	else:
		item_lists = client.get_item_lists()

		for l in item_lists['own']:
			items.append(client.get_item_list(l['item_list_url']))


	for item in items:
		primary_text = item.get_primary_text()
		year = item.item_metadata['alveo:metadata']['dc:created']
		words = word_tokenize(primary_text)
		filtered_words = []
		
		if pos:
			for i in range(len(words)):
				if words[i] == search_term:
					filtered_words.append(words[i-1])
					filtered_words.append(words[i])
					filtered_words.append(words[i+1])

			tagged_words = nltk.pos_tag(filtered_words)
			f = nltk.FreqDist(tagged_words)

			word_pos = (search_term, pos)
		
		
			if word_pos in f.keys():
				
				print word_pos

				word_freq = f[word_pos]
			else:
				word_freq = words.count(search_term)
		else:
			word_freq = words.count(search_term)
	
		temp_result.append((year, word_freq))


	for i in temp_result:
		if i[0] in result.keys():
			result[i[0]] = result[i[0]] + i[1]
		else:
			result[i[0]] = i[1]


	return result




if __name__ == '__main__':
	client  = hcsvlab.Client()
	#print get_collocation_frequency(client, 'ace list')



import utils

import nltk
import requests
import docx2txt
from AsyncPQ import AsyncPriorityQueue

text = 'This is a table. We should table this offer. The table is hairy.'
text = nltk.word_tokenize(text)
result = nltk.pos_tag(text)

class Suggest(object):

	def __init__(self, arg): pass

class Synonym(object):

	def __init__(self, word, definition, example):
		self.word, self.definition, self.example = word, definition, example

class Parser(object):

	def __init__(self):

		self.asrwq = AsyncReadWriteQueue()
		self.SYNONYMS_API = 'http://api.pearson.com/v2/dictionaries/entries?synonyms='
		self.ADJ_TAG, self.VERB_TAG = 'JJ', 'VB'

	def get_pos(self, pos):
		pos_list = list(filter(lambda x: x[1] == pos, self.tagged_text))
		return [word[0] for word in pos_list]

	async def get_synonyms(self, word):
			
		raw_synonyms = requests.get((self.SYNONYMS_API + word)).json()
		results = raw_synonyms['results']

		headwords = [i['headword'] for i in results]
		definitions = [i['senses']['definition'] for i in results]
		examples = [i['senses']['examples']['text'] for i in results]
		synonyms = [Synonym(h,d,e) for h,d,e in zip(headwords, definitions, examples)]

		await asyncio.sleep(0)
		return synonyms

	def parse_text(self, file_path):

		raw_text = docx2txt.process(file_path)
		tokenized_test = nltk.word_tokenize(raw_text)
		result = nltk.pos_tag(tokenized_test)

		adjectives, verbs = self.get_pos(result, "JJ"), self.get_pos(result, "VB")
		all_adj_syn = [self.asrwq.read(self.get_synonyms, i) for i in adjectives]
		all_vrb_syn = [self.asrwq.read(self.get_synonyms, i) for i in verbs]
		all_synonyms = self.asrwq.processTasks()

		return utils.flattenList(all_synonyms)

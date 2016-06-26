from flask import Flask, request, jsonify
from collections import OrderedDict
import quails
import nltkfuns
import stanfuns
import nltk
from nltk.corpus import wordnet as wn

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cross_validation import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix

import os
import sys
import whoosh.index as index
from whoosh.qparser import QueryParser, MultifieldParser

toolkit_lists = {'nltk' : nltkfuns.nltkfuns, 'stanfuns' : stanfuns.stanfuns}
sets = quails.get_training_sets()

app = Flask(__name__)

@app.route('/quails/nlp')
def process():
	params = dict(request.args.items())

	text = params['text']
	input_steps = params['pipeline'].split(quails.DELIMITER)	

	if input_steps not in quails.valid_pipelines:
		return jsonify(failure="Invalid pipeline found.  Consult quails.py for options.")

	results = OrderedDict()
	results['text'] = text
	for step in input_steps:
		toolkit = params[step]
		if toolkit in toolkit_lists:
			toolkit_functions = toolkit_lists[toolkit]
			if step in toolkit_functions:
				# print step
				results[step]= toolkit_functions[step](results[quails.step_input[step]])
				#print results[step]
				
	del results['text']
	return jsonify(results)

@app.route("/quails/classification")
def classification():
	params = dict(request.args.items())
        text = params['text']
	classify = params['classify']
	
	if 'svm' in classify:
		#print "Classify new question using SVM."
		classes=classify_svm(text)
		#print classes		
		return jsonify(results=classes)

	return jsonify(success="Found me!")
	
# auxiliary function for classification service
def classify_svm(text):

	coarse_X = sets['coarse_training_qs']
	coarse_Y = sets['coarse_training_targets']
	fine_X = sets['fine_training_qs']
	fine_Y = sets['fine_training_targets']

	vectz = TfidfVectorizer(min_df=2, decode_error="ignore")
	coarse_X = vectz.fit_transform(coarse_X)	
	fine_X = vectz.fit_transform(fine_X)
	array_to_classify = vectz.transform([text]).toarray()

	
	# coarse
	svm_coarse = SVC(C=1000, gamma = 0.001, kernel='rbf')
	svm_coarse.fit(coarse_X, coarse_Y)
	# predict
	coarse_predict = svm_coarse.predict(array_to_classify)

	# fine
	svm_fine = SVC(C=1000, gamma = 0.001, kernel='rbf')
	svm_fine.fit(fine_X, fine_Y)
	# predict
	fine_predict = svm_fine.predict(array_to_classify)

	results={}
	results['coarse_class'] = coarse_predict[0] 
	results['fine_class'] = fine_predict[0]

	return results

@app.route("/quails/wordnetdefs")
def wordnetdefs():
	nounphrases = request.args.getlist('nounphrases')
	
	
	definitions = []
	for nounphrase in nounphrases:
		print nounphrase
		slist = nounphrase.split(" ")
		if len(slist) > 1:
			s = "_".join(slist)
		if s.endswith('_'):
			s = s[:-1]
		synsets = wn.synsets(s)
		print synsets
		if len(synsets) > 0:
			for synset in synsets:
				print synset.definition()
				definitions.append(str(synset.definition()))
	
		
	
	return jsonify(results=definitions)
	

@app.route("/quails/getdocs")
def getdocs():
	params = dict(request.args.items())
	search_terms = params['NPS'].split(quails.DELIMITER)
	try:
		ix = index.open_dir("indexQ")
		
	except:
		return jsonify(failure="Index not found.  Ensure that index exists and tries again.")

	qp = MultifieldParser(["title","body"], schema=ix.schema)

	queries = []
	for term in search_terms:
		queries.append(qp.parse(term))

	docs = OrderedDict()
	hit_list = []
	with ix.searcher() as searcher:
		
		for query in queries:
			
			results=searcher.search(query)	
	
			for result in results: 
				hit_list.append((str(query),result['title']))

	return jsonify(results=hit_list)

@app.route("/quails/passagextract")
def passagextract():
	
	params = dict(request.args.items())

	nps = params['NPS'].split(quails.DELIMITER)

	print "Print NPS"
	for np in nps:
		print np

	sents = []

	for filename in os.listdir("wiki-resources"):
		try:
			f=open("wiki-resources/" + filename, 'r')
		except: 
			print "Resource " + filename + " not found."
#		return jsonify(results=str("Passage extraction error, see server log."))

		lines = f.readlines()

		raw = []
		for line in lines:
			raw.append(line.strip('\n'))

		body = " ".join(raw)

		sentences = nltk.tokenize.sent_tokenize(body) 	

		
		for sent in sentences:
			for np in nps:
				if str(np) in str(sent):
					# print str(sent)
					sents.append(sent)

	#print len(sents)

	return jsonify(results=sents)

@app.route("/quails/answerextract")
def answerextract():
	return jsonify(success="Found answer extract!")



if __name__=="__main__":
	app.run(debug=True)

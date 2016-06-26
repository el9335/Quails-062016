import sys 
import requests
import quails
from collections import OrderedDict


################
# Initialization
# ==============
################

# validate and store input
if len(sys.argv) != 2:
	print "Usage: python test.py \"What is Obama's email address?\""
	sys.exit()

text = sys.argv[1]

# initialize new question object
question = quails.Question(text)

# get user preferences from 'config/quails.config
config = quails.Config(quails.CONFIG_FILE)

####################################################
# Question Analysis
# =================
#
# 1.  Run question through NLP pipeline
# 2.  Classify question into coarse and fine classes
#
####################################################

# build URL for '/nlp', pipeline string and preferred step toolkits (e.g. 'nltk','stanfuns')
payload = OrderedDict()
nlp = config.get_nlp_pipeline()

# step format (step,toolkit)
# step[0] = step (e.g. 'parsetree') 
# step[1] = toolkit (e.g. 'toolkit')
for step in nlp:
	payload[step[0]] = step[1]

# build pipeline string from order of step preferences
# server will validate pipeline
# set pipeline here, if it is invalid the program will quit when error is returned from server
payload['pipeline'] = quails.DELIMITER.join(payload.keys())
question.set_nlp_pipeline(payload['pipeline'])
payload['text'] = question.get_text()

try:
	r = requests.get(quails.SERVER + "/nlp", params = payload)
except:
	print "Server error, exiting."
	sys.exit()

# removed ordered dict logic, could cause a problem, we'll see.
# set question nlp features
question.set_nlp_features(r.json())

# build URL for '/classification', text and user specified classification method (e.g. 'svm')

# reset payload dictionary
payload = OrderedDict()
payload['text'] = question.get_text()
classfn_prefs = config.get_classfn_prefs()

# clss[0] = 'classify'
# class[1]  = algorithm (e.g. 'svn') 
for clss in classfn_prefs:
	payload[clss[0]] = clss[1]

try:
	r = requests.get(quails.SERVER + "/classification", params = payload)
except:
	print "Server error, exiting."
	sys.exit()	

# set question coarse and fine classes
results = r.json()['results']
question.set_coarse_class(results['coarse_class'])
question.set_fine_class(results['fine_class'])

################## 
# Answer Retrieval
# ================
#
# 1. If coarse type is ENTY, DESC, or HUM, look for WordNet definition
# 2. For all questions, document retrieval 
# 3. Passage extraction
# 4. Candidate answers extraction (pull noun phrases)
# 5. Soft filtering (frequency dictionary (remove least occurring answers)
# 6. Return a list of candidate answers and scores

wordnet_classes = ['ABBR','ENTY','DESC','HUM']

# reset payload
payload = OrderedDict()
if question.get_coarse_class().upper() in wordnet_classes and 'nounphrases' in question.get_nlp_features():

	payload_phrases = []
	nps = question.get_nlp_features()['nounphrases']
	for np in nps:
		payload_phrases.append(np)

	payload['nounphrases'] = payload_phrases

	#print payload
	try:	
		r = requests.get(quails.SERVER + "/wordnetdefs", params = payload)
	except:
		print "Server error, exiting."
		sys.exit()

	
	answers = r.json()['results']
	for answer in answers:
		question.add_candidate_answer(answer)

question.merge_answers()
question.score_answers() 

print "Answers:"
answers = question.get_scored_answers()
count = 0
for ans in answers:
	count += 1
	print str(count) + "\t" + str(answers[ans]) + "\t" + ans

print "\n"

from __future__ import division
import configparser
from collections import OrderedDict, defaultdict

#import nltkfuns
#import stanfuns

# constants
CONFIG_FILE = "config/quails.config"
SERVER = "http://localhost:5000/quails"
DELIMITER = "+"
TRAINING_FILE = "training_questions/train_1000.label"

# lists etc.
# need a better solution for populating these
valid_pipelines = [['tokens'],['tokens','pos'],
		   ['tokens','pos','ner'],
		   ['tokens','pos','ner','headchunks'],
		   ['tokens','pos','headchunks','ner'],
		   ['tokens','pos','ner','headchunks','parsetree'],
		   ['tokens','pos','headchunks','ner','parsetree'],
		   ['tokens','pos','headchunks','ner','parsetree','deps'],
		   ['tokens','pos','ner','headchunks','parsetree','nounphrases'],
                   ['tokens','pos','headchunks','ner','parsetree','nounphrases']
		  ]
#toolkit_lists = {'nltk' : nltkfuns.nltkfuns, 'stanfuns' : stanfuns.stanfuns}
#toolkit_lists = {'nltk' : nltkfuns.nltkfuns}
# use this to determine which type
step_input = {'tokens':'text',
	      'pos':'tokens',
	      'ner':'pos',
	      'headchunks':'text',
	      'parsetree' : 'text',
	      'dep' : 'text',
	      'nounphrases' : 'parsetree'}
# Li, Roth Classifications
classes = {'ABBR':['abb','exp'],
	   'ENTY':['animal','body','color','cremat','currency','dismed',
		   'event','food','instru','lang','letter','other',
		   'plant','product','religion','sport','substance',
		   'symbol','techmeth','termeq','veh','word'],
	   'DESC':['def','desc','manner','reason'],
	   'HUM':['gr','ind','title','desc'],
	   'LOC':['city','country','mount','other','state'],
	   'NUM':['code','count','date','dist','money','ord','other',
		  'period','perc','speed','temp','volsize','weight']}

# objects
class Question(object):
	total_ans = 0
	candidate_answers = []
	merged_answers = []
	frequencies = defaultdict(int)
	scored_answers = OrderedDict()

	def __init__(self, text):
		self.text = text
	
	def get_text(self):
		return self.text
	
	def set_nlp_pipeline(self, nlp_pipeline):
		self.nlp_pipeline = nlp_pipeline

	def get_nlp_pipeline(self):
		return self.nlp_pipeline

	def set_nlp_features(self, nlp_features):
		self.nlp_features = nlp_features

	def get_nlp_features(self):
		return self.nlp_features

	def set_coarse_class(self, coarse_class):
		self.coarse_class = coarse_class

	def get_coarse_class(self):
		return self.coarse_class

	def set_fine_class(self, fine_class):
		self.fine_class = fine_class

	def set_docs(self, docs):
		self.docs = docs

	def get_docs(self):
		return self.docs

	def set_sents(self, sents):
		self.sents = sents

	def get_sents(self):
		return self.sents

	def add_candidate_answer(self, candidate_answer):
		#print candidate_answer
		self.candidate_answers.append(candidate_answer) 

	def get_candidate_answers(self):
		return self.candidate_answers
	def get_frequencies(self):
		return self.frequencies
	def get_scored_answers(self):
		return self.scored_answers	

	def merge_answers(self):
		# as development of the systems progresses,
		# the approach to merging will need to be 
		# more sophisticated
		
		
		for ans in self.candidate_answers:
			self.total_ans += 1	
			self.frequencies[ans] += 1 

		self.merged_answers = set(self.candidate_answers)
		
	def score_answers(self):
		for freq in self.frequencies:
			self.scored_answers[freq] = self.frequencies[freq]/self.total_ans	
		#print self.scored_answers

	def about(self):
		print "Question: " + self.text
		print
		print "Pipeline:"
		try:
			print self.nlp_pipeline
		except:
			print "Pipeline not yet defined."
		print
		print "NLP Features:"
		try:
			for feature in self.nlp_features:
				print feature + ":"
				print self.nlp_features[feature]
				print
		except:
			pass
			#print "NLP Features not yet set."
		try:
			print "Coarse class: " + self.coarse_class
		except:
			pass
			#print "Coarse class not yet set."
		try:
			print "Fine class: " + self.fine_class
		
		except:
			pass
			#print "Fine class not yet set."
		try:
			print "Docs:"
			for doc in self.docs:
				# print "Search engine query: " + doc[0]
				print "Title: " + doc[1] 
			print
		except:
			pass

		try:
			print "Extracted passages:"
			for sent in self.sents:
				print sent
		except:	
			pass
		
		print "Scored answers <answer number, score, answer>:"
		self.count = 0 
		for answer in self.scored_answers:
			self.count += 1
			print str(self.count) + "\t" + str(self.scored_answers[answer]) + "\t" + answer
		
class Config(object):

	nlp_pipeline = []
	classfn_prefs = []

	def __init__(self, file):
		self.file = file

		self.config = configparser.ConfigParser()
		self.config.read(self.file)

		if 'NLP' in self.config:
			
			self.items = OrderedDict(self.config.items('NLP'))
	
			for item in self.items:
				if item != '0':
					self.nlp_pipeline.append((item, self.items[item]))			
			
		else:
			print "No NLP preferences found in " + self.file + "."
		
		if 'Classification' in self.config:
                        self.items = OrderedDict(self.config.items('Classification'))

              		for item in self.items:
				if item != '0':
					self.classfn_prefs.append((item, self.items[item]))

                else:
                        print "No Classication preferences found in " + self.file + "."

	
	def get_nlp_pipeline(self):
		return self.nlp_pipeline

	def get_classfn_prefs(self):
		return self.classfn_prefs

def get_training_sets():

        f = open(TRAINING_FILE)

        lines = f.readlines()
        f.close()

        coarse_training_qs = []
	coarse_training_targets = []
        fine_training_qs = []
	fine_training_targets = []

        for line in lines:
                toks = line.split(" ")
                classes = toks[0].split(":")
                class_coarse = classes[0]
                class_fine = classes[1]
                question = " ".join(toks[1:len(toks)]).strip('\n')

                #print "Coarse class: " + class_coarse
                #print "Fine class: " + class_fine
                #print "Question: " + question

		coarse_training_qs.append(str(question))
		coarse_training_targets.append(str(class_coarse))
		fine_training_qs.append(str(question))
		fine_training_targets.append(str(class_fine))

        results = {}
        results['coarse_training_qs'] = coarse_training_qs
        results['coarse_training_targets'] = coarse_training_targets
	results['fine_training_qs'] = fine_training_qs
	results['fine_training_targets'] = fine_training_targets

        return results

import nltk

heads = {"who", "what", "where", "when", 
	      "why", "how", "whose", "how often", 
	      "how old", "what time", "with whom"}

def tokens(input):
	# accepts a text string
	# returns a list of tokens
	return nltk.word_tokenize(input)

def pos(input):
	# accepts a list of tokens
	# returns a list of pairs of form (token, pos_tag)
	# VVVVV THIS IS THE CORRECT WAY
	return nltk.pos_tag(input)
	#return nltk.pos_tag(nltk.word_tokenize(input))

def ner(input):
	# accepts a list of pairs of form (token, pos_tag)
	# returns a list of pairs of form (token, entity_type)
	# VVVVV THIS IS THE CORRECT WAY
	chunks = nltk.chunk.ne_chunk(input) 
	# chunks = nltk.chunk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(input)))
	nes = []
	for c in chunks:
		if hasattr(c,'label'):
			nes.append((str(c[0][0]),c.label().lower()))
	return nes

def headchunks(input):
	# accepts a text string
	# accepts a list of tokens
	# returns a singleton head chunk
	text = input.lower()
	results = []
	for chunk in heads:
		if chunk in text:
			results.append(chunk)
	return results		

# auxillary function for nounphrases
def np_filter(tree):
        return tree.label() == 'NP'

# this version removes determiners, should probably make a specific function
def nounphrases(input):
	# accepts a dependency tree string
	# returns a list of nounphrases
	# noun phrases are represented as lists of words

	tree = nltk.Tree.fromstring(input)
	subtrees = tree.subtrees(filter = np_filter)
	nounphrases = []

	for st in subtrees:
		pos = st.pos()
		np = ""
		for p in pos:
			if p[1] != 'DT':
				np += p[0] + " "
			
		nounphrases.append(np)
	
	return nounphrases
	
nltkfuns = {'tokens' : tokens,
	   'pos' : pos,
           'ner' : ner,
	   'headchunks' : headchunks,
	   'nounphrases' : nounphrases}



from corenlp import StanfordCoreNLP
corenlp_dir = "./stanford-corenlp-full-2014-08-27"
corenlp = StanfordCoreNLP(corenlp_dir)

def parsetree(input):
	# accepts a text string
	# outputs a text string

	results = corenlp.raw_parse(input)
	return results['sentences'][0]['parsetree']

def deps(input):
	# accepts a text string
	# outputs a text string

	results = corenlp.raw_parse(input)
	return results['sentences'][0]['tuples']

stanfuns = {'parsetree' : parsetree,
	    'deps' : deps}

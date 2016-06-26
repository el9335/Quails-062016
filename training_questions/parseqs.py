def get_training_sets():

	f = open('train_1000.label')

	lines = f.readlines()
	f.close()

	coarse_training=[]
	fine_training=[]

	for line in lines:
		print line
		toks = line.split(" ")
		classes = toks[0].split(":")
		class_coarse = classes[0]
		class_fine = classes[1]
		question = " ".join(toks[1:len(toks)])

		#print "Coarse class: " + class_coarse
		#print "Fine class: " + class_fine
		#print "Question: " + question
	
		coarse_training.append((class_coarse, question))
		fine_training.append((class_fine, question))

	results = {}
	results['coarse_training'] = coarse_training
	results['fine_training'] = fine_training

	return results

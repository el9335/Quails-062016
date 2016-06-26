import os
import sys
from whoosh import index
from whoosh.fields import *
from collections import OrderedDict

#if len(sys.argv) != 2:
#	print "Usage: python quails_indexer.py <relative or abs path to documents to be indexed>"
#	sys.exit()

schema = Schema(title=TEXT(stored=True, field_boost=2.0), body=TEXT)

if not os.path.exists("indexQ"):
	os.mkdir("indexQ")

ix = index.create_in("indexQ", schema)

documents = OrderedDict()

for filename in os.listdir("wiki-resources"):

	try:
		f = open("wiki-resources/" + filename, 'r')
	except:
		print "Resource " + filename + " not found."
		sys.exit()

	lines = f.readlines()

	raw = []
	for line in lines:
		raw.append(line.strip('\n'))

	body = " ".join(raw)

	documents[filename]=body

	f.close()

writer = ix.writer()

#for document in documents:
#	print document + ": " + documents[document] 

for document in documents:
	writer.add_document(title=unicode(str(document),"utf-8"), body=unicode(str(documents[document]),"utf-8"))	

writer.commit()

from collections import Counter
import pickle
import json

def build(st):
	if st=='benign':
		with open("benignwords.txt", "r") as f:
			words=f.readlines()
			i=0
			while i<len(words):
				words[i]=words[i].lower().strip("\n")
				i+=1
			counts = Counter(words)
			json.dump(counts, open('bdic.json', 'wb'), indent=4, sort_keys=False)
		
	elif st=='malicious':
		with open("maliciouswords.txt", "r") as f:
			words=f.readlines()
			i=0
			while i<len(words):
				words[i]=words[i].lower().strip("\n")
				i+=1
			counts = Counter(words)
			#pickle.json( counts, open( "mdic.p", "wb" ) )
			json.dump(counts, open('mdic.json', 'wb'), indent=4, sort_keys=False)
		



build("benign")
				


		
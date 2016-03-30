import numpy as np
from sklearn import preprocessing
from sklearn import metrics
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
from sklearn.svm import SVC
from sklearn.externals import joblib
import json
import feature_extraction.py

def test(url):
	
	data=save_data(url).copy()
	
	bdic= json.load( open( "bdic.json", "rb" ) )
	mdic= json.load( open( "mdic.json", "rb" ) )
	process=json.load(open("all.json",'r'))

	url_length = 0
	out_of_place = 0
	ip_check = 0
	nameservers = 0
	location = 0
	special_char = 0
	tags_count = 0
	term=0
	
	for process_data in process:
		if process[process_data]["url_length"] == data["url_length"]:
			url_length = url_length + 1
		if process[process_data]["no_of_out_of_place_features"] == data["no_of_out_of_place_features"]:
			out_of_place = out_of_place + 1
		if process[process_data]["ip_check"] == data["ip_check"]:
			ip_check = ip_check + 1
		if process[process_data]["nameservers"] == data["nameservers"]:
			nameservers = nameservers + 1
		if process[process_data]["location"] == data["location"]:
			location = location + 1
		if process[process_data]["special_char_count"] == data["special_char_count"]:
			special_char = special_char + 1
		if process[process_data]["url_length"] == data["url_length"]:
			url_length = url_length + 1
		if process[process_data]["tags_count"] == data["tags_count"]:
			tags_count+=1
		
		lsum=0
		liss=data["terms"]
		if liss:
			for li in liss:
				if not li in bdic:
					term=-1
				elif not li in mdic:
					term=1
				elif bdic[li]>mdic[li]:
					term=1
				elif bdic[li]<mdic[li]:
					term=-1
				else:
					term=0
				lsum+=term

		lis = [url_length,out_of_place,ip_check,nameservers,location,special_char,tags_count,lsum]
		print lis
		model=joblib.load("trainmodelnb.pkl")
		print model.predict(lis)
	
	print len(data)	

	
test("benign")

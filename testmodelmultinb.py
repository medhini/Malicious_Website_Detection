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
import csv


def test(stri):

	bdic= json.load( open( "bdic.json", "rb" ) )
	mdic= json.load( open( "mdic.json", "rb" ) )

	if stri=='malicious':
		flist=[]
		data = json.load(open("phish50.json", 'r'))
		process=json.load(open("all.json",'r'))

		for each in data:

			url_length = 0
			out_of_place = 0
			ip_check = 0
			nameservers = 0
			location = 0
			special_char = 0
			tags_count = 0
			term=0
			for process_data in process:
				if process[process_data]["url_length"] == data[each]["url_length"]:
					url_length = url_length + 1
				if process[process_data]["no_of_out_of_place_features"] == data[each]["no_of_out_of_place_features"]:
					out_of_place = out_of_place + 1
				if process[process_data]["ip_check"] == data[each]["ip_check"]:
					ip_check = ip_check + 1
				if process[process_data]["nameservers"] == data[each]["nameservers"]:
					nameservers = nameservers + 1
				if process[process_data]["location"] == data[each]["location"]:
					location = location + 1
				if process[process_data]["special_char_count"] == data[each]["special_char_count"]:
					special_char = special_char + 1
				if process[process_data]["url_length"] == data[each]["url_length"]:
					url_length = url_length + 1
				if process[process_data]["tags_count"] == data[each]["tags_count"]:
					tags_count+=1
			lsum=0
			liss=data[each]["terms"]
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
			lis2= [url_length,out_of_place,ip_check,nameservers,location,special_char,tags_count,lsum,-1]
			
			flist.append(lis2)
			print lis
			model=joblib.load("trainmodelmultinb.pkl")
			print model.predict(lis)
		print len(data)	
		with open("confusion2.csv", "a") as f:
			writer = csv.writer(f)
			writer.writerows(flist)
	
	if stri=='benign':
		flist=[]
		data = json.load(open("benign(testing60).json", 'r'))
		process =json.load(open("all.json",'r'))
		

		
		#print data
		final_list = []
		for each in data:

			url_length = 0
			out_of_place = 0
			ip_check = 0
			nameservers = 0
			location = 0
			special_char = 0
			tags_count = 0
			term=0
			for process_data in process:
				if process[process_data]["url_length"] == data[each]["url_length"]:
					url_length = url_length + 1
				if process[process_data]["no_of_out_of_place_features"] == data[each]["no_of_out_of_place_features"]:
					out_of_place = out_of_place + 1
				if process[process_data]["ip_check"] == data[each]["ip_check"]:
					ip_check = ip_check + 1
				if process[process_data]["nameservers"] == data[each]["nameservers"]:
					nameservers = nameservers + 1
				if process[process_data]["location"] == data[each]["location"]:
					location = location + 1
				if process[process_data]["special_char_count"] == data[each]["special_char_count"]:
					special_char = special_char + 1
				if process[process_data]["url_length"] == data[each]["url_length"]:
					url_length = url_length + 1
				if process[process_data]["tags_count"] == data[each]["tags_count"]:
					tags_count+=1
			lsum=0
			liss=data[each]["terms"]
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
			lis2=[url_length,out_of_place,ip_check,nameservers,location,special_char,tags_count,lsum,1]
			
			flist.append(lis2)
			print each
			print lis
			model=joblib.load("trainmodelmultinb.pkl")
			print model.predict(lis)

			
		print len(data)
		with open("confusion.csv", "a") as f:
				writer = csv.writer(f)
				writer.writerows(flist)
test("benign")

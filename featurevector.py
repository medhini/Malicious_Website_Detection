import json
import csv

def feature_vector(stri):
	bdic= json.load( open( "bdic.json", "rb" ) )
	mdic= json.load( open( "mdic.json", "rb" ) )
	process=json.load(open("all.json",'r'))
	if stri=="benign":
	 	data = json.load(open("benign(testing60).json", 'r'))
	
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



			lis = [url_length,out_of_place,ip_check,nameservers,location,special_char,tags_count,lsum,1]
			print lis
			final_list.append(lis)
			
			json.dump(final_list, open('bvec.json', 'wb'), indent=4, sort_keys=False)
			

		print len(final_list)
		with open("f_vectorstry.csv", "a") as f:
			writer = csv.writer(f)
			writer.writerows(final_list)
		return final_list

	elif stri=="malicious":
		data = json.load(open("phish50.json", 'r'))
		ec=0
		pc=0

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



			lis = [url_length,out_of_place,ip_check,nameservers,location,special_char,tags_count,lsum,-1]
			print lis
			final_list.append(lis)
			json.dump(final_list, open('nvec.json', 'wb'), indent=4, sort_keys=False)
			if len(final_list) ==500:
				break
			

		print len(final_list)
		with open("f_vectorstry2.csv", "a") as f:
			writer = csv.writer(f)
			writer.writerows(final_list)
		return final_list

		

feature_vector("benign")
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
#import feature_extraction.py

import dns.resolver
from bs4 import BeautifulSoup
import time
import requests
import sys
from topia.termextract import tag
from topia.termextract import extract
import nltk
from nltk.data import load
import pickle
from IPy import IP
import re
import urllib2,httplib,pdb
from bs4 import BeautifulSoup
from tidylib import tidy_document
import pdb
import json 
import re

rdctr=0
feature={}
class SmartRedirectHandler(urllib2.HTTPRedirectHandler):     
    def http_error_301(self, req, fp, code, msg, headers):  
        global rdctr
	result = urllib2.HTTPRedirectHandler.http_error_301(
		 self, req, fp, code, msg, headers)              
        result.status = code                                 
#	print code
#	print result.status
	rdctr+=1
        return result                                       

    def http_error_302(self, req, fp, code, msg, headers):  
        global rdctr
	result = urllib2.HTTPRedirectHandler.http_error_302(
            self, req, fp, code, msg, headers)              
        result.status = code                                
#	print code
	rdctr+=1
#	print result.status
        return result 


#function to find nameservers
def nameservers(url):
	try:
		answer=dns.resolver.query(url,'NS')
		#print "Name servers of the URL :"
		#for i in answer:
		#	print i
		return len(answer)
	except:
		pass

#Function that returns location of server
def location(url):
	try:
		fdata={'Accept':'*/*',
		'Accept-Encoding':'gzip, deflate',
		'Accept-Language':'en-US,en;q=0.8',
		'Connection':'keep-alive',
		'Content-Length':'29',
		'Content-type':'application/x-www-form-urlencoded',
		'Cookie':'PHPSESSID=hisbu0rrh09nssn99vckkqr740; __utma=103585558.1324897437.1443987736.1443987736.1443987736.1; __utmb=103585558.2.10.1443987736; __utmc=103585558; __utmz=103585558.1443987736.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided)',
		'Host':'get-site-ip.com',
		'Origin':'http://get-site-ip.com',
		'Referer':'http://get-site-ip.com/',
		'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'}
		response=requests.post('http://get-site-ip.com/_pages/_moduler/ajaxSkrivUtIpPaNamn.php',data={'dnsNakeLookUp_In':url})
		#print response.content
		soup=BeautifulSoup(response.content,"lxml")
		#print "Location : "
		for i in soup.find_all("div", { "class" :"response"}):
		#	print i.get_text()
		#	print i.get_text().split('-')[2].replace(' ','')
			return i.get_text().split('-')[2].replace(' ','')
	except:
		pass

#Finds number of special characters
def spcount(url):
	count=0
	if '.' in url or '-' in url or '_' in url or '/' in url or '=' in url:
		count+=1
#	print "Number of Special Characters = " + str(count)
	return count

#Returns list of keywords in website

'''def terms(url):
	terms={}
	url="http://www." + url
	html=requests.get(url)
	content=html.content.decode("utf-8")
	soup=BeautifulSoup(content,"lxml")
	
	for script in soup(['script','style']):
		script.extract

	text=soup.get_text().decode("utf-8")
	print(text)
	
	[s.extract() for s in soup(['style', 'script', '[document]', 'head', 'title'])]
	visible_text = soup.getText()
	#print visible_text.decode
	f=open('haha4.txt','w')
	f2=open('keys','a')
	for i in visible_text:
		f.write(i.encode('utf-8'))
		if not i in terms:
			terms[i]=1
		else:
			terms[i]=terms[i]+1
			#print "yees"
	pickle.dump(terms,f2)
	f2.close()
	f.close()

	tagger = tag.Tagger('english')
	tagger.initialize()
	 
	 # create the extractor with the tagger
	extractor = extract.TermExtractor(tagger=tagger)
	 # invoke tagging the text
	s = nltk.data.load('haha4.txt',format = 'raw')
	extractor.tagger(s)
	 # extract all the terms, even the &amp;quot;weak&amp;quot; ones
	extractor.filter = extract.DefaultFilter(singleStrengthMinOccur=1)
	 # extract
	#print extractor(s)
	return terms
'''


#Returns boolean value about whether ip is valid or not
def ipchecker(url):
	p=re.compile("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}")
	fl=0
	if p.search(url):
		matches=re.search(p,url)
		ip=matches.group(0)
		#print "\nIP addres exists in URL : ",ip

		try:
			IP(ip)
			fl=1
		except Exception:
			fl=-1
	return fl
		
'''
	else :
		print "IP Address does not exist in URL"

	if fl==1:
		print "Valid IP Address exists"

	if fl==-1:
		print "Invalid IP Address exists"
'''
	
	

#Function that returns no of redirections
def noredirects(urll):
	try:
		global rdctr
		urll="http://www." + urll
		httplib.HTTPConnection.debuglevel = 1
	    #pdb.set_trace()

	    #request = urllib2.Request('http://diveintomark.org/redir/example301.xml')

		request = urllib2.Request(urll)
		opener = urllib2.build_opener(SmartRedirectHandler())
	    #opener = urllib2.build_opener()

		f = opener.open(request)

	    #f2 = opener.open(response)
	    #print f.url
	    #print "Number of total redirects = ",rdctr
	    #print f.headers.dict
	    #print f.status
	    
	#print "Number of redirects = " + str(rdctr)	
		return rdctr
	except:
		pass
#Function that returns nofoutofplacecharacters
def nofoutofplacefeatures(url):
	try:
	

	#	pdb.set_trace()

		if url[:4]=="http":
			r = requests.get(url)
		else:
			url="http://"+url
			r  = requests.get(url)

		#r = requests.get(url)
		data = r.text
		data2=r.content

		document, errors = tidy_document(data,
		  options={'numeric-entities':1})

		#print document
		#print errors
		#print "Number of Elements Out of Place : " + str(len(errors))
		return len(errors)
	except:
		pass

def reg_date(url):
	url=url.strip("www.")
	#print url
	ur="http://www.whois.com/whois/"+url
	r = requests.get(ur)
	data = r.content.decode("utf-8")

	#print data
	try :
		soup = BeautifulSoup(data,"lxml")
		#<div class="whois_result" 
		for link in soup.find_all("div",{"class":"whois_result"}):
			site = link.get_text().lower()
			#print site.decode("utf-8")
			print "\n Domain registration date is " + re.findall("\d\d-[a-z][a-z][a-z]-\d\d\d\d",site.decode("utf-8"))[1]
			
			return re.findall("\d\d-[a-z][a-z][a-z]-\d\d\d\d",site.decode("utf-8"))[1]
	except:
		pass

def tags_count(url):
	try:
		htmlcount=0
		scriptcount=0
		iframecount=0
		hrefcount=0
		embedcount=0
		objectcount=0
		url="http://" + url
		r1 = requests.get(url)
		data1 = r1.text
		soup1 = BeautifulSoup(data1,"lxml")
		for htmltag in soup1.find_all('html'):
			htmlcount = htmlcount + 1
		for scripttag in soup1.find_all('script'):
			#print scripttag
			scriptcount = scriptcount + 1
		for iframetag in soup1.find_all('iframe'):
			#print iframetag
			iframecount = iframecount + 1
		for hreftag in soup1.find_all('a'):
			#print iframetag
			hrefcount = hrefcount + 1
		for embedtag in soup1.find_all('embed'):
			#print iframetag
			embedcount = embedcount + 1
		for objecttag in soup1.find_all('object'):
			#print iframetag
			objectcount = objectcount + 1
		count={}
		count["html"] = htmlcount
		count["script"] = scriptcount
		count["iframe"] = iframecount
		count["href"] = hrefcount
		count["embed"] = embedcount
		count["object"] = objectcount
		return count
	except:
		pass

def terms(url):
	try:
		terms={}
		url="http://"+url
		html=requests.get(url)
		content=html.content.decode("utf-8")
		soup=BeautifulSoup(content,"lxml")
		#print soup.get_text()
		'''
		for script in soup(['script','style']):
			script.extract

		text=soup.get_text().decode("utf-8")
		print(text)
		'''
		[s.extract() for s in soup(['style', 'script', '[document]', 'head', 'title','select'])]
		visible_text = soup.getText()
		#print soup.getText()

		#print visible_text.decode

		'''f=open('haha4.txt','w+')
		
		for i in visible_text:
			f.write(i.encode('utf-8'))
		f.close()
	'''
		tagger = tag.Tagger('english')
		tagger.initialize()
		 
		 # create the extractor with the tagger
		extractor = extract.TermExtractor(tagger=tagger)
		 # invoke tagging the text
		
		patt="((?: [\x00-\x7F] | [\xC0-\xDF][\x80-\xBF] | [\xE0-\xEF][\x80-\xBF]{2} | [\xF0-\xF7][\x80-\xBF]{3}){1,100})"

		#s = nltk.data.load('/home/suryansh/webTech/finalcrawler/haha4.txt',format = 'raw').lower()
		#s = nltk.data.load(url,format = 'raw').lower()
		s=visible_text.encode("utf-8")

	#	print "s is: \n"+s
	#	print "\n s is done"
		re.sub(patt,'',visible_text.encode("utf-8"))
		extractor.tagger(s)
		 # extract all the terms, even the &amp;quot;weak&amp;quot; ones
		extractor.filter = extract.DefaultFilter(singleStrengthMinOccur=1)
		 # extract
		
		print extractor(s)
		result=[]
		for ss in extractor(s):
			#print ss[0]
			for i in ss[0].split(" "):
				for j in i.split("-"):
					if not j in result:
						result.append(j)


	#	print result

		with open("beingnwords(testing80).txt", "a") as myfile:
			for i in result:
				myfile.write(i+"\n")

		return result
	except:
		pass


def save_data(url):
	#feature={}
	feature["no_of_out_of_place_features"] = nofoutofplacefeatures(url)
	feature["reg_date"]=reg_date(url)
	feature["no_of_redirects"] = noredirects(url)
	feature["ip_check"] = ipchecker(url)
	feature["nameservers"] = nameservers(url)
	feature["location"] = location(url)
	feature["special_char_count"] = spcount(url)
	feature["url_length"] = len(url)
	feature["tags_count"] = tags_count(url)
	termlist=[]
	termlist=terms(url)

	feature["terms"]=termlist
	#with open('/home/suryansh/webTech/file.json', 'a') as f:
	 #   json.dump(feature, f)
	return feature


def test(url):
	print url
	data=save_data(url).copy()
	#data=url
	#print url1
	#print data
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
	#print lis
	model=joblib.load("trainmodelmultinb.pkl")
	print model.predict(lis)
	#return model.predict(lis)
	#print len(data)	

#urls=json.load(open("benign(testing60).json","r"))
#print urls
#for url in urls:	
#test("http://nedbankweb.com/nedadmin/ned/newned.html")
#test("http://grospeedo.com/cgi-sys/suspendedpage.cgi")

#test("http://stylishwife.com")
#test("sportamore.se")
#test("nitk.ac.in")
#test("snapdeal.com")
#for url in urls:
#	test(url)
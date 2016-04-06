import requests
from bs4 import BeautifulSoup
import numpy as np
import unicodedata
import urllib
import csv

def extractFromURL(url):
	f = open('url_list', 'a')

	url = urllib.urlopen(url)

	soup = BeautifulSoup(url)
	
	print soup

	table = soup.find('table', {"class" : "data"})

	tr = soup.findAll('tr')
	
	urls = []

	for r in range(len(tr) - 1):
		td = tr[r].findAll('td')

		if(len(td) < 5):
			continue

		for d in range(len(td)):
			if(d == 1):
				url = unicodedata.normalize('NFKD', td[d].text).encode('ascii','ignore')
				url = url.split('...')[0]
				url = url.split('//')[1]
				url = url.split('/')[0]
				#row.append(unicodedata.normalize('NFKD', td[d].text).encode('ascii','ignore'))
				f.write(url)
				f.write('\n')

url = 'https://www.phishtank.com/phish_archive.php?page=100'
extractFromURL(url)

'''
pageNumber = 0
while(pageNumber <= 25):
	print "Extracting from page " + str(pageNumber)
	url = 'https://www.phishtank.com/phish_archive.php?page=' + str(pageNumber)
	extractFromURL(url)
	pageNumber += 1
'''	

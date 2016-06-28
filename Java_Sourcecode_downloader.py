import requests
from bs4 import BeautifulSoup

'''
Downloads the Java source code from grepcode.com for the methods present
in the file you run the script on. 
'''

# website used to get source code 
website = "http://grepcode.com"

# query url used to get source code 
url = "http://grepcode.com/search/?query="


def firstStage(methodName):

	# make the query using the method name 
	url = url + methodName
	r = requests.get(url)

	# create BeautifulSoup object for the site with query results
	soup = BeautifulSoup(r.content, "html.parser")

	# find all results of search for div tags with class "result-list"
	results = soup.find_all("div", {"class":"result-list"})

	# get all links 
	soup = BeautifulSoup(str(results), "html.parser")
	links = soup.find_all("a")

	for link in links:
		print(link.get("href"))
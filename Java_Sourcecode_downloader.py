import requests
from bs4 import BeautifulSoup

'''
Downloads the Java source code from grepcode.com for the methods present
in the file you run the script on. 
'''


def downloadSourcecode(methodName, url, website):

	# make the query using the method name 
	url = url + methodName
	firstRequest = requests.get(url)
	# create BeautifulSoup object for the site with query results
	soup = BeautifulSoup(firstRequest.content, "html.parser")

	# find all results of search for div tags with class "result-list"
	results = soup.find_all("div", {"class":"result-list"})

	# get all links 
	soup = BeautifulSoup(str(results), "html.parser")
	link = soup.find("a")

	print link.get("href")

	finalUrl = link.get("href")

	# after getting the url for the method documentation replace the .. with
	# the website url to get the correct url 
	finalUrl = finalUrl.replace("..", website)

	# use requests to get content for the new url 
	secondRequest = requests.get(finalUrl)

	soup = BeautifulSoup(secondRequest.content, "html.parser")

	rawDownloadLink = soup.find("a", title = "Download file")

	# separate "../" from the new url 
	downloadLinkHolder = str(rawDownloadLink).split("..")

	# last index in downloadLinkHolder is what we need
	# add full website url to get the correct download link 
	downloadLink = website + downloadLinkHolder[len(downloadLinkHolder) - 1]

	# use requests to get the required file 
	download = requests.get(downloadLink)

	# raise error is request was unsuccessful 
	download.raise_for_status()

	# make file object to write content to file 
	# open in write binary mode to maintain Unicode encoding of text
	finalFile = open(methodName + ".java", "wb")

	# write data in chunks of bytes (100000 in this case) to the file 
	for chunk in download.iter_content(100000):
		finalFile.write(chunk)

	finalFile.close()



def main():

	# website used to get source code 
	website = "http://grepcode.com"

	# query url used to get source code 
	url = "http://grepcode.com/search/?query="


	fileName = raw_input("Pleae enter the name of the file you want to read: ")
	
	# make a file object with read mode that reads all methods from the file 
	methodFile = open(fileName, "r")

	# loop over all the lines/methods in the file 
	for line in methodFile:
		if line != "\n":
			downloadSourcecode(line, url, website)
			print "Source code for " + line + " has been downloaded!"


if __name__ == "__main__": main()
import re, sys, unicodedata, os, json, RegexParser
from urllib import urlopen
from Reviews import *
from Responses import *
from HTMLParser import HTMLParser
from AlchemyAPI.alchemyapi import AlchemyAPI

class AmazonParser:
	""" Stores reviews from an Amazon.com product page in a list """

	def __init__(self, product_URL):
		""" Constructor """

		# Get review_URL from product_URL
		self.review_URL = str.replace(product_URL, "/dp/", "/product-reviews/")
		self.review_URL = str.replace(self.review_URL, "/gp/", "/product-reviews/")

		# Get the page's contents as an array of lines
		content = self.getContentFrom(self.review_URL)
		self.setProductInfo(content)
		self.reviews = Reviews(self.productName)

		# If the reviews have been parsed, read them from the disk.
		# Else parse them from the website and store them on disk.
		if self.reviewsOnDisk():
			self.readReviewsOnDisk()
			self.saveData()
		else:
			# Each iteration of the loop parses a review page 
			self.lastPage = self.currPage = 1
			while self.lastPage >= self.currPage:
				self.getReviewsFrom(content)
				content = self.getNextPageFrom(content)
			self.saveData()

	def getReviewsFrom(self, content):
		""" Takes a product review page in array form and returns a list
			of reviews on that page
			"""
		rating = helpfulVotes = title = date = userName = text = None
		startParsing = False

		# Go through every line in the page
		for line in content:

			# <!-- BOUNDARY --> represents the start of a new comment
			if startParsing is not True:
				if re.search('<![- ]*BOUNDARY[- ]*>', line):
					startParsing = True

			# Rating appears first along with helpful votes
			elif rating == None:
				# Helpful is grouped with rating because it may or may not appear
				if helpfulVotes == None: helpfulVotes = self.getHelpfulVotesFrom(line)
				rating = self.getRatingFrom(line)

			# Title and date appear next
			elif title == None or date == None: (title, date) = self.getTitleAndDateFrom(line)
			
			# Next comes the username
			elif userName == None: userName = self.getUserNameFrom(line)
			
			# Last comes the review text
			elif text == None: text = self.getTextFrom(line)
			
			# We now have all parts of the review
			else:
				self.reviews.add(Review(rating, title, date, userName, text))
				startParsing = False
				rating = helpful = title = date = userName = text = None


	def getNextPageFrom(self, content):
		""" Returns the content of the next page of reviews if it exists.
			Returns None otherwise.
			"""
		for line in content:

			# This line contains information for the next, previous, first
			# and last review page.
			if re.search('&lsaquo;[ ]*Previous', line):

				# Get the last page number. The max value of i for every instance
				# of pageNumber=i gives us the last page number. If this is more than
				# the existing value of self.lastPage, update it.
				newLastPage = 0
				if len([int(i) for i in re.findall('pageNumber=([0-9]+)', line)]) > 0:
					newLastPage = max([int(i) for i in re.findall('pageNumber=([0-9]+)', line)])
				self.lastPage = max(newLastPage, self.lastPage)

				# If there exists a next page, return it
				if self.lastPage > self.currPage:
					URLpart1 = re.search('http([^<>]+?)pageNumber=', line).group()
					URLpart2 = re.search('pageNumber='+ str(self.currPage+1)+ '(.+?)>', line).group()
					nextPage = URLpart1 + URLpart2[len("pageNumber="):-2]
					self.currPage += 1
					return self.getContentFrom(nextPage)
				break
		self.currPage += 1
		return None

	def getContentFrom(self, URL):
		""" Given a URL, returns its contents as an array of lines """
		sock = urlopen(URL)
		encoding = sock.headers['content-type'].split('charset=')[-1]
		content = sock.read()
		sock.close()
		ucontent = unicode(content, encoding)
		return unicodedata.normalize('NFKD', ucontent).encode('ASCII', 'ignore').split('\n')	

	def __str__(self):
		""" Outputs the reviews """
		s = '\n\n\n' + '#'*(len(self.productName)+20)
		s +=('\n#         ' +  self.productName + '         #\n')
		s +=('#'*(len(self.productName)+20) + '\n\n\n')
		s += str(self.reviews)
		return s

	def setProductInfo(self, content):
		""" Gets the ASIN number and product title """
		self.ASIN = self.productName = None
		for line in content:
			x = re.search("<meta[ ]*name=\"title\"[ ]*content=\"(.+?)\"[ ]*/>", line)
			if x:
				x = x.group(1).replace("Amazon.com: ", "", 1)
				self.productName = x.replace("Customer Reviews: ", "", 1)
				if self.ASIN != None and self.productName != None:
						return
			for ASIN in re.findall('[Aa][Ss][Ii][Nn]=(.{10,10})', line):
				if ASIN in self.review_URL:
					self.ASIN = ASIN
					if self.ASIN != None and self.productName != None:
						return
		print 'Could not get product info.\n'

	def saveData(self):
		""" Saves the reviews into a JSON file """
		if self.ASIN != None:
			dirName = "Reviews/" + self.ASIN + ' - ' + self.productName
			if not os.path.isdir(dirName): os.mkdir(dirName)
			filename = dirName + '/Reviews.json'
			self.reviews.saveData(filename)

	def reviewsOnDisk(self):
		""" Checks if product reviews have be retrieved """
		return os.path.isfile('Reviews/' + self.ASIN  + ' - ' + self.productName + '/Reviews.json')

	def readReviewsOnDisk(self):
		""" Reads reviews stored in a JSON file into the reviews data structure.
			Reviews must exist on disk.
			"""
		json_data=open('Reviews/' + self.ASIN  + ' - ' + self.productName + '/Reviews.json')
		data = json.load(json_data)
		review_List_JSON = data['Reviews']
		for review_JSON in review_List_JSON:
			self.reviews.add(Review(review_JSON['rating'],
								review_JSON['title'],
								review_JSON['date'],
								review_JSON['userName'],
								review_JSON['text']))

	def getResponses(self):

		alchemyapi = AlchemyAPI()

		if self.ResponsesOnDisk():
			# printResponsesFromDisk()
			responses = self.readResponsesOnDisk()
			# print responses
			dirName = "Reviews/" + self.ASIN  + ' - ' + self.productName
			if not os.path.isdir(dirName): os.mkdir(dirName)
			filename = dirName + '/Responses.json'
			responses.list.sort(reverse=True)
			responses.saveData(filename)
		
		else:
			responses = Responses(self.productName)
			for review in self.reviews.list:
				response = alchemyapi.keywords('text',review.text, { 'sentiment':1 })

				if response['status'] == 'OK':
					for keyword in response['keywords']:
						text = keyword['text'].encode('utf-8')
						relevance = keyword['relevance']
						sentiment = keyword['sentiment']['type'] 
						score = 0
						if 'score' in keyword['sentiment']:
							score = keyword['sentiment']['score']
						responses.add(Response(1, text, relevance, sentiment, score))
			dirName = "Reviews/" + self.ASIN  + ' - ' + self.productName
			if not os.path.isdir(dirName): os.mkdir(dirName)
			filename = dirName + '/Responses.json'
			responses.saveData(filename)
			print responses


	def ResponsesOnDisk(self):
		""" Checks if product responses have be retrieved """
		return os.path.isfile('Reviews/' + self.ASIN  + ' - ' + self.productName + '/Responses.json')

	def readResponsesOnDisk(self):
		""" Reads responses stored in a JSON file into the responses data structure.
			Responses must exist on disk.
			"""
		responses = Responses(self.productName)
		json_data=open('Reviews/' + self.ASIN  + ' - ' + self.productName + '/Responses.json')
		data = json.load(json_data)
		response_List_JSON = data['Responses']
		for response_JSON in response_List_JSON:
			responses.add(Response(response_JSON['count'],
								response_JSON['text'],
								response_JSON['relevance'],
								response_JSON['sentiment'],
								response_JSON['score']))
		return responses

	def printResponsesFromDisk(self):
		""" Prints the responses stored in the JSON file
			Responses must exist on disk.
			"""
		json_data=open('Reviews/' + self.ASIN  + ' - ' + self.productName + '/Responses.json')
		data = json.load(json_data)
		print str(data['Count']) + " reviews found.\n"
		response_List_JSON = data['Responses']
		for response_JSON in response_List_JSON:
			print (response_JSON['text'] + "\n"
				+ str(response_JSON['relevance']) + "\n"
				+ response_JSON['sentiment'] + "\n"
				+ str(response_JSON['score']) + "\n")
		print ''
		
	def getTextFrom(self, line):
		x = re.search("<div[ ]*class[ ]*=[ \'\"]+reviewText[ \'\"]+>(.*?)</div>", line)
		if x:
			text = x.group(1)
			text = ' '.join(text.split())
			return strip_tags(text.replace("<br />", "\n"))
		return None

	def getHelpfulVotesFrom(self, line):
		x = re.search('>([0-9]+?) of ([0-9]+?) people', line)
		if x:
			return x.group(1), x.group(2)
		return None

	def getRatingFrom(self, line):
		x = re.search('>([0-9].+?) out of', line)
		if x:
			return x.group(1)
		return None

	def getTitleAndDateFrom(self, line):
		# 'try' is faster than 'if' when no exception is thrown
		try:
			title = re.search('<b>(.+?)</b>', line).group(1)
			date = re.search('<nobr>(.+?)</nobr>', line).group(1)
			return title, date
		except AttributeError:
			return None, None

	def getUserNameFrom(self, line):
		x = re.search('<a.+?/profile/.+?span.+?>(.+?)</span></a>', line)
		if x:
			return x.group(1)
		return None

# Functionality for removing HTML tags
class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()
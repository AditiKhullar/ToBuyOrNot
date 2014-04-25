#from AlchemyAPI.alchemyapi import AlchemyAPI
import sys, os
#sys.path.append(os.path.abspath('../AlchemyAPI'))
from AmazonParser import *
from Reviews import *
from Responses import *
#import AlchemyAPI
from AlchemyAPI.alchemyapi import AlchemyAPI

# URL of product's main/ review page
#URL = "http://www.amazon.com/dp/B000Y9YJK4/"
URL = "http://www.amazon.com/dp/B000BVZ3BO/"


Parser = AmazonParser(URL)
alchemyapi = AlchemyAPI()
# Parser.getResponses() 


# Group text from all reviews into one text file to process
text = ''
singleText = ''
sentiment = []
print " \n Processing all documents sentiments iteratively \n "
for r in Parser.reviews.list:
	text += r.text
	singleText = r.text
	print "\n\n\n@@@@@@@Printing text here@@@@@@@\n\n\n"
	print r.text
	print "\n\n\n@@@@@@@END of text@@@@@@@@\n\n\n"

	currentResponse = alchemyapi.sentiment('text', singleText, { 'showSourceText':0 })

	#print "\n\n\nPRINT SENTIMENT ANALYSIS HERE\n\n\n"
	#print currentResponse
	#print "\\n\n\nEnd of sentiment analysis\n\n\n"

	if currentResponse['status'] == 'OK':
		#print('##currentResponse object')
		#print(json.dumps(currentResponse, indent=4))

		print('')
		print('### Document sentiment analysis ###')

		print('type: ', currentResponse['docSentiment']['type'])
	
        if 'score' in currentResponse['docSentiment']:
            print('score: ', currentResponse['docSentiment']['score'])
        else:
            print('Error in sentiment analysis call: ', currentResponse['statusInfo'])

        sentiment.append(float(currentResponse['docSentiment']['score']))

        print " \n ***DONE WITH CURRENT DOCUMENT. PROCESSING NEXT*** \n"

average = sum(sentiment) / float(len(sentiment))
print "\n\n\n###RESULT###\n\n\n"
print "average sentiment: \n"
print average

if average > 0:
	print "\n\n\nGO FOR IT\n\n\n"

#print " \n *******DONE WITH PROCESSING ALL DOCUMENTS********** \n"






"""
# commented from here to try sentiment analysis 
# and targeted sentiment analysis on individual reviews
# - Rajath - 04/25
# Option 1

print('Processing text: ', text)

print('')
print('')
print('')
print('############################################')
print('#   Keyword Extraction Example             #')
print('############################################')
print('')
print('')
print('')

response = alchemyapi.entities('url',URL, { 'sentiment':1 })

## debug
print "\n\n\n PRINTING RESPONSE HERE \n\n\n"
print response
print "\nEND OF PRINT\n"

if response['status'] == 'OK':
	print('## Response Object ##')
	print(json.dumps(response, indent=4))


	print('')
	print('## Entities ##')
	for entity in response['entities']:
		print('text: ', entity['text'].encode('utf-8'))
		print('type: ', entity['type'])
		print('relevance: ', entity['relevance'])
		print('sentiment: ', entity['sentiment']['type'])
		if 'score' in entity['sentiment']:
			print('sentiment score: ' + entity['sentiment']['score'])
		print('')
else:
	print('Error in entity extraction call: ', response['statusInfo'])
"""


# Option 2

# print('')
# print('')
# print('')
# print('############################################')
# print('#   Sentiment Analysis Example             #')
# print('############################################')
# print('')
# print('')
# print('')

# response = alchemyapi.sentiment('text',text)

# if response['status'] == 'OK':
# 	print('## Response Object ##')
# 	print(json.dumps(response, indent=4))

# 	print('')
# 	print('## Document Sentiment ##')
# 	print('type: ', response['docSentiment']['type'])
	
# 	if 'score' in response['docSentiment']:
# 		print('score: ', response['docSentiment']['score'])
# else:
# 	print('Error in sentiment analysis call: ', response['statusInfo'])

# print('Processing text: ', text)


# Option 3

# for word in ['price', 'quality', 'sound', 'tone', 'durability']:
# 	print('')
# 	print('')
# 	print('')
# 	print('############################################')
# 	print('#   Targeted Sentiment Analysis Example    #')
# 	print('############################################')
# 	print('')
# 	print('')

# 	print('Target: ', word)
# 	print('')

# 	response = alchemyapi.sentiment_targeted('text',text, word)

# 	if response['status'] == 'OK':
# 		print('## Response Object ##')
# 		print(json.dumps(response, indent=4))

# 		print('')
# 		print('## Targeted Sentiment ##')
# 		print('type: ', response['docSentiment']['type'])
		
# 		if 'score' in response['docSentiment']:
# 			# score += float(response['docSentiment']['score'])
# 			print('score: ', response['docSentiment']['score'])
# 	else:
# 		print('Error in targeted sentiment analysis call: ', response['statusInfo'])


# Option 4

# print('')
# print('')
# print('')
# print('############################################')
# print('#   Keyword Extraction Example             #')
# print('############################################')
# print('')
# print('')

# print('Processing text: ', text)
# print('')

# response = alchemyapi.keywords('text',text, { 'sentiment':1 })

# if response['status'] == 'OK':
# 	print('## Response Object ##')
# 	print(json.dumps(response, indent=4))


# 	print('')
# 	print('## Keywords ##')
# 	for keyword in response['keywords']:
# 		print('text: ', keyword['text'].encode('utf-8'))
# 		print('relevance: ', keyword['relevance'])
# 		print('sentiment: ', keyword['sentiment']['type']) 
# 		if 'score' in keyword['sentiment']:
# 			print('sentiment score: ' + keyword['sentiment']['score'])
# 		print('')
# else:
# 	print('Error in keyword extaction call: ', response['statusInfo'])

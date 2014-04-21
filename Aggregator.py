from AlchemyAPI.alchemyapi import AlchemyAPI
from AmazonParser import *
from Reviews import *
from Responses import *

# URL of product's main/ review page
URL = "http://www.amazon.com/dp/B000Y9YJK4/"


Parser = AmazonParser(URL)
alchemyapi = AlchemyAPI()
# Parser.getResponses() 


# Group text from all reviews into one text file to process
text = ''
for r in Parser.reviews.list:
	text += r.text


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

response = alchemyapi.entities('url',url, { 'sentiment':1 })

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

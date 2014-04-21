from AlchemyAPI.alchemyapi import AlchemyAPI
from Reviews import *
from List import *

class Responses(List):
	""" Manages reviews in a list """
	pass

class Response(Item):
	""" Represents a response consisting of a rating, title, date,
		userName and the response text.
		"""

	def __init__(self, count, text, relevance, sentiment, score):
		""" Constructor. Initializes with given parameters """

		self.count = count
		self.text = text
		self.relevance = float(relevance)
		self.sentiment = sentiment
		self.score = float(score)

	def __iadd__(self, other):
		""" += operator """
		total = self.count + other.count
		self.relevance = (self.relevance*self.count + other.relevance*other.count)/total
		self.score = (self.score*self.count + other.score*other.count)/total
		self.count = total
		if self.score > 0.0: self.sentiment = 'positive'
		elif self.score < 0.0: self.sentiment = 'negative'
		else: self.sentiment = 'neutral'

	def __eq__(self, other):
		""" Checks if the response keywords are equal """
		return self.text == other.text

	def __lt__(self, other):
         return self.relevance*self.count < other.relevance*other.count
from List import *

class Reviews(List):
	""" Manages reviews in a list """
	pass

class Review(Item):
	""" Represents a review consisting of a rating, title, date,
		userName and the review text.
		"""

	def __init__(self, rating, title, date, userName, text):
		""" Constructor. Initializes with given parameters """
		self.rating = rating
		self.title = title
		self.date = date
		self.userName = userName
		self.text = text

	def __eq__(self, other):
		""" Checks if this review has all the same parameters as the other
			review
			"""
		return self.__dict__ == other.__dict__
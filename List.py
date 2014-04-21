import json
from datetime import datetime

class List:

	def __init__(self, productName):
		""" Constructor """
		self.list = []
		self.productName = productName

	def add(self, new):
		""" Adds a new response to the list. Duplicates are ignored """
		if new != None:
			for r in self.list:
				if r == new:
					if self.__class__.__name__ == "Responses":
						r += new
					return
			self.list.append(new)

	def __str__(self):
		""" Outputs all the responses in the list """
		s = str(len(self.list)) + " " + self.__class__.__name__ + " found.\n\n"
		for r in self.list:
			s += str(r) + "\n"
		return s

	def saveData(self, filename):
		file = open(filename,'w')
		List_JSON = []
		for item in self.list:
			List_JSON.append(item.__dict__)

		JSON = {'Product Name' : self.productName}
		JSON.update({'Last Update' : str(datetime.now())})
		JSON.update({'Count' : str(len(self.list))})
		JSON.update({self.__class__.__name__ : List_JSON})

		json.dump(JSON, file, sort_keys=True, indent=4, separators=(',', ': '))

class Item:

	def __str__(self):
		""" String representation of the response """
		s = ''
		for i in self.__dict__.items():
			s += str(i[0]) + ': ' + str(i[1]) + '\n'
		return s
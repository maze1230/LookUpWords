class Word:
	def __init__(self, name, mean=None, synonym=None, sentence=None):
		self.name = name
		self.mean = mean
		self.synonym = synonym
		self.sentence = sentence

	def to_csv(self):
		return [self.name, ','.join(self.mean), ','.join(self.synonym), self.sentence]
class Player:
    
	name: str
	scores: List[int]

	def __init__(self, name: int):
		self.name = name
		self.scores = list()

	def get_top_score(self):
		pass

	def get_average_score(self, n: int):
		pass

	def add_new_score(self, score: int):
		pass
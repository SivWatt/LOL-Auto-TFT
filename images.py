from PIL import Image
import os

# class for storing images 
class MatchingImages:
	def __init__(self, cwd):
		path = os.path.join(cwd, 'image')
		self.matchBtn = Image.open( os.path.join(path, 'match.PNG') )
		self.acceptBtn = Image.open( os.path.join(path, 'accept.PNG') )
		self.ff1Btn = Image.open( os.path.join(path, 'ff1.PNG') )
		self.ff2Btn = Image.open( os.path.join(path, 'ff2.PNG') )
		self.againBtn = Image.open( os.path.join(path, 'again.PNG') )
		self.optionBtn = Image.open( os.path.join(path, 'option.PNG') )
		self.optionText = Image.open( os.path.join(path, 'optionText.PNG') )
		self.questConfirmBtn = Image.open( os.path.join(path, 'QuestConfirm.PNG') )

# end of class Image
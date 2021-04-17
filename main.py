import pyautogui
import win32gui
from PIL import Image

import time
import datetime
import os
import sys
from os import listdir

###########################################################
# Class definitions:

# class for storing images 
class Images:
	#static variables
	matchBtn = None
	acceptBtn = None
	ff1Btn = None
	ff2Btn = None 
	againBtn = None
	optionBtn = None
	questConfirmBtn = None

	@staticmethod 
	def initialize(cwd):
		path = cwd + '/image/'
		Images.matchBtn = Image.open( path + 'match.PNG' )
		Images.acceptBtn = Image.open( path + 'accept.PNG' )
		Images.ff1Btn = Image.open( path + 'ff1.PNG' )
		Images.ff2Btn = Image.open( path + 'ff2.PNG' )
		Images.againBtn = Image.open( path + 'again.PNG' )
		Images.optionBtn = Image.open( path + 'option.PNG' )
		Images.questConfirmBtn = Image.open( path + 'QuestConfirm.PNG' )

# end of class Image

# class for storing window rect and handler
class WindowProperty:
	#static variables
	#hwnd = None
	#rect = None

	# method passed to win32gui
	@staticmethod
	def windowEnumHandler(hwnd, top_windows):
		top_windows.append((hwnd, win32gui.GetWindowText(hwnd)))

	# bring league window to the front
	@staticmethod
	def bringFront(hwnd):
		win32gui.ShowWindow(hwnd, 9)
		win32gui.SetForegroundWindow(hwnd)

	# initialize the static variable
	# "league of legends", "league of legends (TM) Client"
	def __init__(self, name):
		top_windows = []
		self.windows = []
		win32gui.EnumWindows(WindowProperty.windowEnumHandler, top_windows)
		for i in top_windows:
			if name == i[1].lower():
				r = win32gui.GetWindowRect(i[0])
				self.windows.append((i[0], (r[0], r[1], r[2] - r[0], r[3] - r[1])))
				self.hwnd = i[0]
				self.rect = (r[0], r[1], r[2] - r[0], r[3] - r[1])
				#print(self.rect)
				#break

# end of class WindowProperty

#take screen shot when unexpect stuff happens
def takeScreen(cwd):
	# get time stamp
	dtNow = datetime.datetime.now()
	timestamp = dtNow.strftime("%Y%m%d-%H%M%S")
	pyautogui.screenshot(cwd + "/screen_" + timestamp + ".png")

###########################################################
# main script starts:

# get the current working directory
cwd = os.path.dirname(sys.argv[0]) if os.path.dirname(sys.argv[0]) != "" else "."

Images().initialize(cwd)

while 1:
	#can find both two windows
	client = WindowProperty('league of legends')
	while not (hasattr(client, 'hwnd')):
		client = WindowProperty('league of legends')

	#if there are more than one client handle
	for w in client.windows:
		if w[1][2] >= 1024 and w[1][3] >= 576:
			client.hwnd = w[0]
			client.rect = w[1]
			break
		# if client is minimized
		#elif w[1][0] == -32000 and w[1][1] == -32000:
		#	client.hwnd = w[0]
		#	client.rect = w[1]
		#	WindowProperty.bringFront(client.hwnd)
		#	break

	print(client.rect)
	WindowProperty.bringFront(client.hwnd)

	# start a match
	matchButton = pyautogui.locateCenterOnScreen(Images.matchBtn, region=client.rect, confidence=0.9)
	if matchButton:
		pyautogui.click(matchButton)
		print("click match")
	else:
		takeScreen(cwd)
	
	# accept a match
	acceptButton = None
	time.sleep(3)
	while acceptButton == None:
		acceptButton = pyautogui.locateCenterOnScreen(Images.acceptBtn, region=client.rect, confidence=0.7)
		print("wait 3 sec")
		time.sleep(3)
	
	# game start 
	play = WindowProperty('league of legends (tm) client')
	while not (hasattr(play, 'hwnd')):	
		print("has no hwnd sleep 3")
		play = WindowProperty('league of legends (tm) client')
		acceptButton = pyautogui.locateCenterOnScreen(Images.acceptBtn, region=client.rect, confidence=0.7)
		if acceptButton:
			pyautogui.click(acceptButton)
		time.sleep(3)
	
	#print(play)
	while not (hasattr(play, 'rect')):
		time.sleep(5)
		play = WindowProperty('league of legends (tm) client')
	
	while play.rect[2] == 1:
		time.sleep(2)
		play = WindowProperty('league of legends (tm) client')
		
	print(play.rect)
	WindowProperty.bringFront(play.hwnd)
	
	# wait for ff
	first5min = 1
	i = 0
	while i < 32:
		if i < 2:
			time.sleep(300)
			print("5 min")
		else:
			time.sleep(10)
			# print("30 sec")

		WindowProperty.bringFront(play.hwnd)
	
		if first5min:
			optionButton = pyautogui.locateCenterOnScreen(Images.optionBtn, region=play.rect, confidence=0.7)
			if optionButton:
				pyautogui.moveTo(optionButton)
				pyautogui.mouseDown(optionButton,duration=1.0)
				pyautogui.mouseUp(optionButton)
			first5min = 0
	
		ff1Button = pyautogui.locateCenterOnScreen(Images.ff1Btn, region=play.rect)
		if ff1Button:
			pyautogui.mouseDown(ff1Button,duration=1.0)
			pyautogui.mouseUp(ff1Button)
			time.sleep(1)
			ff2Button = pyautogui.locateCenterOnScreen(Images.ff2Btn, region=play.rect, confidence=0.9)
			if ff2Button:
				pyautogui.moveTo(ff2Button)
				pyautogui.mouseDown(ff2Button,duration=1.5)
				pyautogui.mouseUp(ff2Button)
				break
		i = i + 1
	
	time.sleep(10)
	WindowProperty.bringFront(client.hwnd)

	# quest confirm
	questConfirmButton = pyautogui.locateCenterOnScreen(Images.questConfirmBtn, region=client.rect, confidence=0.9)
	while questConfirmButton:
		pyautogui.click(questConfirmButton)
		print("Click quest confirm")
		time.sleep(5)
		questConfirmButton = pyautogui.locateCenterOnScreen(Images.questConfirmBtn, region=client.rect, confidence=0.9)

	# again 
	againButton = pyautogui.locateCenterOnScreen(Images.againBtn, region=client.rect, confidence=0.8)
	if againButton:
		pyautogui.click(againButton)
		pyautogui.moveTo(1,1)
		time.sleep(5)
	else:
		takeScreen(cwd)

# game start
#play = WindowProperty('league of legends (tm) client')
#print(play.rect)


#matchButton = pyautogui.locateCenterOnScreen(Images.matchBtn, region=client.rect)
#if matchButton:
#	pyautogui.click(matchButton)
#
#acceptButton = None
#time.sleep(5)
#while acceptButton == None:
#	acceptButton = pyautogui.locateCenterOnScreen(Images.acceptBtn, region=client.rect, confidence=0.7)
#	print("wait 5 sec")
#	time.sleep(5)
#
#if acceptButton:
#	pyautogui.click(acceptButton)

#play = WindowProperty('league of legends (tm) client')
#while play.rect == None:
#	time.sleep(5)
#	play = WindowProperty('league of legends (tm) client')
#
#print(play.rect)
#
#WindowProperty.bringFront(play.hwnd)
#
#
#
#optionButton = pyautogui.locateCenterOnScreen(Images.optionBtn, region=play.rect, confidence=0.7)
#if optionButton:
#	pyautogui.moveTo(optionButton)
#	pyautogui.mouseDown(optionButton,duration=1.0)
#	pyautogui.mouseUp(optionButton)
#else:
#	print('fail')
#
#ff1Button = pyautogui.locateCenterOnScreen(Images.ff1Btn, region=play.rect)
#if ff1Button:
#	pyautogui.mouseDown(ff1Button,duration=1.0)
#	pyautogui.mouseUp(ff1Button)
#	time.sleep(1)
#	ff2Button = pyautogui.locateCenterOnScreen(Images.ff2Btn, region=play.rect)
#	if ff2Button:
#		pyautogui.mouseDown(ff2Button,duration=1.0)
#		pyautogui.mouseUp(ff2Button)
		


#ff1Button = pyautogui.locateCenterOnScreen(Images.ff1Btn, region=play.rect)
#if ff1Button:
#	pyautogui.moveTo(ff1Button)


#first5min = TRUE
#i = 0
#while i < 2:
#	time.sleep(300)
#	WindowProperty.bringFront(play.hwnd)
#	if first5min:
#		pyautogui.press('esc')
#		first5min = FALSE
#	ff1Button = pyautogui.locateCenterOnScreen(Images.ff1Btn, region=play.rect)
#	if ff1Button:
#		pyautogui.click(ff1Button)
#		time.sleep(1)
#		ff2Button = pyautogui.locateCenterOnScreen(Images.ff2Btn, region=play.rect)
#		if ff2Button:
#			pyautogui.click(ff2Button)
#			break
#	i++
#
#while 1:
#	time.sleep(60)
#	WindowProperty.bringFront(play.hwnd)
#	if first5min:
#		pyautogui.press('esc')
#		first5min = FALSE
#	ff1Button = pyautogui.locateCenterOnScreen(Images.ff1Btn, region=play.rect)
#	if ff1Button:
#		pyautogui.click(ff1Button)
#		time.sleep(1)
#		ff2Button = pyautogui.locateCenterOnScreen(Images.ff2Btn, region=play.rect)
#		if ff2Button:
#			pyautogui.click(ff2Button)
#			break
import pyautogui
import keyboard

import window

import time
import threading
import logging
import datetime
import os

# can create a thread to play TFT automatically
class PlayTFT(threading.Thread):
	def __init__(self, logger, images, cwd):
		threading.Thread.__init__(self)
		self.logger = logger
		self.images = images
		self.cwd = cwd
		self.daemon = True
		self.timesLeft = 1
		self.stopAfterTimes = False
		self.totalTimes = 0
		self.logger.info("A thread to play TFT is initialized")

	# stop the run after running a specific time
	def stopAfter(self, times):
		if not self.stopAfterTimes:
			self.stopAfterTimes = True
			self.timesLeft = times
			self.logger.info("Turn Stop after times on, times: %d" % times)
		else:
			self.logger.info("Stop after times has already been enabled")
			self.logger.info("Current times left is %d" % self.timesLeft)

	# take screen shot when unexpect stuff happens
	def takeScreen(self):
		# get time stamp
		dtNow = datetime.datetime.now()
		timestamp = dtNow.strftime("%Y%m%d-%H%M%S")
		fileName = "screen_{id}.png".format(id = timestamp)
		self.logger.info("Take screenshot: %s" % fileName)
		pyautogui.screenshot( os.path.join(self.cwd, fileName) )

	# locate with retry times
	def locate(self, image, region, confidence, retryTimes):
		i = 0
		while i < retryTimes:
			result = pyautogui.locateCenterOnScreen(image, region=region, confidence=confidence)
			if result:
				return result
			i += 1
		return None

	def run(self):
		while self.timesLeft > 0:
			self.totalTimes += 1
			self.logger.info("===== loop %d =====" % self.totalTimes)

			client = window.LeagueClient()
			while not (hasattr(client, 'hwnd')):
				client = window.LeagueClient()

			self.logger.info(client.rect)
			client.bringFront()
			time.sleep(1)

			# start a match
			matchButton = pyautogui.locateCenterOnScreen(self.images.matchBtn, region=client.rect, confidence=0.9)
			if matchButton:
				pyautogui.click(matchButton)
				self.logger.info("click match")
			else:
				self.logger.info("Fail to locate match button, take screenshot.")
				self.takeScreen()
				self.logger.info("Run stops at loop %d encountering unexpect situation." % self.totalTimes)
				return
			
			# accept a match, might need to click accept multiple times
			play = window.LeagueGame()
			while not (hasattr(play, 'hwnd')):	
				self.logger.info("wait 3 sec")
				time.sleep(3)
				acceptButton = pyautogui.locateCenterOnScreen(self.images.acceptBtn, region=client.rect, confidence=0.7)
				if acceptButton:
					pyautogui.click(acceptButton)
				play = window.LeagueGame()
						
			# wait for game window fully initialized
			while not (hasattr(play, 'rect')) or play.rect[2] == 1:
				time.sleep(5)
				play = window.LeagueGame()
				
			self.logger.info(play.rect)
			play.bringFront()
			
			# wait for ff totally about 15 minutes
			first5min = 1
			i = 0
			while i < 32:
				if i < 2:
					time.sleep(300)
					self.logger.info("5 min")
				else:
					time.sleep(10)

				play.bringFront()

				pyautogui.click(x=play.rect[0]+5, y=play.rect[1]+5)

				# type /ff command
				keyboard.press_and_release('enter')
				time.sleep(2)
				keyboard.write('/ff')
				keyboard.press_and_release('enter')
				time.sleep(1)
				ff2Button = self.locate(self.images.ff2Btn, play.rect, 0.9, 5)
				if ff2Button:
					j = 0
					while j < 3:
						pyautogui.moveTo(ff2Button)
						pyautogui.mouseDown(ff2Button, duration=1.5)
						pyautogui.mouseUp(ff2Button)
						j += 1
					break
				elif i % 15 == 0 and i != 0:
					self.logger.info("Unable to locate ff2 button, take screenshot.")
					self.takeScreen()
				i += 1

			# wait game window gone
			while hasattr(play, 'hwnd'):
				self.logger.info("Game window still exists, wait 10 seconds.")
				time.sleep(10)
				play = window.LeagueGame()
			
			client.bringFront()

			# quest confirm
			questConfirmButton = pyautogui.locateCenterOnScreen(self.images.questConfirmBtn, region=client.rect, confidence=0.9)
			while questConfirmButton:
				pyautogui.click(questConfirmButton)
				self.logger.info("Click quest confirm")
				time.sleep(5)
				questConfirmButton = pyautogui.locateCenterOnScreen(self.images.questConfirmBtn, region=client.rect, confidence=0.9)

			# again 
			againButton = pyautogui.locateCenterOnScreen(self.images.againBtn, region=client.rect, confidence=0.8)
			if againButton:
				pyautogui.click(againButton)
				# pyautogui.moveTo(1,1)
				time.sleep(5)
			else:
				self.logger.info("Fail to locate again button, take screenshot.")
				self.takeScreen()
				self.logger.info("Run stops at loop %d encountering unexpect situation." % self.totalTimes)
				return

			if self.stopAfterTimes: 
				self.timesLeft -= 1
	
		self.logger.info("Run stops, total loops: %d" % self.totalTimes)


# end of class PlayTFT
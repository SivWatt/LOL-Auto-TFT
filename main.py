import robot
import images
import win32api

import logging
import os
import sys
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext

###########################################################
# Class definitions:

# logging handler to print log in UI text field
class TextHandler(logging.Handler):
	def __init__(self, text):
		logging.Handler.__init__(self)
		self.text = text
		self.setFormatter(logging.Formatter("%(asctime)s - %(message)s", "%m-%d %H:%M:%S"))

	def emit(self, record):
		msg = self.format(record)
		def append():
			self.text.configure(state='normal')
			self.text.insert(tk.END, msg + '\n')
			self.text.configure(state='disabled')
			self.text.yview(tk.END)
		self.text.after(0, append)
# end of class TextHandler

# GUI implement via tkinter
class Application(tk.Frame):
	def __init__(self):
		self.cwd = os.path.dirname(sys.argv[0]) if os.path.dirname(sys.argv[0]) != "" else "."

		# images
		self.images = images.MatchingImages(self.cwd)

		# logger 
		self.logger = logging.getLogger()
		self.logger.level = logging.INFO

		# UI
		window = tk.Tk()
		super().__init__(window)
		self.master = window
		window.title('水水牌掛戰棋')
		window.iconbitmap( os.path.join(self.cwd, 'image', 'rsc', 'window.ico') )
		window.configure(background='white')

		# if multiple monitors detected, create window in second monitor
		monitors = win32api.EnumDisplayMonitors()
		if len(monitors) > 1:
			# monitor[1] = (<handle>, <handle>, (startX, startY, w, h))
			window.geometry("+{x}+500".format(x = monitors[1][2][0]))
		else:
			window.geometry("+0+500")
		
		topFrame = ttk.Frame(window)
		topFrame.pack()
		midFrame = ttk.Frame(window)
		midFrame.pack()
		botFrame = ttk.Frame(window)
		botFrame.pack(side=tk.BOTTOM)

		# top frame
		st = scrolledtext.ScrolledText(topFrame, state='disabled')
		st.pack(side=tk.TOP)
		textHandler = TextHandler(st)
		self.logger.addHandler(textHandler)

		# middle frame
		startStyle = ttk.Style()
		startStyle.configure('Start.TButton', foreground='green', background='green')
		startButton = ttk.Button(midFrame, text='Start', style='Start.TButton', command=self.start )
		startButton.pack(side=tk.LEFT)

		stopStyle = ttk.Style()
		stopStyle.configure('Stop.TButton', foreground='red', background='red')
		stopAfterThisButton = ttk.Button(midFrame, text='Stop after this run', style='Stop.TButton', command=self.stopAfterThis)
		stopAfterThisButton.pack(side=tk.LEFT)
		stopAfterNButton = ttk.Button(midFrame, text='Stop after n runs', style='Stop.TButton', command=self.stopAfterN)
		stopAfterNButton.pack(side=tk.LEFT)
		
		nLabel = ttk.Label(midFrame, text='n: ')
		nLabel.pack(side=tk.LEFT)

		self.timesBox = ttk.Spinbox(midFrame, from_=1, to=100, width=5)
		self.timesBox.set(1)
		self.timesBox.pack(side=tk.LEFT)

		# bottom frame 
		quitStyle = ttk.Style()
		quitStyle.configure('Quit.TButton', foreground='black')
		quitBotton = ttk.Button(botFrame, text='Stop and Exit', style='Quit.TButton', command=self.master.destroy)
		quitBotton.pack()

		self.pack()

	# start a playing thread
	def start(self):
		if not (hasattr(self, 't')) or not (self.t.is_alive()):
			self.t = robot.PlayTFT(self.logger, self.images, self.cwd)
			self.t.start()
		elif self.t.is_alive():
			self.logger.info("A playing thread already exists")

	# stop current playing thread after this run
	def stopAfterThis(self):
		if hasattr(self, 't'):
			if not self.t.stopAfterTimes:
				self.logger.info("Stop after this game.")
				self.t.stopAfter(1)
			else:
				self.logger.info("Unable to stop: a stop button has been pressed.")
		else:
			self.logger.info("Unable to stop: there isn't a game playing.")

	# stop current playing thread after N runs
	def stopAfterN(self):
		if hasattr(self, 't'):
			if not self.t.stopAfterTimes:
				times = self.timesBox.get()
				self.logger.info("Stop after %s games." % times)
				self.t.stopAfter(int(times))
			else:
				self.logger.info("Unable to stop: a stop button has been pressed.")
		else:
			self.logger.info("Unable to stop: there isn't a game playing.")

# end of class Application

###########################################################
# main script starts:
if __name__ == '__main__':
	app = Application()
	app.mainloop()
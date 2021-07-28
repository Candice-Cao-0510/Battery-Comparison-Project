import matplotlib.pyplot as plt
import matplotlib.animation as animation
import tkinter as tk
import sqlite3
import pandas as pd
import numpy as np 
import seaborn as sns
import time
import sys

import constants
from bk_precision8600 import BKP8600
from creating_files import createCSVFiles, createDBFiles, createPNG

class CC_Plot:
	def _init_(self, instrument, constantCurrent, targetVoltage):
		self.constantCurrent = constantCurrent
		self.targetVoltage = targetVoltage
		self.timeInSec = 0
		self.dbFileName = createDBFiles("cc", constantCurrent, targetVoltage)
		self.conn = sqlite3.connect(self.dbFileName)
		self.cur = self.conn.cursor()
		self.inst = instrument

		#initiating plots
		"""
		sns.set_theme(style="darkgrid")
		self.fig, (self.ax1, self.ax2) = plt.subplots(nrows=2, ncols=1)
		plt.subplots_adjust(hspace=0.5)
		self.ax1.spines['right'].set_color(None)
		self.ax1.spines['top'].set_color(None)
		self.ax2.spines['right'].set_color(None)
		self.ax2.spines['top'].set_color(None)
		"""

		#start program
		self.cc_create_table()
		self.cc_set_instrument()
		self.inst.inputOn()
		self.initialVoltage = self.initial_state()
		self.read_and_store_data(self.initialVoltage)
		#self.ani = animation.FuncAnimation(self.fig, self.animate_plot_data, interval=constants.FRAME_INTERVAL)
		#plt.show()

		#closing database reading and turn off instrument
		self.inst.inputOff()
		self.cc_close_db()
		#plt.close('all')

	def cc_create_table(self):
		#get the count of tables with the name
		self.cur.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='tcvTable' ''')

		#if the count is 1, then table exists
		if (self.cur.fetchone()[0] == 1):
			print('Table exists.')
			ifContinue = input("Would you like to start a fresh new table? (y/n)")
			while (True):
				if (ifContinue[0] == "y" or ifContinue[0] == "Y"):
					self.cur.execute("DROP TABLE tcvTable")
					self.cur.execute("""Create Table tcvTable (
							timeInSec INTEGER,
							current REAL,
							voltage REAL
							)""")
					break
				elif (ifContinue[0] == "n" or ifContinue[0] == "N"):
					print("Program terminating now ~")
					return
				else:
					ifContinue = input("unable to read your input, would you like to start a new table? (please answer with 'y' or 'n')")
		else:
			self.cur.execute("""Create Table tcvTable (
							timeInSec INTEGER,
							current REAL,
							voltage REAL
							)""")

	def cc_close_db(self):
		self.conn.commit()
		self.conn.close()

	def cc_set_instrument(self):
		self.inst.reset()
		self.inst.setCurrentRange(str(constants.CURRENT_RANGE))
		self.inst.setCurrent(str(self.constantCurrent))

	def initial_state(self):
		initialVoltage = float(self.inst.getVoltage())
		opc = self.inst.getOPC()
		time.sleep(constants.SLEEP_TIME)

		return str(initialVoltage)

	def read_and_store_data(self, voltageReading):

		while (voltageReading >= self.targetVoltage):
			tik = time.perf_counter()

			#get the current voltage and current reading
			voltageReading = float(self.inst.getVoltage())
			currentReading = float(self.inst.getCurrent())
			opc = self.inst.getOPC()

			self.cur.execute("INSERT INTO tcvTable VALUES (:timeInSec, :current, :voltage)", {'timeInSec': self.timeInSec, 'current': currentReading, 'voltage': voltageReading})
			
			self.cur.execute("SELECT * from tcvTable")
			table = self.cur.fetchall()
			
			tcvDF = pd.DataFrame(table, columns=["Time", "Current", "Voltage"])
			print(tcvDF)
			print("\n")

			tok = time.perf_counter()
			while (tok - tik < constants.TIME_INTERVAL):
				tok = time.perf_counter()

			#update time to be stored in database
			self.timeInSec += round(tok - tik, 2)

"""
	def animate_plot_data(self, i):
		tik = time.perf_counter()

		#get the current voltage and current reading
		voltageReading = float(self.inst.getVoltage())
		currentReading = float(self.inst.getCurrent())
		opc = self.inst.getOPC()

		if (voltageReading < self.targetVoltage):
			self.ani.event_source.stop()
			plot_picture = createPNG("cc", self.constantCurrent, self.targetVoltage)
			plt.savefig(plot_picture)
			return

		self.cur.execute("INSERT INTO tcvTable VALUES (:timeInSec, :current, :voltage)", {'timeInSec': self.timeInSec, 'current': currentReading, 'voltage': voltageReading})
		
		self.cur.execute("SELECT * from tcvTable")
		table = self.cur.fetchall()
		
		tcvDF = pd.DataFrame(table, columns=["Time", "Current", "Voltage"])
		print(tcvDF)
		print("\n")

		self.ax1.clear()
		self.ax2.clear()

		self.ax1.set_title("Constant Current Starting at Voltage %sV: \n Current Vs. Time" % self.initialVoltage)
		sns.lineplot(x="Time", y="Current", data=tcvDF, ax=self.ax1)

		self.ax2.set_title("Voltage Vs. Time")
		sns.lineplot(x="Time", y="Voltage", data=tcvDF, ax=self.ax2)

		tok = time.perf_counter()
		while (tok - tik < constants.TIME_INTERVAL):
			tok = time.perf_counter()

		#update time to be stored in database
		self.timeInSec += (round(tok - tik, 2) + constants.FRAME_INTERVAL_IN_SEC)
"""

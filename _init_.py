import pyvisa
import time
import sqlite3
import matplotlib.pyplot as plt
import numpy as np 

from creating_files import createCSVFiles, createDBFiles
from bk_precision8600 import BKP8600

class INIT:
	def _init_(self, device_name=None):
		self.rm = pyvisa.ResourceManager()
		self.device_count = 0
		self.inst = BKP8600()
		self.timeInterval = []
		self.voltageChangeData = []
		self.currentChangeData = []

		lst = self.rm.list_resources()
		tempInstrument = self.rm.open_resource(lst[0])
		self.rm.timeout = 8000
		idn = tempInstrument.query("*IDN?")
		opc = tempInstrument.query("*OPC?")
		self.inst._init_(tempInstrument, idn)

	def constant_current(self, constantCurrent, targetVoltage):

		#self.inst.inputOff()
		#[currentFileName, voltageFileName, timeFileName] = self.createCSVFiles("cc", constantCurrent, targetVoltage)
		dbFileName = createDBFiles("cc", constantCurrent, targetVoltage)

		""" if fileName already exists, notify user and ask if want to append, replace or terminate """
		""" now assume it does not exist and we are building from scratch """

		#connecting to sqlite database
		conn = sqlite3.connect(dbFileName)
		cur = conn.cursor()

		#get the count of tables with the name
		cur.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='tcvTable' ''')

		#if the count is 1, then table exists
		if (cur.fetchone()[0] == 1):
			print('Table exists.')
			while (True):
				ifContinue = input("Would you like to start a fresh new table? (y/n)")
				if (ifContinue[0] == "y" or ifContinue[0] == "Y"):
					cur.execute("DROP TABLE tcvTable")
					cur.execute("""Create Table tcvTable (
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
			cur.execute("""Create Table tcvTable (
							timeInSec INTEGER,
							current REAL,
							voltage REAL
							)""")


		self.inst.reset()
		self.inst.setCurrentRange('0.1')
		self.inst.setCurrent(str(constantCurrent))

		#initialize time to be 0 second
		timeInSec = 0
		#initialize voltageReading
		voltageReading = float(self.inst.getVoltage())
		#initialize currentReading
		currentReading = float(self.inst.getCurrent())

		#the intrument starts to drain the battery in a constant current
		self.inst.inputOn()

		#let the thread sleep for 1 second to avoid rushing to append initialized data into the arrays
		time.sleep(1)

		while (voltageReading >= targetVoltage):	
			tik = time.perf_counter()

			#get the current voltage and current reading
			voltageReading = float(self.inst.getVoltage())
			currentReading = float(self.inst.getCurrent())
			
			cur.execute("INSERT INTO tcvTable VALUES (:timeInSec, :voltage, :current)", {'timeInSec': timeInSec, 'voltage': voltageReading, 'current': currentReading})
			
			cur.execute("SELECT timeInSec from tcvTable")
			timeTable = cur.fetchall()

			cur.execute("SELECT voltage from tcvTable")
			voltageTable = cur.fetchall()

			cur.execute("SELECT current from tcvTable")
			currentTable = cur.fetchall()

			print(timeTable)
			print(voltageTable)
			print(currentTable)

			tok = time.perf_counter()
			while (tok - tik < 5.0):
				tok = time.perf_counter()

			#update time to be stored in database
			timeInSec += int(tok - tik)

		#turn the input off
		self.inst.inputOff()
		conn.commit()
		conn.close()

bus = INIT()
bus._init_("bk_precision8600")
bus.constant_current(0.1, 7.5)

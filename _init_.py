import pyvisa
import time
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
		self.inst._init_(tempInstrument, idn)

	def constant_current(self, targetVoltage):
		self.inst.reset()

		self.inst.setCurrentRange('1')
		self.inst.setCurrent('0.1')

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
			#get the current voltage and current reading
			voltageReading = float(self.inst.getVoltage())
			currentReading = float(self.inst.getCurrent())

			#print("time is ", timeInSec, " voltage is ",voltageReading," current is ",currentReading)
			
			#append new readings to timeInterval, voltageChangeData and currentChangeData arrays
			self.timeInterval.append(timeInSec)
			self.voltageChangeData.append(voltageReading)
			self.currentChangeData.append(currentReading)

			#let the reading stop for 5 seconds
			time.sleep(5)

			#update time, since we let the timer sleep for 5 seconds each time
			timeInSec += 5

		#turn the input off
		self.inst.inputOff()

		print(self.timeInterval)
		print(self.voltageChangeData)
		print(self.currentChangeData)


bus = INIT()
bus._init_("bk_precision8600")
bus.constant_current(7.5)
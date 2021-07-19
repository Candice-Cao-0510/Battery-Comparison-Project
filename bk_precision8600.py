import pyvisa
import time

"""
written by Candice Cao
"""

class BKP8600:
	def _init_(self, visa_instance, identity):
		self.inst = visa_instance
		self.name = "BK Precision 8600"
		self.idn = identity
		self.type = "electronic load"

	def getIdentifier(self):
		self.idn = self.inst.query("*IDN?")
		return self.idn

# reset, input on (start draining battery), input off (stop draining battery)
	def reset(self):
		self.inst.write('rst')

	def inputOn(self):
		self.inst.write('inp 1')

	def inputOff(self):
		self.inst.write('inp 0')

# get & set current, voltage, resistance, power range 
	
	#set constant current range (MAX)
	def setCurrentRange(self, currentRange):
		self.inst.write('current:range ' + currentRange)

	#query constant current range
	def getCurrentRange(self):
		return(self.inst.query('current:range?'))

	#set constant voltage range (MIN)
	def setVoltageRange(self, voltageRange):
		self.inst.write('voltage:range ' + voltageRange)

	#query constant voltage range
	def getVoltageRange(self):
		return(self.inst.query('voltage:range?'))

	#set constant resistance range (MAX)
	def setResistanceRange(self, resistanceRange):
		self.inst.write('resistance:range ' + resistanceRange)

	#query constant resistance range
	def getResistanceRange(self):
		return(self.inst.query('resistance:range?'))

	#set power protection delay time (3)
	def setPowerRange(self, powerRange):
		self.inst.write('power:range ' + powerRange)

	#query power protection delay time
	def getPowerRange(self):
		return(self.inst.query('power:range?'))

# set & get current, voltage, resistance, power

	#set current when in constant current mode
	def setCurrent(self, current):
		self.inst.write('current ' + current)

	#get current current
	def getCurrent(self):
		return(self.inst.query(':measure:current?'))

	#set voltage when in constant voltage mode
	def setVoltage(self, voltage):
		self.inst.write('voltage ' + voltage)

	#get current voltage
	def getVoltage(self):
		return(self.inst.query(':measure:voltage?'))

	#set resistance when in constant resistance mode
	def setResistance(self, resistance):
		self.inst.write('resistance ' + resistance)

	#get current resistance
	def getResistance(self):
		return(self.inst.query('resistance?'))

	#set power when in constant power mode
	def setPower(self, power):
		self.inst.write('power ' + power)

	#get current power
	def getPower(self):
		return(self.inst.query('power?'))

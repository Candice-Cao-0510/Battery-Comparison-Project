import pyvisa
import time
import sqlite3
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pandas as pd
import numpy as np 
import seaborn as sns

from creating_files import createCSVFiles, createDBFiles
from bk_precision8600 import BKP8600
from cc_real_time_plot import CC_Plot

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
		constant_current_plot = CC_Plot()
		constant_current_plot._init_(self.inst, constantCurrent, targetVoltage)
		

bus = INIT()
bus._init_("bk_precision8600")
bus.constant_current(0.01, 7.0)

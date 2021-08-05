import sqlite3
import pandas as pd
import numpy as np 
import os

#creating data files for testing usage
def createCSVTestingFiles(fileName):
	csvFileName = ("data_files/%s.csv" % fileName)
	return csvFileName

def writingToCSVFile(csvFileName, dbFileName):
	csvFile = open(csvFileName, "w")
	conn = sqlite3.connect(dbFileName)
	cur = conn.cursor()
	cur.execute("SELECT * FROM tcvTable")
	table = cur.fetchall()
	tcvDF = pd.DataFrame(table, columns=["Time", "Current", "Voltage"])
	tcvDF.to_csv(csvFileName, index=False, encoding='utf-8')

fileName = "cc_0.05A_target4.5V"
dbFileName = "/Users/candicecao/Downloads/Battery_Comparison_Project/Battery-Comparison-Project/dbDataFiles/cc_0.05A_target4.5V.db"
csvFileName = createCSVTestingFiles(fileName)
writingToCSVFile(csvFileName, dbFileName)


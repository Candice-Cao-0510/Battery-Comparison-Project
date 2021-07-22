def createCSVFiles(mode, constantValue, changingVariableTarget):
	constant = ""
	target = ""

	if (mode == "cc"):
		constant = ("%sA" % str(constantValue))
		target= ("%sV" % str(changingVariableTarget))
	elif (mode == "cr"):
		constant = ("%sR" % str(constantValue))
		target= ("%sV" % str(changingVariableTarget))
	elif (mode == "cp"):
		constant = ("%sW" % str(constantValue))
		target= ("%sV" % str(changingVariableTarget))
	else:
		print("undefined mode")
		return None

	currentFileName = ("csvDataFiles/%s_%s_target%s_current.csv" % (mode, constant, target))
	voltageFileName = ("csvDataFiles/%s_%s_target%s_voltage.csv" % (mode, constant, target))
	timeFileName = ("csvDataFiles/%s_%s_target%s_time.csv" % (mode, constant, target))
	"""currentFile = open(currentFileName, "w")
	voltageFile = open(voltageFileName, "w")
	timeFile = open(timeFileName, "w")"""
	return [currentFileName, voltageFileName, timeFileName]

def createDBFiles(mode, constantValue, changingVariableTarget):
	constant = ""
	target = ""

	if (mode == "cc"):
		constant = ("%sA" % str(constantValue))
		target= ("%sV" % str(changingVariableTarget))
	elif (mode == "cr"):
		constant = ("%sR" % str(constantValue))
		target= ("%sV" % str(changingVariableTarget))
	elif (mode == "cp"):
		constant = ("%sW" % str(constantValue))
		target= ("%sV" % str(changingVariableTarget))
	else:
		print("undefined mode")
		return None

	fileName = ("dbDataFiles/%s_%s_target%s.db" % (mode, constant, target))

	return fileName
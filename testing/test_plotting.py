import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns

def plotting_data(tcvaDF, initialVoltage, constantCurrent, targetVoltage):
	sns.set_theme(style="darkgrid")
	fig, (ax1, ax2, ax3) = plt.subplots(nrows=3, ncols=1, sharex=True)

	ax1.set_title("Constant Current Starting at Voltage %sV: \n Current Vs. Time" % initialVoltage)
	sns.lineplot(x="Time", y="Current", data=tcvaDF, ax=ax1)

	ax2.set_title("Voltage Vs. Time")
	sns.lineplot(x="Time", y="Voltage", data=tcvaDF, ax=ax2)

	ax3.set_title("Ampere Hour Vs. Time")
	sns.lineplot(x="Time", y="AmpHour", data=tcvaDF, ax=ax3)

	plot_picture = "testing_plots/cc_0.05A_target4.5V.png"
	plt.savefig(plot_picture)

def testing_plotting_data_function(csvFileName):
	tcvaDF = pd.read_csv(csvFileName)
	plotting_data(tcvaDF, "6.43297", "0.05", "4.5")

testing_plotting_data_function("data_files/cc_0.05A_target4.5V.csv")

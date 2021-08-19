"""
Writen by Candice Cao

This module is for plotting data using matplotlib and seaborn

"""

import seaborn as sns
import matplotlib.pyplot as plt

from creating_files import create_png

def plotting(mode, df, start_voltage, end_voltage, is_ah, date_time, time_elapsed):
    """ plotting plots dataframes """

    x_axis = ""
    if time_elapsed / 3600 > 1:
        x_axis = "TimeInHour"
    else:
        x_axis = "TimeInSec"

    sns.set_theme(style="darkgrid")
    fig, axs = plt.subplots(nrows=3, ncols=2, sharex=True)
    fig.suptitle("%s with Start Voltage %sV and Ending Voltage %sV" % (mode, start_voltage, end_voltage), fontsize=16)
    fig.set_size_inches(9.5, 8)

    axs[0, 0].set_title("Current Vs. Time")
    sns.lineplot(x=x_axis, y="Current", data=df, ax=axs[0, 0])

    axs[1, 0].set_title("Voltage Vs. Time")
    sns.lineplot(x=x_axis, y="Voltage", data=df, ax=axs[1, 0])

    axs[2, 0].set_title("Resistance Vs. Time")
    sns.lineplot(x=x_axis, y="Resistance", data=df, ax=axs[2, 0])

    axs[0, 1].set_title("Power Vs. Time")
    sns.lineplot(x=x_axis, y="Power", data=df, ax=axs[0, 1])

    if is_ah:
        axs[1, 1].set_title("Ampere Hour Vs. Time")
        sns.lineplot(x=x_axis, y="AmpHour", data=df, ax=axs[1, 1])
    else:
        axs[1, 1].set_title("Milli Ampere Hour Vs. Time")
        sns.lineplot(x=x_axis, y="milliAmpHour", data=df, ax=axs[1, 1])

    axs[2, 1].set_title("Watt Hour Vs. Time")
    sns.lineplot(x=x_axis, y="WattHour", data=df, ax=axs[2, 1])

    plot_picture = create_png(date_time)
    plt.savefig(plot_picture)

    return plot_picture

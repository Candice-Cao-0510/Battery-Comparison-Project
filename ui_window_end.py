"""
Written by Candice Cao

ending user interface that displays the time elapsed and plots
"""
import io
import os
from PIL import Image
import PySimpleGUI as sg

#from ui_window_intro import intro_ui
from plotting import plotting

# ----------- program starts
def end_ui(df, mode, start_voltage, end_voltage, date_time, time_elapsed):
    """ main method for ending user interface """

    # ----------- Set theme
    sg.theme('SandyBeach')

    # ------------ Set font
    font_l = ("Times New Roman", 20)
    font_m = ("Times New Roman", 18)

    # ----------- variables
    is_ah = True
    plotname = ""
    calculated_time = calculate_time(time_elapsed)

    # ----------- Create the layouts this Window will display -----------
    layout1 = [[sg.Text('Test completed!', font=font_l)],
               [sg.Text('       Time elapsed:           ', font=font_m),
                sg.Text(calculated_time, size=(400, 1), font=font_m,
                text_color='teal', key='-TIME_ELAPSED-')],
               [sg.Button('Get plots', font=font_m)]]

    layout2 = [[sg.Text('Would you like to use Ah or milli Ah?', font=font_m),
                sg.Button('Ah', font=font_m), sg.Button('mAh', font=font_m),
                sg.Text('               '), sg.Button('Display plots', font=font_m)],
                [sg.Image(key='-PLOTS-')],
                [sg.Text(size=(500, 3), font=font_m, text_color='teal', key='-SAVED_FILES-')],
                [sg.Button('Exit', font=font_m)]]

    # ----------- Create actual layout using Columns and a row of Buttons
    layout = [[sg.Column(layout1, key='-COL1-'), sg.Column(layout2, visible=False, key='-COL2-')]]

    window = sg.Window('Battery Test Plotting', layout, size=(800, 800))

    layout = 1  # The currently visible layout

    while True:
        event, values = window.read()
        if (event == sg.WIN_CLOSED or event == 'Exit'):  # if the X button clicked, just exit
            break
        if event == 'Get plots':
            window[f'-COL{layout}-'].update(visible=False)
            layout = layout + 1
            window[f'-COL{layout}-'].update(visible=True)

        if event == 'Ah':
            is_ah = True
        if event == 'mAh':
            is_ah = False

        if event == 'Display plots':
            plotname = plotting(mode, df, start_voltage, end_voltage, is_ah, date_time, time_elapsed)

            if os.path.exists(plotname):
                image = Image.open(plotname)
                image.thumbnail((700, 700))
                bio = io.BytesIO()
                image.save(bio, format="PNG")
                window['-PLOTS-'].update(data=bio.getvalue())
            window['-SAVED_FILES-'].update("The displayed plot and corresponding csv files are saved under folders 'plot_screenshots' and\n 'csvDataFiles'!")

    window.close()

def calculate_time(time_elapsed_in_sec):
    """ calculate time in seconds to time in days, hours, minutes, seconds """
    second = time_elapsed_in_sec % 60
    minute = time_elapsed_in_sec // 60
    hour = minute // 60
    day = hour // 24
    minute = minute % 60
    hour = hour % 24
    return "%d days %d hours %d minutes %d seconds" % (day, hour, minute, second)

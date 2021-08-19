"""
Written by Candice Cao

This module is the intro user interface that records all user input information
(battery info, mode, targe voltage, etc), and at the end of the intro, it triggers
the another python function that starts to read from the instrument and write to
database.
"""

import PySimpleGUI as sg

from _init_ import TEST
import constants
import drop_downs
import record_log

def intro_ui():
    """ main intro ui function """

    # ----------- Set theme
    sg.theme('SandyBeach')

    # ------------ Set font
    font_l = ("Times New Roman", 20)
    font_m = ("Times New Roman", 18)

    # ----------- Initialize equipment
    record_log.initialize_record_log()
    bus = TEST()
    bus._init_()
    bus.set_equipment_meta()
    equipment_info = bus.equipment_meta

    # ----------- collect battery info
    battery_info = []
    start = False

    # ----------- variables
    mode = ""

    # ----------- Create the layouts this Window will display -----------
    layout1 =  [[sg.Text('Please check the equipment information \n\n', font=font_m)],
                [sg.Text('       Equipment brand:                ', font=font_m),
                sg.Text(equipment_info[0], size=(20, 1), font=font_m, text_color='teal', key='equipment_brand')],
                [sg.Text('       Equipment model number:         ', font=font_m),
                sg.Text(equipment_info[1], size=(20, 1), font=font_m, text_color='teal', key='equipment_model_number')],
                [sg.Text('       Equipment serial number:        ', font=font_m),
                sg.Text(equipment_info[2], size=(20, 1), font=font_m, text_color='teal', key='equipment_serial_number')],
                [sg.Text('       Equipment software revision:    ', font=font_m),
                sg.Text(equipment_info[3], size=(20, 1), font=font_m, text_color='teal', key='equipment_software_revision')],
                [sg.Text('\n\n')],
                [sg.Button('Incorrect, Reload', font=font_m), sg.Text('      '),
                sg.Button('Correct! Continue', font=font_m), sg.Text('      '),
                sg.Button('Exit', font=font_m)]]

    layout2 = [[sg.Text('Please input battery information', font=font_l)],
               [sg.Text('       Battery brand:                                  ', font=font_m),
                sg.Combo(drop_downs.BATTERY_BRANDS, key='battery_brand', size=(10, 1), font=font_m)],
               [sg.Text('       Battery form factor:                            ', font=font_m),
                sg.Combo(drop_downs.FORM_FACTORS, key='battery_form_factor', size=(10, 1), font=font_m)],
               [sg.Text('       Battery model number:                           ', font=font_m),
                sg.Input(key='battery_model_number', size=(10, 1), font=font_m)],
               [sg.Text('       Battery chemistry type:                         ', font=font_m),
                sg.Combo(drop_downs.CHEMISTRY_TYPES, key='battery_chemistry_type', size=(10, 1), font=font_m)],
               [sg.Text('       Battery nominal voltage:                        ', font=font_m),
                sg.Combo(drop_downs.NOMINAL_VOLTAGE, key='battery_nominal_voltage', size=(10, 1), font=font_m)],
               [sg.Text('       Battery nominal amp hour capacity:              ', font=font_m),
                sg.Input(key='battery_nominal_ah', size=(10, 1), font=font_m)],
               [sg.Text('       Battery nominal watt hour capacity:             ', font=font_m),
                sg.Input(key='battery_nominal_wh', size=(10, 1), font=font_m)],
               [sg.Text('       Battery serial number(if available):            ', font=font_m),
                sg.Input(key='battery_serial_number', size=(10, 1), font=font_m)],
               [sg.Text('       Battery manufaturing date code(if available):   ', font=font_m),
                sg.Input(key='battery_manufacturing_date', size=(10, 1), font=font_m)],
               [sg.Text('       Battery expiration date(if available):          ', font=font_m),
                sg.Input(key='battery_expiration_date', size=(10, 1), font=font_m)],
               [sg.Text('       Battery country of origin:                      ', font=font_m),
                sg.Combo(drop_downs.COUNTRY_OF_ORIGIN, key='battery_coo', size=(10, 1), font=font_m)],
               [sg.Text('       Room temperature(in Celcius):                   ', font=font_m),
                sg.Input(key='room_temperature', size=(10, 1), font=font_m)],
               [sg.Button('Return', font=font_m),
                sg.Button('Continue', font=font_m),
                sg.Button('Exit', font=font_m)]]

    layout3 = [[sg.Text('Please choose a mode\n', font=font_l)],
               [sg.Button('Constant Current', font=font_m)],
               [sg.Button('Constant Resistance', font=font_m)],
               [sg.Button('Constant Power', font=font_m)],
               [sg.Text('\n\n')],
               [sg.Button('Return', font=font_m),
                sg.Button('Continue', font=font_m),
                sg.Button('Exit', font=font_m)]]

    layout4 = [[sg.Text('Constant Current Mode\n\n', font=font_l)],
               [sg.Text('   End Voltage:       ', font=font_m),
                sg.Input(key='end_voltage_cc', size=(10, 1), font=font_m), sg.Text(' V', font=font_m)],
               [sg.Text('   Constant Current:     ', font=font_m),
                sg.Input(key='constant_current', size=(10, 1), font=font_m), sg.Text(' A', font=font_m)],
               [sg.Text('   Sampling Interval:    ', font=font_m),
                sg.Input(key='time_interval_cc', size=(10, 1), font=font_m), sg.Text(' s', font=font_m)],
               [sg.Text(size=(500, 1), font=font_m, text_color='red', key='error_message_cc')],
               [sg.Button('Return', font=font_m),
                sg.Button('Continue', font=font_m),
                sg.Button('Exit', font=font_m)]]

    layout5 = [[sg.Text('Please check the constant current mode settings: \n\n', font=font_m)],
               [sg.Text('   End Voltage:       ', font=font_m),
                sg.Text(size=(5, 1), font=font_m, text_color='teal', key='end_voltage_cc_out'), sg.Text(' V', font=font_m)],
               [sg.Text('   Constant Current:     ', font=font_m),
                sg.Text(size=(5, 1), font=font_m, text_color='teal', key='constant_current_out'), sg.Text(' A', font=font_m)],
               [sg.Text('   Sampling Interval:    ', font=font_m),
                sg.Text(size=(5, 1), font=font_m, text_color='teal', key='time_interval_cc_out'), sg.Text(' s', font=font_m)],
               [sg.Button('Return', font=font_m),
                sg.Button('Start Testing!', font=font_m),
                sg.Button('Exit', font=font_m)]]

    layout6 = [[sg.Text('Constant Resistance Mode\n\n', font=font_l)],
               [sg.Text('   End Voltage:       ', font=font_m),
                sg.Input(key='end_voltage_cr', size=(10, 1), font=font_m), sg.Text(' V', font=font_m)],
               [sg.Text('   Constant Resistance:     ', font=font_m),
                sg.Input(key='constant_resistance', size=(10, 1), font=font_m), sg.Text(' Ohm', font=font_m)],
               [sg.Text('   Sampling Interval:    ', font=font_m),
                sg.Input(key='time_interval_cr', size=(10, 1), font=font_m), sg.Text(' s', font=font_m)],
               [sg.Text(size=(500, 1), font=font_m, text_color='red', key='error_message_cr')],
               [sg.Button('Return', font=font_m),
                sg.Button('Continue', font=font_m),
                sg.Button('Exit', font=font_m)]]

    layout7 = [[sg.Text('Please check the constant resistance mode settings: \n\n', font=font_m)],
               [sg.Text('   End Voltage:       ', font=font_m),
                sg.Text(size=(5, 1), font=font_m, text_color='teal', key='end_voltage_cr_out'), sg.Text(' V', font=font_m)],
               [sg.Text('   Constant Resistance:     ', font=font_m),
                sg.Text(size=(5, 1), font=font_m, text_color='teal', key='constant_resistance_out'), sg.Text(' Ohm', font=font_m)],
               [sg.Text('   Sampling Interval:    ', font=font_m),
                sg.Text(size=(5, 1), font=font_m, text_color='teal', key='time_interval_cr_out'), sg.Text(' s', font=font_m)],
               [sg.Button('Return', font=font_m),
                sg.Button('Start Testing!', font=font_m),
                sg.Button('Exit', font=font_m)]]

    # ----------- Create actual layout using Columns and a row of Buttons
    layout = [[sg.Column(layout1, key='-COL1-'),
                sg.Column(layout2, visible=False, key='-COL2-'),
                sg.Column(layout3, visible=False, key='-COL3-'),
                sg.Column(layout4, visible=False, key='-COL4-'),
                sg.Column(layout5, visible=False, key='-COL5-'),
                sg.Column(layout6, visible=False, key='-COL6-'),
                sg.Column(layout7, visible=False, key='-COL7-')]]

    window = sg.Window('Battery Test', layout, size=(500, 500))

    layout = 1  # The currently visible layout

    while True:
        event, values = window.read()
        if (event == sg.WIN_CLOSED or event == 'Exit' or event[0:4] == 'Exit'):  # if the X button clicked, just exit
            break

        if event == 'Return' or event[0:6] == 'Return':
            window[f'-COL{layout}-'].update(visible=False)
            layout = layout - 1
            window[f'-COL{layout}-'].update(visible=True)

        elif event == 'Correct! Continue':
            window[f'-COL{layout}-'].update(visible=False)
            layout = layout + 1
            window[f'-COL{layout}-'].update(visible=True)

        elif event == 'Incorrect, Reload':
            bus = TEST()
            bus._init_()
            bus.set_equipment_meta()
            equipment_info = bus.equipment_meta

            window['equipment_brand'].update(equipment_info[0])
            window['equipment_model_number'].update(equipment_info[1])
            window['equipment_serial_number'].update(equipment_info[2])
            window['equipment_software_revision'].update(equipment_info[3])

        elif event == 'Constant Current':
            bus.set_mode('Constant Current')
            window[f'-COL{layout}-'].update(visible=False)
            layout = 4
            window[f'-COL{layout}-'].update(visible=True)
            mode = 'cc'

        elif event == 'Constant Resistance':
            bus.set_mode('Constant Resistance')
            window[f'-COL{layout}-'].update(visible=False)
            layout = 6
            window[f'-COL{layout}-'].update(visible=True)
            mode = 'cr'

        elif event == 'Continue' or event[0:8] == 'Continue':
            if layout == 2: #battery info page
                battery_info = [values['battery_brand'],
                                values['battery_form_factor'],
                                values['battery_model_number'],
                                values['battery_chemistry_type'],
                                values['battery_nominal_voltage'],
                                values['battery_nominal_ah'],
                                values['battery_nominal_wh'],
                                values['battery_serial_number'],
                                values['battery_manufacturing_date'],
                                values['battery_expiration_date'],
                                values['battery_coo'],
                                values['room_temperature']]
                bus.set_battery_meta(battery_info)
                window[f'-COL{layout}-'].update(visible=False)
                layout = layout + 1
                window[f'-COL{layout}-'].update(visible=True)

            if layout == 4: #constant current ui page
                if float(values['end_voltage_cc']) < constants.VOLTAGE_LOWER_LIMIT:
                    window['error_message_cc'].update('Error: Voltage is lower than the limit of %f'
                                                        % constants.VOLTAGE_LOWER_LIMIT)

                elif (float(values['constant_current']) <= 0 or float(values['constant_current']) > constants.CURRENT_RANGE):
                    window['error_message_cc'].update('Error: Current is <= 0 or exceeds the limit of %f'
                                                        % constants.CURRENT_RANGE)

                elif float(values['time_interval_cc']) < constants.TIME_INTERVAL:
                    window['error_message_cc'].update('Error: sampling interval can not be less than %f'
                                                        % constants.TIME_INTERVAL)
                else:
                    bus.set_end_voltage(values['end_voltage_cc'])
                    bus.set_constant_var(values['constant_current'])
                    window['error_message_cc'].update('')
                    window[f'-COL{layout}-'].update(visible=False)
                    layout = layout + 1
                    window[f'-COL{layout}-'].update(visible=True)

            if layout == 5: #constant current mode checking page
                window['end_voltage_cc_out'].update(values['end_voltage_cc'])
                window['constant_current_out'].update(values['constant_current'])
                window['time_interval_cc_out'].update(values['time_interval_cc'])

            if layout == 6: #constant resistance ui page
                if float(values['end_voltage_cr']) < constants.VOLTAGE_LOWER_LIMIT:
                    window['error_message_cr'].update('Error: Voltage is lower than the limit of %f'
                                                        % constants.VOLTAGE_LOWER_LIMIT)

                elif float(values['constant_resistance']) < constants.RESISTANCE_LOWER_LIMIT:
                    window['error_message_cr'].update('Error: Resistance is lower than %f'
                                                        % constants.RESISTANCE_LOWER_LIMIT)

                elif float(values['time_interval_cr']) < constants.TIME_INTERVAL:
                    window['error_message_cr'].update('Error: sampling interval can not be less than %f'
                                                        % constants.TIME_INTERVAL)
                else:
                    bus.set_end_voltage(values['end_voltage_cr'])
                    bus.set_constant_var(values['constant_resistance'])
                    window['error_message_cr'].update('')
                    window[f'-COL{layout}-'].update(visible=False)
                    layout = layout + 1
                    window[f'-COL{layout}-'].update(visible=True)

            if layout == 7: #constant resistance mode checking page
                window['end_voltage_cr_out'].update(values['end_voltage_cr'])
                window['constant_resistance_out'].update(values['constant_resistance'])
                window['time_interval_cr_out'].update(values['time_interval_cr'])

        elif (event == 'Start Testing!' or event[0:14] == 'Start Testing!'):
            start = True
            break

    window.close()

    if start:
        bus.store_to_log()
        if mode == 'cc':
            bus.constant_current()
        elif mode == 'cr':
            bus.constant_resistance()

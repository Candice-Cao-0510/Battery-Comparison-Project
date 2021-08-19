""" Written by Candice Cao

CCPlot is for constant current mode: sets end voltage, sets constant current, reads from instrument,
writes to database, creates csv data file and calls the ending user interface
"""

import sqlite3
import time
import pandas as pd

import constants
import errors
from creating_files import create_csv_files, create_db_files
from ui_window_end import end_ui

class CCPlot:
    """ Constant Current Plot """
    constant_current = 0
    initial_voltage = 0
    end_voltage = 0
    time_in_sec = 0
    time_in_hour = 0
    ampere_hour = 0
    milli_amphour = 0
    watt_hour = 0
    db_file_name = None
    conn = None
    cur = None
    inst = None

    def _init_(self, instrument, date_time, constant_current, end_voltage):
        """ main method in CCPlot that prepares for reading data from instrument and writing data into database """
        self.constant_current = float(constant_current)
        self.end_voltage = float(end_voltage)
        self.db_file_name = create_db_files(date_time)
        print(self.db_file_name)

        self.conn = sqlite3.connect(self.db_file_name)
        self.cur = self.conn.cursor()
        self.inst = instrument

        # cc_create_table creates a sqlite table if user wants to:
        # if_continue == 1, then keep going, else termintes
        if_continue = self.cc_create_table()
        if if_continue:
            self.cc_set_instrument()
            self.initial_voltage = self.initial_state()
            self.inst.input_on()
            self.read_and_store_data(float(self.initial_voltage))
            self.inst.input_off()

            self.cur.execute("SELECT * from dataTable")
            table = self.cur.fetchall()

            df = pd.DataFrame(table,
            columns=["TimeInSec", "TimeInHour", "Current", "Voltage",
             "Resistance", "Power", "AmpHour", "milliAmpHour", "WattHour"])

            print(df)
            print("\n")

            #create csv files
            create_csv_files(date_time, df)

            #display ending ui
            end_ui(df, 'Constant Current', self.initial_voltage, self.end_voltage, date_time, self.time_in_sec)

            #closing database reading and turn off instrument
            self.cc_close_db()
        else:
            return

    def cc_create_table(self):
        """ get the count of tables with the name """
        self.cur.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='dataTable' ''')

        #if the count is 1, then table exists
        if self.cur.fetchone()[0] == 1:
            print('Table exists.')
            if_continue = input("Would you like to start a fresh new table? (y/n)")
            while True:
                if if_continue[0] == "y" or if_continue[0] == "Y":
                    self.cur.execute("DROP TABLE dataTable")
                    self.cur.execute("""Create Table dataTable (
                                        timeInSec INTEGER,
                                        timeInHour REAL,
                                        current REAL,
                                        voltage REAL,
                                        resistance REAL,
                                        power REAL,
                                        amphour REAL,
                                        mamphour REAL,
                                        watthour REAL
                                    )""")
                    break
                if if_continue[0] == "n" or if_continue[0] == "N":
                    print("Program terminating now ~")
                    return False
                else:
                    if_continue = input("unable to read your input, would you like to start a new table? (please answer with 'y' or 'n')")
        else:
            self.cur.execute("""Create Table dataTable (
                                timeInSec INTEGER,
                                timeInHour REAL,
                                current REAL,
                                voltage REAL,
                                resistance REAL,
                                power REAL,
                                amphour REAL,
                                mamphour REAL,
                                watthour REAL
                                )""")
            return True

    def cc_close_db(self):
        """ closes the connection to database """
        self.conn.commit()
        self.conn.close()

    def cc_set_instrument(self):
        """ reset instrument """
        self.inst.reset()
        self.inst.constant_current_mode()
        self.inst.set_current_range(str(constants.CURRENT_RANGE))
        self.inst.set_current(str(self.constant_current))

    def initial_state(self):
        """ gets the initial state of the battery: initial voltage """
        initial_voltage = float(self.inst.get_voltage())
        opc = self.inst.get_opc()
        if initial_voltage <= self.end_voltage:
            errors.voltage_setting_error()

        return str(initial_voltage)

    def read_and_store_data(self, voltage_reading):
        """ main method for reading the instrument and writing to database """
        print("Time(s)   Time(hr)   Curr(A)    Volt(V)    Res(Ohm)     Pow(W)      Ah        mAh        Wh")
        time.sleep(constants.SLEEP_TIME)

        initial_time = time.time()
        target_time = constants.TIME_INTERVAL

        while voltage_reading >= self.end_voltage:

            # time_in_sec and time_in_hour record the time elapsed in sec/hr
            self.time_in_sec = round(time.time() - initial_time, 2)
            self.time_in_hour = self.time_in_sec / 3600

            #get the current voltage and current reading
            self.inst.timeout = 0.4
            voltage_reading = float(self.inst.get_voltage())
            current_reading = float(self.inst.get_current())
            opc = self.inst.get_opc()

            #calculate resistance, power, ah, mah, wh
            resistance_reading = voltage_reading / current_reading
            power_reading = voltage_reading * current_reading

            self.ampere_hour += (current_reading * constants.TIME_INTERVAL / 3600)
            self.milli_amphour = (self.ampere_hour * 1000)
            self.watt_hour += (power_reading * constants.TIME_INTERVAL / 3600)

            #insert data into database
            self.cur.execute("INSERT INTO dataTable VALUES (:timeInSec, :timeInHour, :current, :voltage, :resistance, :power, :amphour, :mamphour, :watthour)",
                {'timeInSec': self.time_in_sec, 'timeInHour': self.time_in_hour, 'current': current_reading,
                  'voltage': voltage_reading, 'resistance': resistance_reading, 'power':power_reading,
                  'amphour': self.ampere_hour, 'mamphour': self.milli_amphour, 'watthour': self.watt_hour})

            #print data in terminal
            print("%.1f     %.5f     %.5f      %.5f      %.2f     %.2f     %.6f     %.5f     %.5f"
                % (self.time_in_sec, self.time_in_hour, current_reading, voltage_reading,
                 resistance_reading, power_reading, self.ampere_hour, self.milli_amphour, self.watt_hour))

            current_time = round(time.time() - initial_time, 2)

            # raise error message if taking longer than a time interval
            if current_time > target_time:
                errors.operation_timeout_error()

            # loop until current_time reaches target_time interval
            while current_time < target_time:
                current_time = round(time.time() - initial_time, 2)

            target_time += constants.TIME_INTERVAL

"""
Written by Candice Cao

This module is for recording a test log, including the time the test is run, equipment meta data,
battery meta data, mode, end voltage, constant variable
"""

import sqlite3

LOG_FILE_NAME = "log/log.db"

def initialize_record_log():
    """ initializes the record log table in sqlite database """
    conn = sqlite3.connect(LOG_FILE_NAME)
    cur = conn.cursor()

    #get the count of tables with the name
    cur.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='logTable1' ''')

    #if the count is 1, then table exists
    if cur.fetchone()[0] == 1:
        print('Table1 exists.')

    else:
        cur.execute("""Create Table logTable1 (
                       id REAL,
                       date_string TEXT,
                       time_string TEXT,
                       equipment_brand TEXT,
                       equipment_model_number TEXT,
                       equipment_serial_number TEXT,
                       equipment_software_revision TEXT,
                       room_temperature TEXT,
                       mode TEXT,
                       end_voltage TEXT,
                       constant_var TEXT
                       )""")

    #get the count of tables with the name
    cur.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='logTable2' ''')

    #if the count is 1, then table exists
    if cur.fetchone()[0] == 1:
        print('Table2 exists.')
    else:
        cur.execute("""Create Table logTable2 (
                       id REAL,
                       battery_brand TEXT,
                       battery_form_factor TEXT,
                       battery_model_number TEXT,
                       battery_chemistry_type TEXT,
                       battery_nominal_voltage TEXT,
                       battery_nominal_ah TEXT,
                       battery_nominal_wh TEXT,
                       battery_serial_number TEXT,
                       battery_manufacturing_date_code TEXT,
                       battery_expiration_date TEXT,
                       battery_coo TEXT
                       )""")
    conn.commit()
    conn.close()

def insert_new_log(date_time, equipment_meta, battery_meta, mode, end_voltage, constant_var):
    """ insert a new log to the data table """
    conn = sqlite3.connect(LOG_FILE_NAME)
    cur = conn.cursor()

    cur.execute("SELECT * from logTable1")
    count = len(cur.fetchall()) + 1
    print(count)

    cur.execute("INSERT INTO logTable1 VALUES (:id, :date_string, :time_string, :equipment_brand, :equipment_model_number, :equipment_serial_number, :equipment_software_revision, :room_temperature, :mode, :end_voltage, :constant_var)",
        {'id': count, 'date_string': date_time[0:10], 'time_string':date_time[11:19],
        'equipment_brand': equipment_meta[0], 'equipment_model_number':equipment_meta[1],
        'equipment_serial_number': equipment_meta[2], 'equipment_software_revision': equipment_meta[3],
        'room_temperature': battery_meta[9], 'mode': mode, 'end_voltage': end_voltage, 'constant_var': constant_var})

    cur.execute("INSERT INTO logTable2 VALUES (:id, :battery_brand, :battery_form_factor, :battery_model_number, :battery_chemistry_type, :battery_nominal_voltage, :battery_nominal_ah, :battery_nominal_wh, :battery_serial_number, :battery_manufacturing_date_code, :battery_expiration_date, :battery_coo)",
        {'id': count, 'battery_brand': battery_meta[0], 'battery_form_factor': battery_meta[1],
        'battery_model_number': battery_meta[2], 'battery_chemistry_type': battery_meta[3],
        'battery_nominal_voltage': battery_meta[4], 'battery_nominal_ah': battery_meta[5],
        'battery_nominal_wh': battery_meta[6], 'battery_serial_number': battery_meta[7],
        'battery_manufacturing_date_code': battery_meta[8], 'battery_expiration_date': battery_meta[9],
        'battery_coo': battery_meta[10]})

    cur.execute("SELECT * from logTable1")
    table1 = cur.fetchall()
    cur.execute("SELECT * from logTable2")
    table2 = cur.fetchall()

    print(table1)
    print(table2)

    conn.commit()
    conn.close()

def clear_table():
    """ clear the whole log table in database """
    conn = sqlite3.connect(LOG_FILE_NAME)
    cur = conn.cursor()

    cur.execute("DELETE FROM logTable1")
    cur.execute("DELETE FROM logTable2")

    conn.commit()
    conn.close()

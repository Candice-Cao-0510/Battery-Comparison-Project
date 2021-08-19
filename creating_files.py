"""
Written by Candice Cao

This module has all functions that create different types of files
"""

import os
cwd = os.path.abspath(os.getcwd())

def create_csv_files(date_time, df):
    """ creates csv files """
    file_name = ('csvDataFiles/%s.csv' % date_time)
    df.to_csv(file_name, index_label="Index")

def create_db_files(date_time):
    """ creates db files """
    file_name = ("dbDataFiles/%s.db" % (date_time))
    return file_name

def create_png(date_time):
    """ creates png """
    png_name = ("%s/plot_screenshots/%s.png" % (cwd, date_time))
    return png_name

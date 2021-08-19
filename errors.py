"""
Written by Candice Cao

this module includes methods for raising errors under certain conditions

"""
def current_limit_error():
    """ when the current limit is too high """
    raise ValueError("Current can not be higher than 0.1A")

def voltage_setting_error():
    """ when the current voltage in the battery is already lower than target voltage """
    raise ValueError("Initial Voltage is already <= target voltage")

def time_interval_limit_error():
    """ when the sampling interval is too short """
    raise ValueError("Time interval can not be lower than 0.75 second")

def instrument_timeout_error():
    """ when the instrument reading did not finish in given time """
    raise TimeoutError("Instrument reading time out")

def operation_timeout_error():
    """ when the operations did not finish in giver time """
    raise TimeoutError("Operations can not be finished in the given amount of time")

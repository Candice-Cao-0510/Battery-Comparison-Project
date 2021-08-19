
"""
written by Candice Cao
This module includes all commands for controlling BK Precision 8601 instrument
And each object of BKP8600 contains all info of the currently accessed instrument
"""

class BKP8600:
    """ BK Precision 8601 object, includes identification and commands to control the instrument """
    inst = None
    name = None
    idn = None
    instrument_type = None

    def _init_(self, visa_instance, identity):
        """ instrument info """
        self.inst = visa_instance
        self.name = "BK Precision 8600"
        self.idn = identity
        self.instrument_type = "electronic load"

    def get_identifier(self):
        """ get identifier """
        return self.idn

# reset, input on (start draining battery), input off (stop draining battery)
    def reset(self):
        """ reset the instrument """
        self.inst.write('rst')

    def input_on(self):
        """ turn on the input reading """
        self.inst.write('inp 1')

    def input_off(self):
        """ turn off the input reading """
        self.inst.write('inp 0')

# mode: constant current, constant resistance, constant power, constant voltage

    def constant_current_mode(self):
        """ put the instrument in constant current mode """
        self.inst.write('func current')

    def constant_resistance_mode(self):
        """ put the instrument in constant resistance mode """
        self.inst.write('func resistance')

    def constant_power_mode(self):
        """ put the instrument in constant power mode """
        self.inst.write('func power')

    def constant_voltage_mode(self):
        """ put the instrument in constant voltage mode """
        self.inst.write('func voltage')

# get & set current, voltage, resistance, power range


    def set_current_range(self, current_range):
        """ set constant current range (MAX) """
        self.inst.write('current:range ' + current_range)

    def get_current_range(self):
        """ query constant current range """
        return self.inst.query('current:range?')

    def set_voltage_range(self, voltage_range):
        """ set constant voltage range (MIN) """
        self.inst.write('voltage:range ' + voltage_range)

    def get_voltage_range(self):
        """ query constant voltage range """
        return self.inst.query('voltage:range?')

    def set_resistance_range(self, resistance_range):
        """ set constant resistance range (MAX) """
        self.inst.write('resistance:range ' + resistance_range)

    def get_resistance_range(self):
        """ query constant resistance range """
        return self.inst.query('resistance:range?')

    def set_power_range(self, power_range):
        """ set power protection delay time (3) """
        self.inst.write('power:range ' + power_range)

    def get_power_range(self):
        """ query power protection delay time """
        return self.inst.query('power:range?')

# set & get current, voltage, resistance, power

    def set_current(self, current):
        """ set current when in constant current mode """
        self.inst.write('current ' + current)

    def get_current(self):
        """ get current current """
        return self.inst.query(':measure:current?')

    def set_voltage(self, voltage):
        """ set voltage when in constant voltage mode """
        self.inst.write('voltage ' + voltage)

    def get_voltage(self):
        """ get current voltage """
        return self.inst.query(':measure:voltage?')

    def set_resistance(self, resistance):
        """ set resistance when in constant resistance mode """
        self.inst.write('resistance ' + resistance)

    def get_resistance(self):
        """ get current resistance """
        return self.inst.query('resistance?')

    def set_power(self, power):
        """ set power when in constant power mode """
        self.inst.write('power ' + power)

    def get_power(self):
        """ get current power """
        return self.inst.query('power?')

    def get_opc(self):
        """ query opc: whether the operation has finished """
        return self.inst.query("*OPC?")

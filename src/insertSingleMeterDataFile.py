#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Inserted a single file of meter data.

Usage:

    insertSingleMeterDataFile.py

"""

__author__ = 'Daniel Zhang (張道博)'
__copyright__ = 'Copyright (c) 2014, University of Hawaii Smart Energy Project'
__license__ = 'https://raw.github.com/Hawaii-Smart-Energy-Project/Smart-Grid' \
              '-PV-Inverter/master/BSD-LICENSE.txt'

from sek.logger import SEKLogger
from si_configer import SIConfiger
from sek.db_util import SEKDBUtil
from sek.db_connector import SEKDBConnector
import argparse


def processCommandLineArguments():
    """
    Create command line arguments and parse them.
    """

    global parser, commandLineArgs
    parser = argparse.ArgumentParser(
        description = 'Perform insertion of data contained in a single file to '
                      'the SI database.')
    parser.add_argument('--filepath',
                        help = 'A filepath, including the filename, '
                               'for a file containing data to be inserted.')
    commandLineArgs = parser.parse_args()


class SingleFileLoader(object):
    """
    Perform insertion of data contained in a single file to the Smart Inverter database
    specified in the configuration file.
    """

    def __init__(self, testing = False):
        """
        Constructor.

        :param testing: Flag indicating if testing mode is on.
        """

        self.logger = SEKLogger(__name__)
        self.configer = SIConfiger()
        self.dbUtil = SEKDBUtil()
        self.conn = SEKDBConnector(
            dbName = self.configer.configOptionValue('Database', 'db_name'),
            dbHost = self.configer.configOptionValue('Database', 'db_host'),
            dbPort = self.configer.configOptionValue('Database', 'db_port'),
            dbUsername = self.configer.configOptionValue('Database',
                                                         'db_username'),
            dbPassword = self.configer.configOptionValue('Database',
                                                         'db_password')).connectDB()
        self.cursor = self.conn.cursor()
        self.meterDataTable = "MeterData"
        self.exitOnError = True
        self.columns = [
            "time(UTC)", "error", "lowalarm", "highalarm",
            "Accumulated Real Energy Net (kWh)",
            "Real Energy Quadrants 1 & 4, Import (kWh)",
            "Real Energy Quadrants 2 & 3, Export (kWh)",
            "Reactive Energy Quadrant 1 (VARh)",
            "Reactive Energy Quadrant 2 (VARh)",
            "Reactive Energy Quadrant 3 (VARh)",
            "Reactive Energy Quadrant 4 (VARh)", "Apparent Energy Net (VAh)",
            "Apparent Energy Quadrants 1 & 4 (VAh)",
            "Apparent Energy Quadrants 2 & 3 (VAh)",
            "Total Net Instantaneous Real Power (kW)",
            "Total Net Instantaneous Reactive Power (kVAR)",
            "Total Net Instantaneous Apparent Power (kVA)",
            "Total Power Factor", "Voltage, L-L, 3p Ave (Volts)",
            "Voltage, L-N, 3p Ave (Volts)", "Current, 3p Ave (Amps)",
            "Frequency (Hz)", "Total Real Power Present Demand (kW)",
            "Total Reactive Power Present Demand (kVAR)",
            "Total Apparent Power Present Demand (kVA)",
            "Total Real Power Max Demand, Import (kW)",
            "Total Reactive Power Max Demand, Import (kVAR)",
            "Total Apparent Power Max Demand, Import (kVA)",
            "Total Real Power Max Demand, Export (kW)",
            "Total Reactive Power Max Demand, Export (kVAR)",
            "Total Apparent Power Max Demand, Export (kVA)",
            "Accumulated Real Energy, Phase A, Import (kW)",
            "Accumulated Real Energy, Phase B, Import (kW)",
            "Accumulated Real Energy, Phase C, Import (kW)",
            "Accumulated Real Energy, Phase A, Export (kW)",
            "Accumulated Real Energy, Phase B, Export (kW)",
            "Accumulated Real Energy, Phase C, Export (kW)",
            "Accumulated Q1 Reactive Energy, Phase A, Import (VARh)",
            "Accumulated Q1 Reactive Energy, Phase B, Import (VARh)",
            "Accumulated Q1 Reactive Energy, Phase C, Import (VARh)",
            "Accumulated Q2 Reactive Energy, Phase A, Import (VARh)",
            "Accumulated Q2 Reactive Energy, Phase B, Import (VARh)",
            "Accumulated Q2 Reactive Energy, Phase C, Import (VARh)",
            "Accumulated Q3 Reactive Energy, Phase A, Export (VARh)",
            "Accumulated Q3 Reactive Energy, Phase B, Export (VARh)",
            "Accumulated Q3 Reactive Energy, Phase C, Export (VARh)",
            "Accumulated Q4 Reactive Energy, Phase A, Export (VARh)",
            "Accumulated Q4 Reactive Energy, Phase B, Export (VARh)",
            "Accumulated Q4 Reactive Energy, Phase C, Export (VARh)",
            "Accumulated Apparent Energy, Phase A, Import (VAh)",
            "Accumulated Apparent Energy, Phase B, Import (VAh)",
            "Accumulated Apparent Energy, Phase C, Import (VAh)",
            "Accumulated Apparent Energy, Phase A, Export (VAh)",
            "Accumulated Apparent Energy, Phase B, Export (VAh)",
            "Accumulated Apparent Energy, Phase C, Export (VAh)",
            "Real Power, Phase A (kW)", "Real Power, Phase B (kW)",
            "Real Power, Phase C (kW)", "Reactive Power, Phase A (kVAR)",
            "Reactive Power, Phase B (kVAR)", "Reactive Power, Phase C (kVAR)",
            "Apparent Power, Phase A (kVA)", "Apparent Power, Phase B (kVA)",
            "Apparent Power, Phase C (kVA)", "Power Factor, Phase A",
            "Power Factor, Phase B", "Power Factor, Phase C",
            "Voltage, Phase A-B (Volts)", "Voltage, Phase B-C (Volts)",
            "Voltage, Phase A-C (Volts)", "Voltage, Phase A-N (Volts)",
            "Voltage, Phase B-N (Volts)", "Voltage, Phase C-N (Volts)",
            "Current, Phase A (Amps)", "Current, Phase B (Amps)",
            "Current, Phase C (Amps)"
        ]


    def insertData(self):
        """
        Insert a row of data to the database.
        """
        values = ''
        sql = 'INSERT INTO "{0}" ({1}) VALUES( {2})'.format(self.meterDataTable,
                                                            ','.join(
                                                                self.columns),
                                                            values)
        self.logger.log('sql: {}'.format(sql), 'debug')
        success = self.dbUtil.executeSQL(self.cursor, sql,
                                         exitOnFail = self.exitOnError)


    def meterID(self, meterName):
        """
        Given a meter name, return its meter ID.
        If the meter name has no ID, create a new one and return it.
        :param meterName: String
        :return: Int of meter ID
        """

        def __meterID(name):
            """
            :param name: String of meter name
            :return: Int or None
            """
            sql = 'SELECT meter_id FROM "Meters" WHERE meter_name = \'{}\''.format(name)
            success = self.dbUtil.executeSQL(self.cursor, sql,
                                             exitOnFail = self.exitOnError)
            return id

        def __makeNewMeter(name):
            """
            :param name: String of meter name
            :return: Int or None
            """
            sql = 'INSERT INTO "Meters" (meter_name) VALUES (\'{}\')'.format(name)
            return id

        id = __meterID(meterName)
        if id:
            return id
        else:
            return __makeNewMeter(meterName)

if __name__ == '__main__':
    inserter = SingleFileLoader()
    processCommandLineArguments()
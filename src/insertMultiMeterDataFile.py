#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Insert multiple data files of meter data by recursively locating available files.

Usage:

    insertMultiMeterDataFile.py --basepath ${PATH}

The naming of this script is unusual on purpose to be consistent with the
single file version.

"""

__author__ = 'Daniel Zhang (張道博)'
__copyright__ = 'Copyright (c) 2014, University of Hawaii Smart Energy Project'
__license__ = 'https://raw.github.com/Hawaii-Smart-Energy-Project/Smart-Grid' \
              '-PV-Inverter/master/BSD-LICENSE.txt'

from sek.logger import SEKLogger
from si_configer import SIConfiger
import argparse
from insertSingleMeterDataFile import SingleFileLoader
import multiprocessing
import os
import fnmatch


COMMAND_LINE_ARGS = None
MULTIPROCESSING_LIMIT = 4


def processCommandLineArguments():
    """
    Create command line arguments and parse them.
    """

    global COMMAND_LINE_ARGS
    parser = argparse.ArgumentParser(
        description = 'Perform insertion of data contained in multiple files to the SI database.')
    parser.add_argument('--basepath', help = 'A base path from which to process data files.')
    COMMAND_LINE_ARGS = parser.parse_args()


class MultiFileLoader(object):
    """
    Perform insertion of data contained in multiple files to the Smart
    Inverter database specified in the site configuration file.
    """

    def __init__(self, basepath = '', testing = False):
        """
        Constructor.
        :param basepath: String
        :param testing: Flag indicating if testing mode is on.
        """

        self.logger = SEKLogger(__name__, 'debug')
        self.configer = SIConfiger()
        self.basepath = basepath


def pathsToProcess():
    """
    :return: List
    """
    global COMMAND_LINE_ARGS
    pathsToProcess = []
    for root, dirnames, filenames in os.walk(COMMAND_LINE_ARGS.basepath):
        for filename in fnmatch.filter(filenames, '*.csv'):
            logger.log(filename, 'debug')
            pathsToProcess.append(os.path.join(root, filename))
    return pathsToProcess


if __name__ == '__main__':
    logger = SEKLogger(__name__, 'debug')
    processCommandLineArguments()


    def insertData(x):
        logger.log('process {}'.format(str(multiprocessing.current_process())))
        SingleFileLoader(x).insertDataFromFile()


    pool = multiprocessing.Pool(MULTIPROCESSING_LIMIT)
    results = pool.map(insertData, pathsToProcess())
    pool.close()
    pool.join()
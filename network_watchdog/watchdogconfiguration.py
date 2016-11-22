"""
This module handles the configuration data used by the network watchdog component.
The data has a simple structure a map of properties:
    * TARGET. The action that will be taken when a disconnection is detected.
    * TIMEOUT_IN_MS. The timeout used by the ping tool, to check whether a configured IP can be reached.
    * IP_TO_CHECK. The IP to check using ping, to decide whether connection is working or not.
    * SLEEP_TIME_IN_S. Value used for the period between ping invocations.
"""


"""
 Copyright (C) 2015 Mytech Ingenieria Aplicada <http://www.mytechia.com>
 Copyright (C) 2015 Victor Sonora Pombo <victor.pombo@mytechia.com>

 This file is part of network_watchdog.

 network_watchdog is free software: you can redistribute it and/or modify it under the
 terms of the GNU General Public License as published by the Free
 Software Foundation, either version 3 of the License, or (at your option) any
 later version.

 network_watchdog is distributed in the hope that it will be useful, but WITHOUT ANY
 WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
 A PARTICULAR PURPOSE. See the GNU General Public License for more
 details.

 You should have received a copy of the GNU General Public License
 along with network_watchdog. If not, see <http://www.gnu.org/licenses/>.
"""


import pickle
import os.path
import watchdoglogger

import watchdogparameters

__author__ = 'victor'


def load_watchdog_configuration_from(path):
    """
    Loads the watchdog configuration data from an existing binary file located in a given path.
    :param path: full path for the configuration data file.
    :return: the watchdog configuration data, as a map.
    """
    return pickle.load(open(path, "rb"))


def save_watchdog_configuration_to(path, watchdog_configuration):
    """
    Saves the given watchdog configuration data to a file as binary data.
    :param path: full path for the file where teh configuration data is to be persisted.
    :param watchdog_configuration: the watchdog configuration data as a map or properties.
    :return: nothing.
    """
    pickle.dump(watchdog_configuration, open(path, "wb"))


def build_default_watchdog_configuration():
    """
    Builds a default watchdog configuration data, as a map.
    :return: default values for the watchdog configuration data.
    """
    return {watchdogparameters.TARGET: watchdogparameters.TARGET_SEND_ALERT,
            watchdogparameters.TIMEOUT_IN_MS: 1500,
            watchdogparameters.IP_TO_CHECK: "127.0.0.1",
            watchdogparameters.SLEEP_TIME_IN_S: 5}


def check_watchdog_configurations_file(path):
    """
    Checks whether a file to persist watchdog configuration data exists.
    If not, it initializes a default watchdog configuration data and saves it in the given path.
    :param path: full path where watchdog configuration data should exists, or be created.
    :return: nothing.
    """
    if not os.path.exists(path):
        save_watchdog_configuration_to(path, build_default_watchdog_configuration())

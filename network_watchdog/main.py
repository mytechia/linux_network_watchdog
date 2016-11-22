#!/usr/bin/env python
# coding: utf-8


"""
Launcher for the NetworkWatchdog component.
Uses ping to check whether a network connection is working, and when the network is down executes configurable actions.
The main loop:
    * checks the existing database (a single binary file) for this component configuration data.
    * loads the existing configuration.
    * launches a DBUS service that handles changes to the component configuration.
    * launches a watchdog worker instance, the one who does the job.
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


import watchdogconfiguration
import watchdog
import watchdoglogger
import sys


__author__ = 'victor'


def main():
    if len(sys.argv) != 3:
        print 'This module needs 2 arguments: DATA_FILE_NAME, LOG_FILE_NAME'
    data_file_name = sys.argv[1]
    log_file_name = sys.argv[2]
    logger = watchdoglogger.initialize_logger(log_file_name)
    watchdogconfiguration.check_watchdog_configurations_file(data_file_name)
    logger.info("Configurations checked")
    watchdog_worker = watchdog.Watchdog(data_file_name)
    logger.info("Watchdog worker initialized")
    watchdog_service = watchdog.WatchdogDBus(watchdog_worker)
    watchdog_worker.register_send_event_callback(watchdog_service.send_connection_timeout_alert)
    logger.info("Watchdog DBus service initialized")
    watchdog_worker.start()
    logger.info("Watchdog worker launched")
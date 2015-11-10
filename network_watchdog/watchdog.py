#!/usr/bin/env python
# coding: utf-8


"""
This module handles a watchdog that checks whether a network connection is working.
It uses a ping tool to check on a configured IP address.
When the
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


import threading
import time

import ping
import socket
import dbus
import dbus.service
import watchdogparameters
import watchdogconfiguration

__author__ = 'victor'


def reboot(data):
    """
    Action to be taken by the watchdog.
    It reboots the whole Linux system, the old way.
    :return: nothing.
    """
    command = "/sbin/shutdown -r now"
    import subprocess
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    print output


def reconnect(data):
    """
    Action to be taken by the watchdog.
    Tries to reconnect to the current network configuration.
    Uses the DBUS API offered by the WiFiConfig component.
    :return: nothing.
    """
    bus = dbus.SystemBus()
    wificonfig_service = bus.get_object('com.mytechia.wificonfig', '/com/mytechia/wificonfig')
    reconnect_method = wificonfig_service.get_dbus_method('reconnect', 'com.mytechia.wificonfig')
    reconnect_method()


def null(data):
    pass


RULE_SWITCHER = {
    # Map with the possible actions the watchdog can take.
    watchdogparameters.TARGET_REBOOT: reboot,
    watchdogparameters.TARGET_RECONNECT: reconnect
}


def check_ip(ip, time_in_ms):
    """
    Returns the delay of a ping to the given ip address.
    False when there is no response.
    :param time_in_ms: is the timeout limit.
    """
    try:
        result = ping.quiet_ping(ip, timeout=(time_in_ms / 1000.0))  # result is (percent max avrg)
        if not result:
            return False
        return result[2]
    except socket.error, e:
        print "Ping Error:", e
        return False


class Watchdog(threading.Thread):
    """
    A Watchdog has its own thread and checks whether a configured IP address can be reached.
    When the ping fails, a configuration-selectable action is executed.
    """

    def __init__(self, config_file_path):
        threading.Thread.__init__(self)
        self.config_file_path = config_file_path
        self.config = watchdogconfiguration.load_watchdog_configuration_from(config_file_path)
        self.stopped = False
        self.send_event_callback = null
        self.timeouts_counter = 0

    def stop(self):
        self.stopped = True

    def run(self):
        while not self.stopped:
            time.sleep(self.config[watchdogparameters.SLEEP_TIME_IN_S])     # wait for SLEEP_TIME_IN_S
            alive = check_ip(
                self.config[watchdogparameters.IP_TO_CHECK],
                self.config[watchdogparameters.TIMEOUT_IN_MS])
            if not alive:
                self.timeouts_counter += 1  # increment timeouts counter
                self._process(self.timeouts_counter)    # the actual job is done by a callback action
            else:
                self.timeouts_counter = 0   # reset timeouts counter

    def _process(self, data):
        """
        Executes the action selected in the handled config as TARGET.
        By default, it executes the send_event action.
        This action is the null() one unless a proper action callback has been registered.
        """
        process_func = RULE_SWITCHER.get(self.config[watchdogparameters.TARGET], self._send_event)
        process_func(data)

    def _send_event(self, data):
        self.send_event_callback(data)

    def _save_config(self):
        watchdogconfiguration.save_watchdog_configuration_to(self.config_file_path, self.config)

    def register_send_event_callback(self, action_callback):
        self.send_event_callback = action_callback

    def change_target(self, target):
        self.config[watchdogconfiguration.TARGET] = target
        self._save_config()

    def change_ip_to_check(self, ip):
        self.config[watchdogconfiguration.IP_TO_CHECK] = ip
        self._save_config()


class WatchdogDBus(dbus.service.Object):
    """
    Encapsulates a DBUS service whose API handles methods to handle the watchdog configuration.
    This service is associated to a configured Watchdog object.
    """

    def __init__(self, w):
        self.watchdog = w
        bus_name = dbus.service.BusName('com.mytechia.networkwatchdog', bus=dbus.SystemBus())
        dbus.service.Object.__init__(self, bus_name, '/com/mytechia/networkwatchdog')

    @dbus.service.method('com.mytechia.networkwatchdog')
    def change_target(self, target):
        self.watchdog.change_target(target)

    @dbus.service.method('com.mytechia.networkwatchdog')
    def change_ip_to_check(self, ip):
        self.watchdog.change_ip_to_check(ip)

    @dbus.service.signal('com.mytechia.networkwatchdog')
    def send_connection_timeout_alert(self, alert_data):
        """
        :param alert_data: currently it includes only the number of timeouts
        :return:
        """
        print "Timeout alert sent: " + str(alert_data)
        return alert_data




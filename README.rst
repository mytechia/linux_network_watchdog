Network Watchdog
================

A component that monitors network availability by checking ping response to a determined IP address.

It can be configured to send aert signals via DBUS, or to use builtin functions to try to reconnect or reboot when
ping check fails.

----

##Contents: Python sources.

The main.py launches both a DBUS service and a small watchdog with its own thread that used ping to check
network availability.

DBUS API: ("com.mytechia.networkwatchdog")

* [method] change_target(action_target)
* [method] change_ip_to_check(ip_as_string)
* [signal] send_connection_timeout_alert(alert_data)

Currently there are tree action_target support: reboot, reconnect, send_alert.

The intented normal use happens with send_alert. In this mode, every time ping fails the watchdog sends an alert
via DBUS, as a signal.

The actions reconnect and reboot can be configured also. This way the watchdog itself acts on the problem.

----

##Contents: Config files.

This package contains all the needed files for a modern Linux distribution. It assumes systemd.

The main.py is wrapped in a small script: wrapped in a small script: network_watchdog.

A .service file is needed in order to launch this script: networkwatchdog.service.

Both a .service file and a .conf file (needed to specify permissions) are used for DBUS integration.
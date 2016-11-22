#!/bin/sh
#exec_path="python `python -c "import site; print site.getsitepackages()[0]"`/network_watchdog/__main__.py"
#eval ${exec_path}
python -m network_watchdog.__main__ /var/tmp/networkwatchdog_data.p /var/tmp/networkwatchdog.log

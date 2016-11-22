#!/bin/sh
#exec_path="python `python -c "import site; print site.getsitepackages()[0]"`/network_watchdog/__main__.py"
#eval ${exec_path}
mkdir -p /var/local/tmp
python -m network_watchdog.__main__ /var/local/tmp/networkwatchdog_data.p /var/local/tmp/networkwatchdog.log

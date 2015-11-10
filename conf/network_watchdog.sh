#!/bin/sh
exec_path="python `python -c "import site; print site.getsitepackages()[0]"`/network_watchdog/main.py"
eval ${exec_path}
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

import main

__author__ = 'victor'

from dbus.mainloop.glib import DBusGMainLoop


if __name__ == '__main__':
    DBusGMainLoop(set_as_default=True)
    main.main()
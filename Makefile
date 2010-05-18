# Copyright 2009 Markus Pielmeier
#
# This file is part of gps4earth.
#
# gps4earth is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# gps4earth is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with gps4earth.  If not, see <http://www.gnu.org/licenses/>.
#

CGI_BIN=/usr/lib/cgi-bin

all:

install:
	install -D src/gps4earth.py ${CGI_BIN}/gps4earth.py
	install -D src/client.py ${CGI_BIN}/client.py
	install -D src/gps.py ${CGI_BIN}/gps.py

uninstall:
	rm -- ${CGI_BIN}/gps4earth.py

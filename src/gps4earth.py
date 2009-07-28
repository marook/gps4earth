#!/usr/bin/env python
#
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


#====================================================================
# first set up exception handling and logging

import logging
import sys

def setUpLogging():
    def exceptionCallback(eType, eValue, eTraceBack):
        import cgitb

        txt = cgitb.text((eType, eValue, eTraceBack))

        logging.fatal(txt)
    
        # sys.exit(1)

    # configure file logger
    logging.basicConfig(level=logging.DEBUG, format = '%(asctime)s %(levelname)s %(message)s',
                        filename = '/tmp/gps4earth.log',
                        filemode='a')
    
    # configure console logger
    consoleHandler = logging.StreamHandler(sys.stdout)
    consoleHandler.setLevel(logging.DEBUG)
    
    consoleFormatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    consoleHandler.setFormatter(consoleFormatter)
    logging.getLogger().addHandler(consoleHandler)

    # replace default exception handler
    sys.excepthook = exceptionCallback
    
    logging.debug('Logging and exception handling has been set up')

if __name__ == '__main__':
    # TODO implement cmd line configurable logging
    setUpLogging()
    
    pass

#====================================================================
# here the application begins

import gps

def testGps():
    session = gps.gps()
    session.verbose = 1
    
    session.connect('localhost', 2947) 
    
    # this is the query from my gps-info app
    #session.query('w+x0')

    # this is the query from the example
    #session.query('admosy')
    
    # possible querries:
    #   x: ?
    logging.debug('query result: %s' , session.query('admosy'))
    logging.debug('timings: %s' , session.timings)
    logging.debug('online: %s', session.online)
    
    #session.poll()
    
    if(session.waiting()):
        logging.debug('GPS data is ready.')
    else:
        logging.debug('GPS data is not ready.')
    
    logging.debug(' GPS reading')
    logging.debug('----------------------------------------')
    logging.debug('latitude    %s' , session.fix.latitude)
    logging.debug('longitude   %s' , session.fix.longitude)
    logging.debug('time utc    %s %s' , session.utc, session.fix.time)
    logging.debug('altitude    %s' , session.fix.altitude)
    logging.debug('eph         %s' , session.fix.eph)
    logging.debug('epv         %s' , session.fix.epv)
    logging.debug('ept         %s' , session.fix.ept)
    logging.debug('speed       %s' , session.fix.speed)
    logging.debug('climb       %s' , session.fix.climb)

    session.close()

def main():
    testGps()
if __name__ == '__main__':
    main()

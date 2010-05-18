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
    #setUpLogging()
    
    pass

#====================================================================
# here the application begins

import gps
import time

MAX_GPS_TRIES = 10
GPS_TRY_SLEEP = 1

def getGpsPosition():
    session = gps.gps()
    session.stream(0x80)
    
    try:
        # enable extended output
        #session.verbose = 1
        
        i = 0
        while(i < MAX_GPS_TRIES):
            r = session.next()
            
            logging.debug('GPS query result: %s' , r)
            
            if(session.fix.mode > 1):
                logging.info('Fetched GPS data after %s cycles.', i)
                
                return session.fix
    
            time.sleep(GPS_TRY_SLEEP)
            
            i = i + 1
            
        logging.warn('Can\'t fetch GPS data after %s cycles.', i)
            
        return None
    finally:
        session.close()

def generateKml(longitude, latitude):
    return ('<?xml version="1.0" encoding="UTF-8"?><kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns:kml="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom">'
            + '<Document><name>GPS</name><visibility>1</visibility><StyleMap id="msn_ylw-pushpin">'
            + '<Pair><key>normal</key><styleUrl>#sn_ylw-pushpin</styleUrl></Pair>'
            + '<Pair><key>highlight</key><styleUrl>#sh_ylw-pushpin</styleUrl></Pair>'
            + '</StyleMap>'
            + '<Style id="sn_ylw-pushpin">'
            + '<IconStyle>'
            + ' <color>ff0000ff</color>'
            + '     <Icon>'
            + '      <href>http://maps.google.com/mapfiles/kml/pushpin/ylw-pushpin.png</href>'
            + '    </Icon>'
            + ' <hotSpot x="20" y="2" xunits="pixels" yunits="pixels"/>'
            + '</IconStyle>'
            + '</Style>'
            + '<Style id="sh_ylw-pushpin">'
            + ' <IconStyle>'
            + '  <color>ff0000ff</color>'
            + '            <scale>1.18182</scale>'
            + '         <Icon>'
            + '          <href>http://maps.google.com/mapfiles/kml/pushpin/ylw-pushpin.png</href>'
            + '   </Icon>'
            + '<hotSpot x="20" y="2" xunits="pixels" yunits="pixels"/>'
            + '        </IconStyle>'
            + '     <LabelStyle>'
            + '      <color>ff0000ff</color>'
            + '        </LabelStyle>'
            + ' </Style>'
            + '    <Placemark>'
            + '        <styleUrl>#msn_ylw-pushpin</styleUrl>'
            + '     <Point>'
            + '      <coordinates>' + str(longitude) + ',' + str(latitude) + ',0</coordinates>'
            + '        </Point>'
            + '    </Placemark>'
            + '</Document>'
            + '</kml>')

def main():
    pos = getGpsPosition()
    
    # print header (and header - content separator newline)
    print('')
    
    # print content
    if(pos == None):
        print('Can\'t fetch GPS position.')
    else:
        kml = generateKml(pos.longitude, pos.latitude)
        
        print(kml)
    
if __name__ == '__main__':
    main()

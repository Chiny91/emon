#!/usr/bin/python
# New batteries in emon 21/3/17
# nohup /home/pi/emon/emondata.py >> /home/pi/emon/Data/emon.log 2>&1 &

# Import some modules
import os       # Used for filer operations
import rrdtool
import serial
import re       # Used for string searching

# Create database if it does not exist
if not (os.path.isfile('/home/pi/emon/Data/emon.rrd')):
    rrdtool.create(
        "/home/pi/emon/Data/emon.rrd",
        "--step", "60",
        "--start", 'now',
        # DS:variable_name:DataSourceType:heartbeat (twice step):min:max
        "DS:Itemp:GAUGE:120:-10:40",
        "DS:Ihumid:GAUGE:120:0:100",
        # RRA:ConsolidationFunction:xff:step:rows
        "RRA:AVERAGE:0.5:1:2880",
        "RRA:AVERAGE:0.5:10:52560"
    )
    print "New database created"

# Set up the GPIO serial port
port = serial.Serial("/dev/ttyAMA0", 38400, timeout=0.5)

# Go round loop forever
while True:

    # Get a line of data where emonTH line ends with ")"
    response = ""
    eol = ")"
    while True:
        if response.endswith(eol):
            break
        else:
            response += port.read(1)
            
    # Remove first and last characters which may be junk,
    # using Python's slice notation
    response = response[1:-1]
    
    # Break up data into individual parameters
    parameters = re.findall('\d+', response)
    
    # Do the sums
    # https://community.openenergymonitor.org/t/emonth-data-output/3557/2
    temperature = (int(parameters[1])+int(parameters[2])*256)/10.0
    if temperature > 32768:
        temperature = temperature - 65536
    humidity = (int(parameters[5])+int(parameters[6])*256)/10.0
    batteryvolts = (int(parameters[7])+int(parameters[8])*256)/10.0
    rssi = -int(parameters[13])
    
    # Test everything
    import datetime
    print (datetime.datetime.now()), temperature, humidity, batteryvolts, rssi
    
    # Flush serial buffer
    # port.flushInput()
    
    # Update the database
    rrdtool.update(
        "/home/pi/emon/Data/emon.rrd",
        # https://stackoverflow.com/questions/30140845/insert-data-into-rrdtool-from-tcp-stream
        "N:%s:%s" %(temperature, humidity)
        # rrd_update('example.rrd', 'N:%s:%s' %(metric1, metric2));
    )

# Python appears to need a line with same indent as the program start
raise SystemExit

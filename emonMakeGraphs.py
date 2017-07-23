#!/usr/bin/env python
# -*- coding: latin-1 -*-

# Log in as pi
# ./emon/emonMakeGraphs.py

# Import required module/s
import rrdtool

rrdtool.graph(
    "/home/pi/emon/Data/emon.png",
    "--end", "now",
    "--start", "end-86200s",
    "--width", "1200",
    "--height", "480",
    "--disable-rrdtool-tag",    # Deletes rrdtool author from vertical axis
    "--watermark", "Copyright 2017 G4FRO. All rights reserved.",
    "--title", "Environment data",
    "--vertical", "temperature °C",
    # [--right-axis scale:shift]
    "--right-axis", "2:0",
    "--right-axis-label", "relative humidity %",
    
    # DEF: fetches data from a .rrd database
    # vname can be used for rest of program
    # rrdtool will select suitable RRA automagically
    # DEF:<vname>=<rrdfile>:<ds-name>:<CF>[:fancy options]

    # Temperature
    "DEF:vtemp=/home/pi/emon/Data/emon.rrd:Itemp:AVERAGE",
    # LINE[width]:value[#color][:fancy options]
    "LINE1:vtemp#009900:""Temperature",
    
    # Humidity
    "DEF:vhumid=/home/pi/emon/Data/emon.rrd:Ihumid:AVERAGE",
    "CDEF:scaled_vhumid=vhumid,0.5,*",
    "LINE1:scaled_vhumid#FF9900:""Humidity",
    "COMMENT:\\n",
    
    # Draw line for maximum temperature for central heating
    "HRULE:21#ff0000:Maximum",
    
    # Draw line for minimum temperature for central heating
    "HRULE:18#005199FF:Minimum temperature for central heating",
    "COMMENT:\\n",
    
    "COMMENT:Comfort temperature is between 18ºC (blue line) and 21ºC (red line)"
    
)

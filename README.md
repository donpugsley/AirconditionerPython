Pugsley notes on homedatalogger package
=======================================

Oct 2021

Working directory is /home/pugsley/code/AC

homedatalogger.py runs every 10 minutes using a CRON job, scraping house AC,
temperature, and humidity data and appending it to homedata.log.

Example cron for 10 minute intervals:

\# m h dom mon dow   command
*/10 * * * * /home/pugsley/anaconda3/bin/python /home/pugsley/homedatalogger.py >> /home/pugsley/hdl.log

The data source for AC info is the upstairs MyInfinity thermostat, set
to use a local Infinitude server as a proxy.  Infinitude
(https://www.github.com/nebulous/infinitude) grabs a copy of the data
on the way through to the manufacturer's site, allowing normal control
with WiFi apps.  The data can be viewed and/or scraped from the
Infinitude server, running locally at http://192.168.1.202:3000 .  

The data source for temperature and humidity is a suite of WirelessTag
( https://my.wirelesstag.net/ ) temp/humidity tags; two tag managers
are used to provide data from 8 locations, and the wirelesstag.net
site API is used to retrieve the most recent data.

Timestamped lines are saved into homedata.log... plotting is done by
plot-homelogger-data.py, which takes a number of hours as a parameter.
The entire homedata.log file is read and parsed, and a matplotlib plot
of data for the requested number of hours back from the present is
displayed.

Recent change, attempting to serve the results to wifi devices in the
house... added a call to plot-homelogger-data.py to the end of
homedatalogger.py, so every time new data is saved a new pair of JPG
plot files will be generated.  These plot files can then be viewed
using a dead simple HTTP server from anything inside the house
firewall.  Various versions of the HTTP server are being tried.

NEXT STEPS:
Once a server is configured to run at boot time, additional
device-specific (small screen) versions of the plot can be added, also
perhaps a "what the F*&% is the AC on for" status plot.  The file name
will select the type of plot, no server smarts or HTML programming
will be required.

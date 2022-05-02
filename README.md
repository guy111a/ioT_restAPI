# ioT_restAPI
**The goal of the project:**
Showing near live data from ioT sensors


22-April-2022
This weekend project came as a work in progress, as i was playing around with my new ocylloscop
Trying to measure wave patterns out of my raspberry pi zero /w.

Those attempts led to connecting a sensor to the sbc and since i already have a sensor i might as well collect some data with it.
Since we have data, we need a db and one thing led to another and i find myself building a web_app to show this data.

The ETL ( currently) consists of two raspberry pi units 

One zero /w connected to the sensor, left abandoned outside. Running a data_collector, connected to the home wifi and using a request to connect to restAPI.

The second rpi is 4 with 4 gb serving as a samba / octoprint/ gp server at home.
Running docker containers of: mariaDB, mongoDB octoprint, nginx and python flask web_app.
This web_app/web_service is used as a restAPI to serve in/out access to the mariaDB.
Also serving the web page hosting the graph of weather data.

There are things i will change, but as it is. The system is fully operational.

Features:
* Write new data
* Read[all data/day(s) data/ between timestamps data]
* Max / Min / AvG : temperature [ all data / day(s) data / between timestamps data]
* Save to file (csv), [all data / between timestamps / day(s)]
* Count number of loggings 
* Draw chart of : [day(s) / all data / between timestamps data / last data]
* The chart page is auto refreshing each 60 seconds.

keep checking as things are changing !


2-May-2022
New Addition, RPI zero /w,  equipped with LCD (16x2) as an independent ‘client’ for reading the information of last reading.
Showing the current time, Temp, Humidity and the Light (0-99%)
Auto refreshing once per 60 sec.

In order to add some complexity, the ‘client’ is reading the information from a MongoDB container holding the last reading only, timed script is running each minute and selecting the last row from MariaDB and storing this record set into MongoDB.

import sys
import RPi.GPIO as GPIO
import os
from time import sleep
import Adafruit_DHT
import time
import urllib2
import urllib
import MySQLdb
import time
import datetime
DEBUG = 1
# Define GPIO pin to which DHT11 is connected
DHTpin = 4
GPIO.setmode(GPIO.BCM)
myDelay=5
#change IP address whenever connected to a MySQL server
con = MySQLdb.connect(&#39;172.17.1.132&#39;,&#39;root&#39;,&#39;&#39;,&#39;temperature&#39;);
cursor = con.cursor()


def getSensorData():
	ts = time.time()
	localtime = datetime.datetime.fromtimestamp(ts).strftime(&#39;%Y-%m-%d %H:%M:%S&#39;)
	#localtime = time.asctime( time.localtime(time.time()) )
	#print &quot;|Temperature\t| Humiditiy|&quot;;
	humidity, temperature =Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, DHTpin)
	if humidity is not None and temperature is not None:
		print (&quot;Time : {0}\t Temperature : {1:0.1f}*C\t Humidity: {2:0.1f}%&quot;.format(localtime,temperature, humidity))
		cursor.execute(&quot;INSERT INTO `data` (`timestrap`,`temperature`, `humidity`) VALUES(%s,%s,%s)&quot;,(localtime,temperature,humidity))
		con.commit()
		#f = { &#39;timestrap&#39; : localtime, &#39;temp&#39; :
		temperature,&#39;hum&#39;:humidity}
		params = [(&#39;timestrap&#39;,localtime), (&#39;temp&#39;,temperature),(&#39;hum&#39;,humidity)]
		para=urllib.urlencode(params)
		#print para
		url=&quot;http://192.168.0.113/Sensor/insert.php?&quot;+para

		#req=urllib2.Request(&quot;http://192.168.0.113/Sensor/insert.php?{0}&quot;.format(para))
		#print url
		#req=urllib2.Request(url)
		#print req
		#urllib.urlopen(Request(str(self.url)))
		#TWF=((9.0/5*temperature)+32)
		#print(&#39;TempF={0:0.1f}*F&#39;.format(TWF))
	else:
		print(&#39;Failed to get reading. Try again!&#39;)
		return (str(humidity), str(temperature))


def main():
	print &#39;starting...&#39;
	while True:
		try:
			#print &quot;Reading Sensor Data now&quot;
			print &quot;&quot;
			#print &quot;TEMPERATURE HUMIDITY&quot;
			RHW, TW = getSensorData()
			#print TW + &quot; &quot; + TWF+ &quot; &quot; + RHW + &quot; &quot;
			sleep(int(myDelay))
		except Exception as e:
			print e
			print &#39;exiting.&#39;
			break


# call main
if __name__ == &#39;__main__&#39;:
	main()

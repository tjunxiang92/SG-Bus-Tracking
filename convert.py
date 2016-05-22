# route_id
# route_name
# trace_id
# bus_id
# bus_name
# xx
# yy
# lon
# lat
# speed
# left_pixel_icon
# top_pixel_icon
# stat
# isc_distance
# datetime
from datetime import datetime, timedelta
import xmltodict
import sqlite3
import os

conn = sqlite3.connect('ntu.sqlite3')
c = conn.cursor()

table = "CREATE TABLE ntubus(id INTEGER PRIMARY KEY,route_id           TEXT    NOT NULL,route_name           TEXT    NOT NULL,trace_id           TEXT    NOT NULL,bus_id           TEXT    NOT NULL,bus_name           TEXT    NOT NULL,xx           TEXT    NOT NULL,yy           TEXT    NOT NULL,lon           TEXT    NOT NULL,lat           TEXT    NOT NULL,speed           TEXT    NOT NULL,left_pixel_icon           TEXT    NOT NULL,top_pixel_icon           TEXT    NOT NULL,stat           TEXT    NOT NULL,isc_distance           TEXT    NOT NULL,datetime           TEXT    NOT NULL);"
c.execute(table)


filenames = os.listdir('NTUBusData')
total_len = len(filenames)
for k, filename in enumerate(filenames):
	#if total_len % 100 == 0:
	print '%i%% Done. %s' % (k * 100 / total_len, filename)

	# Change Time
	d = datetime.strptime(filename[:-4], '%d%m%y-%H%M%S')
	new_d = d + timedelta(hours=12)
	new_time = new_d.strftime("%d%m%y-%H%M%S")


	f = open('NTUBusData/' + filename, 'r')
	data = f.read()
	f.close()

	dic = xmltodict.parse(data)
	if dic['current_position'] is None or 'error' in dic['current_position']:
		print 'Skipped'
		continue

	busObj = []
	try:
		for i in dic['current_position']['device']:
			i[u'@datetime'] = new_time
			busObj.append(i.values())
	except:
		dic['current_position']['device'][u'@datetime'] = new_time
		busObj.append(dic['current_position']['device'].values())

	#print busObj
	keys = "id, route_id, route_name, trace_id, bus_id, bus_name, xx, yy, lon, lat, speed, left_pixel_icon, top_pixel_icon, stat, isc_distance, datetime"
	values = ','.join(['?']*len(busObj[0]))

	sql = 'INSERT INTO ntubus (%s) VALUES (NULL,%s)' % (keys, values)
	c.executemany(sql, busObj)


conn.commit()
conn.close()
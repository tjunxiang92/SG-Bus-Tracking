from burp import *
import time

a = """
POST /busbuzz/v1/bus_stops/search2 HTTP/1.1
userid: 160200
secret: ad1548d6791f37c15642a086966ab3f3d80919a6
Content-Type: application/json; charset=UTF-8
Content-Length: 74
Host: by.originally.us
Connection: close
Accept-Encoding: gzip
User-Agent: okhttp/2.2.0

{"os_type":2,"os_version":23,"ver":"73.0","os":"android","keywords":"199"}
"""

r = code('https', a)
b = r.json()
b['extras'][0]['tab_name']

c = """
GET /busbuzz/v1/buses2/get_arrival/%s?os_type=2&os_version=23&ver=73.0&os=android HTTP/1.1
userid: 160200
secret: ad1548d6791f37c15642a086966ab3f3d80919a6
Host: by.originally.us
Connection: close
Accept-Encoding: gzip
User-Agent: okhttp/2.2.0

""" 

# Process Bus Stops
bus_stops = b['extras'][0]['bus_stops']

tracking_bus = 27051#bus_stops[1]['id'] # Bus Stop ID

for i, bus_stop in enumerate(bus_stops):
	bid = bus_stop['id']
	if not tracking_bus == bid:
		continue

	while True:
		cc = c % (bus_stop['id'])
		timings = code('https', cc).json()
		for timing in timings:
			if not timing['service_number'] == 199:
				continue

			eta = timing['timing'][0]['etaText']
			if eta == 0:
				try:
					tracking_bus = bus_stops[i + 1]['id'] # Next ID
				except:
					print 'Back to Interchange. Ending...'
					exit()

			print '%s: %s' % (bus_stop['bus_stop_name'], eta)

		# Move next stop
		if not tracking_bus == bid:
			break
		time.sleep(20)

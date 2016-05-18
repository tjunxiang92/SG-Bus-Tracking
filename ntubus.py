from burp import *
import time

wait_time = 5 # 5 seconds

a = """
GET /ntubus/index.php/main/getCurrentPosition HTTP/1.1
Host: campusbus.ntu.edu.sg
Accept: */*
Accept-Language: en
User-Agent: Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0)
Connection: close

"""

while True:
	r = code('http', a)
	if r is None:
		continue

	f = open('NTUBusData/' + time.strftime("%d%m%y-%H%M%S") + '.txt', 'w')
	f.write(r.text)
	f.close()
	
	print time.strftime("%d%m%y-%H%M%S")
	time.sleep(wait_time)
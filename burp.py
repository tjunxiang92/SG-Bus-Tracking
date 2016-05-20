import requests
retries = 3
timeout = 10

def code(proto, text):
	d = text

	d = d.strip().split('\n')
	header = d[0].split(' ')



	# Crop out data
	data = {}
	for i in d[1:]:
		if i == '':
			break

		h = i.split(': ')
		data[h[0]] = h[1]

	base_url = d[0]
	data_type = header[0] # Type
	url_params = header[1] # Url

	url = "%s://%s%s" % (proto, data['Host'], url_params)

	r = None
	for i in range(retries):
		try:
			if header[0] == 'GET':
				r = requests.get(url, headers=data, timeout=timeout)
			else:
				r = requests.post(url, headers=data, data=d[-1], timeout=timeout)
			break
		except:
			pass

	return r
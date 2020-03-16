#	PYTOR
#	Lightweight wrapper for web scraping on the Tor network
#	Brad Heath, brad.heath@gmail.com, @bradheath
#
# 	REQUIREMENTS
#	- Functioning (and active) TOR proxy
#	- SocksiPy (socks.py installed to lib/site-packages)
#	- Stem (pip install stem)
#	- Mechanize
#
#

import stem
from stem.control import Controller
from stem import Signal
import datetime
import requests

import socks 
import socket

class pytor:

	def __init__(self, password=''):
		self.password = password
		self.port = 9050 
		
		self.init_socks()
		self.torControl = Controller.from_port(port=9051)
		self.refresh_identity()		
		self._last_id_time = datetime.datetime.now()
		
	### init methods 

	def init_socks(self):
		socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, 
			'127.0.0.1', self.port)
		socket.socket = socks.socksocket

	def refresh_identity(self):
		with self.torControl as controller:
			controller.authenticate(self.password)
			controller.signal(Signal.NEWNYM)
		self._connected = True

	def get(self, url, timeout=30):		
		self._checkIdentityTime()
		r = requests.get(url, timeout=timeout)
		
		if r.status_code == 200:
			return r.text
		else:
			return "BAD REQUEST"
	
	"""	
	def saveLastResult(file):
		with open(file, 'wb') as local_file:
			local_file.write(self._last_result)
		
	def downloadFile(self, url, file):
		self._checkIdentityTime()
		r = requests.get(url, stream = True)
		with open(file, 'wb') as local_file:
			for chunk in r.iter_content ( chunk_size = 1024):
				if chunk:
					local_file.write(chunk)
		self._last_request = url
		return True
	"""

	def newIdentity(self):
		self.refresh_identity()
		self.init_socks()
		print('new identity')
		self._last_id_time = datetime.datetime.now()
		return True

	def _checkIdentityTime(self):
		if self._id_time != None and self._last_id_time != None:
			if (datetime.datetime.now() - self._last_id_time).seconds >= self._id_time:
				print('Getting new identity')
				self.newIdentity()
		
	def identityTime(self, time = 600):
		self._id_time = time
		

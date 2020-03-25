# Grab a user's parameters
	# Phone Number
	# Year (default: 2017)
	# Semester (default: spring)
	# Subject (course abbreviation)
	# Course (course number)
# Randomly space out time b/w API calls (rate limit or nah?)
	# 'http://courses.illinois.edu/cisapp/explorer/schedule/' + year + '/' + semester + '/' + subject + '/' + course + '.xml?mode=detail'
	# Use lxml to parse the XML file
# Check for a change in enrollment status
	# Log the <enrollmentStatus> from previous API call and compare w/ current call
		# Closed, Open, Open (Restricted)
# If there is a change, send a txt msg notification (using Twilio) with details

import time
import random
# import urllib.request # Py3
from xml.etree import ElementTree as ET
from twilio.rest import TwilioRestClient as TRC

###############GLOBALS###############

ACCOUNT_SID = "ACd5f8f32c2bac16c75345c5a8ea89372c" 
AUTH_TOKEN = "0d0467d5959050e6a31b991f54221021" 

client = TRC(ACCOUNT_SID, AUTH_TOKEN) 

counter = range(1, 8)

phone = input('Enter your phone number (no space): ') # Py3
year = input('Enter the term year: ') # Py3
semester = input('Enter the semester: ') # Py3
subject = input('Enter the subject (course abbreviation): ') # Py3
course = input('Enter the course number: ') # Py3

url = 'http://courses.illinois.edu/cisapp/explorer/schedule/' + str(year) + '/' + semester + '/' + subject + '/' + course + '.xml?mode=detail'
root = ET.parse(urllib.request.urlopen(url)).getroot()

###############MAIN###############

while True:
	log = {}
	pres = {}
	result = {'Subject': subject, 'CourseNum': course, 'SectionNum': '', 'Status': '', 'OGStatus': ''}

	for child in root:
		if child.tag == 'detailedSections':
			for node in child:
				for sub in node:
					if sub.tag == 'sectionNumber':
						section = str(sub.text)
					if sub.tag == 'enrollmentStatus':
						log[section] = sub.text

	print(log)

	time.sleep(60*(random.choice(counter)))

	for child in root:
		if child.tag == 'detailedSections':
			for node in child:
				for sub in node:
					if sub.tag == 'sectionNumber':
						section = str(sub.text)
					if sub.tag == 'enrollmentStatus':
						pres[section] = sub.text

	print(pres)
	print('')

	if len(log) == len(pres):
		for key in pres:
			if pres[key] != log[key]: # Enrollment status doesn't match
				client.messages.create(
					to = '+1' + str(phone),
					from_ = '+12397917242',
					#messaging_service_sid = 'MGd4c29ba82fb88c08abaad23c1fb0937a',
					body = subject + " " + course + ", Section " + key + " has changed from " + log[key] + " to " + pres[key]
				)
				print(subject + " " + course + ", Section " + key + " has changed from " + log[key] + " to " + pres[key])
				print('')
	"""
	client.messages.create(
		to = '+1' + str(phone),
		from_ = '+18666120259',
		body = subject + " " + course + ", Section " + 'D1' + " has changed from " + 'Closed' + " to " + 'Open (restricted)'
	)
	print(subject + " " + course + ", Section " + 'D1' + " has changed from " + 'Closed' + " to " + 'Open (restricted)')
	"""
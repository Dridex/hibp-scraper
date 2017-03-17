#!/usr/bin/python

# Python import
import requests
import json
import logging
import smtplib
import sys
import os.path

# Personal import
import hibpScrape

logging.basicConfig(filename='/var/log/hibp/hibp.log',level=logging.DEBUG,format='%(asctime)s %(message)s')

def sendEmail():

	pwnedAccounts = hibpScrape.scrapeTotal()

	sender = ''
	receivers = ['']

	message = """From: hibp script <test@test.com>
To: Test <test@test.com>
Subject: New breach in HIPB!

New breach loaded in hibp database. See below.
			""" + '\n'

	for site in newbreach:
		for pwn in pwnlist:
			if pwn['Name'] == site:
				message += 'Name: ' + site + '\n'
				message += 'Domain: ' + str(pwn['Domain']) + '\n'
				message += 'Size: ' + str(pwn['PwnCount']) + '\n'
				message += 'Description:' + str(pwn['Description'].encode('utf-8')) + '\n\n'

	with open(pwnpath) as c:
		pwncount = sum(1 for _ in c)
	message += 'Total breaches: ' + str(pwncount) + '\n'
	message += 'Total pwned accounts: ' + str(pwnedAccounts) + '\n'

	try:
		smtpObj = smtplib.SMTP('localhost')
		smtpObj.sendmail(sender, receivers, message)         
		logging.info("Successfully sent email notification")
	except SMTPException:
		logging.error("Error: unable to send email")


if __name__ == '__main__':

	pwnpath = '/opt/hibp/pwn.txt'
	if not os.path.isfile(pwnpath):
		logging.warning('pwn.txt not found, creating new file: ' + pwnpath)
		pwnfile = open(pwnpath, "w")
		r = requests.get('https://haveibeenpwned.com/api/v2/breaches')
		if not r.status_code == 200:
			logging.error('Problem with request, exiting.')
			sys.exit(1)
		pwnlist = r.json()
		for pwn in pwnlist:
			title = pwn['Name'].encode('utf-8') 
			pwnfile.write(title + '\n');
		pwnfile.close()
	else: 
		pwnfile = open(pwnpath, "a+")
		pwnfile.seek(0)
		currentlist = pwnfile.readlines()			
		cliststrip = []
		for item in currentlist:	
			cliststrip.append(item.strip())
		r = requests.get('https://haveibeenpwned.com/api/v2/breaches')
		if not r.status_code == 200:
			logging.error('Problem with request, exiting.')
			sys.exit(1)
		pwnlist = r.json()
		newlist = []
		for pwn in pwnlist:
			newlist.append(pwn['Name'].encode('utf-8'))

		c = set(cliststrip)
		n = set(newlist)
		newbreach = list(n - c)

		if newbreach:
			logging.info('New breach(es)! Writing to file...')
			for item in newbreach:
				pwnfile.write(item + '\n');
			pwnfile.close()
			sendEmail()
		else:
			logging.info('No change.')

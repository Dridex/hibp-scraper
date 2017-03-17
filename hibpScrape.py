#!/usr/bin/python

import requests


def scrapeTotal():

	r = requests.get('https://haveibeenpwned.com')

	summary = []
	indexStr = str(r.text)
	index = indexStr.split('\n')

	count = 0
	while count < (len(index)-1):
	#for line in index:
		if 'pwnedSummaryRow' in index[count]:
			summary.append(index[count+1])
			summary.append(index[count+2])
			summary.append(index[count+3])
			summary.append(index[count+4])
		count += 1

	accountLine = ''
	for line in summary:
		if 'pwned accounts' in line:
			accountLine = line

	halfWay = accountLine.split("pwnSummaryCount\">",1)[1]
	pwnTotal = halfWay.split("</span>",1)[0]
	return pwnTotal


if __name__ == '__main__':

	total = scrapeTotal()
	print total

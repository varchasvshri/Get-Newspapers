import urllib.request, urllib.error, urllib.parse
from bs4 import BeautifulSoup
import ssl
import requests
import regex as re
import os
from datetime import date, timedelta
import shutil

today = date.today()

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def is_downloadable(url):
    """
    Does the url contain a downloadable resource
    """
    h = requests.head(url, allow_redirects=True)
    header = h.headers
    content_type = header.get('content-type')
    if 'text' in content_type.lower():
        return False
    if 'html' in content_type.lower():
        return False
    return True

newspaper = dict({'Economic_times':'https://dailyepaper.in/economic-times-epaper-pdf-download-2020/', 'Times_of_India':'https://dailyepaper.in/times-of-india-epaper-pdf-download-2020/',
	'Financial_Express':'https://dailyepaper.in/financial-express-epaper-pdf-download-2020/', 'Deccan_Chronicle':'https://dailyepaper.in/deccan-chronicle-epaper-pdf-download-2020/',
	'The_Telegraph':'https://dailyepaper.in/the-telegraph-epaper-pdf-download-2020/', 'The_Pioneer':'https://dailyepaper.in/the-pioneer-epaper-pdf-download-2020/',
	'Business_Line':'https://dailyepaper.in/business-line-epaper-pdf-download-2020/', 'Indian_Express':'https://dailyepaper.in/indian-express-epaper-pdf-download-2020/',
	'Hindustan_Times':'https://dailyepaper.in/hindustan-times-epaper-pdf-free-download-2020/', 'The_Hindu':'https://dailyepaper.in/the-hindu-pdf-newspaper-free-download/',
	'Dainik_Jagran':'https://dailyepaper.in/dainik-jagran-newspaper-pdf/', 'Dainik_Bhaskar':'https://dailyepaper.in/dainik-bhaskar-epaper-pdf-download-2020/',
	'Amar_Ujala':'https://dailyepaper.in/amar-ujala-epaper-pdf-download-2020/'})

serial_num = dict({1:'Economic_times', 2:'Times_of_India', 3:'Financial_Express', 4:'Deccan_Chronicle', 5:'The_Telegraph', 6:'The_Pioneer', 7:'Business_Line', 
	8:'Indian_Express', 9:'Hindustan_Times', 10:'The_Hindu', 11:'Dainik_Jagran', 12:'Dainik_Bhaskar', 13:'Amar_Ujala'})

print("The following Newspapers are available for download. Select any of them by giving number inputs - ")
print("1. Economic Times")
print("2. Times of India")
print("3. Financial Express")
print("4. Deccan Chronicle")
print("5. The Telegraph")
print("6. The Pioneer")
print("7. Business Line")
print("8. Indian Express")
print("9. Hindustan Times")
print("10. The Hindu")
print("11. Dainik Jagran")
print("12. Dainik Bhaskar")
print("13. Amar Ujala")

serial_index = input('Enter the number for newspapers - ')
serial_index = serial_index.split()
indices = [int(x) for x in serial_index]

for ser_ind in indices:
	url = newspaper[serial_num[ser_ind]]

	req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
	html = urllib.request.urlopen(req).read()
	soup = BeautifulSoup(html, 'html.parser')
	tags = soup('a')
	list_paper = list()

	directory = serial_num[ser_ind]
	parent_dir = os.getcwd()
	path = os.path.join(parent_dir, directory)
	try:
		os.mkdir(path)
	except OSError as error:
		pass
	os.chdir(path)

	for i in range(len(tags)):
		links = tags[i].get('href',None)
		x = re.search("^https://vk.com/", links)
		if x:
			list_paper.append(links)

	print('For how many days you need the '+ serial_num[ser_ind]+' paper?')
	print('i.e. if only todays paper press 1, if want whole weeks paper press 7')
	print('Size of each paper is 5-12MB')
	for_how_many_days = int(input('Enter your number - '))

	for i in range(for_how_many_days):
		url = list_paper[i]

		req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
		html = urllib.request.urlopen(req).read()
		soup = BeautifulSoup(html, 'html.parser')
		tags = soup('iframe')
		link = tags[0].get('src',None)		

		date_that_day = today - timedelta(days=i)

		if is_downloadable(link):
			print('Downloading '+serial_num[ser_ind]+'...')
			r = requests.get(link, allow_redirects=True)
			with open(serial_num[ser_ind]+"_"+str(date_that_day)+".pdf",'wb') as f:
				f.write(r.content)
			print('Done :)')
		else:
			print(serial_num[ser_ind] + ' paper not available for '+ str(date_that_day))
	os.chdir('../')

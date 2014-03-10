import re, requests, praw, time
from bs4 import BeautifulSoup

def get_paragraphs():
	para = ""
	temp = soup.find(id="Biology").next_elements#This gets the right pattern
	for element in temp:
		if element.name == 'p':
			para += element.text
		if element.name =='h2':
			break
	return para

def fix_paragraph(body):
	body = re.sub(r"<\/{0,1}p>", "", body)
	return body

def get_pokemon(url):
	global soup 
	pattern = r'id="Biology"'
	soup = BeautifulSoup(requests.get(url).text)
	in_soup = re.search(pattern, soup.prettify())
	if in_soup != None:
		return fix_paragraph(get_paragraphs())
	else: return False
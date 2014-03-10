import re, requests, praw
from bs4 import BeautifulSoup

get_paragraph = lambda: soup.find(id="Biology").next_element.next_element.next_element.prettify() #This gets the right pattern

def fix_paragraph(body):
	pattern = re.compile(r'(<a href="(.+?)".*?>(.*?)<\/a>)', re.DOTALL)
	while True:
		#[full, link, word]
		matches = re.search(pattern, body)
		if matches == None:
			print "fuck you"
			break
		matches = matches.groups()
		body = re.sub(matches[0], "[%s](http://bulbapedia.bulbagarden.net%s)"%(matches[2].strip(),matches[1]), body)
	body = body.replace("\n", "")
	body = re.sub(r"<\/{0,1}p>", "", body)
	return body


def get_pokemon(url):
	global soup 
	pattern = r'id="Biology"'
	soup = BeautifulSoup(requests.get(url).text)
	in_soup = re.search(pattern, soup.prettify())
	if in_soup != None:
		return fix_paragraph(get_paragraph())
	else: return False
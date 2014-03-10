import re, requests, time
from bs4 import BeautifulSoup

def get_paragraphs():
	para = ""
	temp = soup.find(id="Biology").next_elements
	for element in temp:
		if element.name == 'p':
			para += ">" + re.sub(r"<\/{0,1}p>", "", element.prettify().replace("\n", ""))+ "\n\n"
		if element.name =='h2':
			break
	return para

def fix_paragraph(body):
	pattern = re.compile(r'(<a.+?href="(.+?)".*?>(.*?)<\/a>)', re.DOTALL)
	pattern2 = re.compile(r'<a.*?class="extiw"')
	while True:
		#[full, link, word]
		matches = re.search(pattern, body)
		is_external = re.search(pattern2, body)
		if matches == None:
			break
		matches = matches.groups()
		#bulbapedia formats internal links annoyingly, necessitating this
		if is_external:
			body = re.sub(re.escape(matches[0]), "[%s](%s)"%(matches[2].strip(), matches[1]), body)	
		else:
			body = re.sub(re.escape(matches[0]), "[%s](http://bulbapedia.bulbagarden.net%s)"%(matches[2].strip(),matches[1]), body)
	return body

def get_pokemon(url):
	global soup 
	tries = 0
	trying = True
	while trying:
		try:
			pattern = r'id="Biology"'
			soup = BeautifulSoup(requests.get(url).text)
			in_soup = re.search(pattern, soup.prettify())
			if in_soup != None:
				return fix_paragraph(get_paragraphs())
			else: return False
		except (requests.exceptions.ConnectionError):
			if tries >3:
				break
			time.sleep(5)	
			tries += 1
	if not trying:
		return False
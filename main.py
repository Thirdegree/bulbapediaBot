import praw, time, re, pokemon_finder
from collections import deque


r = praw.Reddit(u"Pok\xe9dex by /u/Thirdegree")
done = deque(maxlen=300)


def _login():
	USERNAME = raw_input("Username?\n> ")
	PASSWORD = raw_input("Password?\n> ")
	r.login(USERNAME, PASSWORD)
	return USERNAME

def find_pokelink(body):
	pattern = "("+re.escape("http://bulbapedia.bulbagarden.net/wiki/")+"([\w]+)_\(Pok(\xe9|e|\%C3\%A9|)mon\))"
	#(link, pokemon name, random extra string for e)
	is_link = re.search(pattern, body)
	if is_link != None:
		return is_link.groups()[:2]
	else: return (False, False)

def get_poke_info(body):
	link, poke_name = find_pokelink(body)
	if not link:
		return (False, False)
	para = pokemon_finder.get_pokemon(link)
	return (link, para, poke_name)

def main():
	comments = r.get_comments("Thirdegree")
	for post in comments:
		if post.id not in done:
			done.append(post.id)
			link, para, poke_name = get_poke_info(post.body)
			if not para:
				continue
			post.reply("[**%s**](%s)\n\n%s"%(poke_name, link, para))


if __name__ == '__main__':
	
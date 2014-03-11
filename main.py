import praw, re, pokemon_finder
from collections import deque
from time import sleep


r = praw.Reddit("Pokedex by /u/Thirdegree")
done = deque(maxlen=300)


def _login():
	USERNAME = raw_input("Username?\n> ")
	PASSWORD = raw_input("Password?\n> ")
	r.login(USERNAME, PASSWORD)
	return USERNAME

def find_pokelink(body):
	body = body.replace("\\", "")
	pattern = "("+re.escape("http://bulbapedia.bulbagarden.net/wiki/")+"([\w]+)_\(Pok(\xe9|e|\%C3\%A9|)mon\))"
	#(link, pokemon name, random extra string for e)
	is_link = re.search(pattern, body)
	if is_link != None:
		return is_link.groups()[:2]
	else: return (False, False)

def get_poke_info(body):
	link, poke_name = find_pokelink(body)
	if not link:
		return (False, False, False)
	para = pokemon_finder.get_pokemon(link)
	return (link, para, poke_name)

def main():
	comments = r.get_comments("Thirdegree")
	for post in comments:
		if post.id not in done and post.author.name != USERNAME:
			done.append(post.id)
			link, para, poke_name = get_poke_info(post.body)
			if not para:
				continue
			print poke_name + ", " + link
			link = link.replace("(", "\\(").replace(")", "\\)")
			reply_post = "[**%s**](%s)\n\n%s\n\n"%(poke_name, link, para)
			reply_post += "[Author](/u/Thirdegree) | [Source](http://github.com/thirdegree/bulbapediaBot) | Posts deleted if comment score is negative"
			post.reply(reply_post)
			sleep(2)

def check_scores():
	me = r.get_redditor(USERNAME)
	comments = me.get_comments(limit = 100)
	for post in comments:
		#print post.score
		if post.score<=(-1):
			post.delete()
			sleep(2)
	sleep(2)

if __name__ == '__main__':
	Trying = True
	while Trying:
		try:
			USERNAME = _login()
			Trying = False
		except praw.errors.InvalidUserPass:
			print "Invalid Username/password, please try again."
	running = True
	while running:
		try:
			print "tick"
			check_scores()
			for i in xrange(3):
				main()
				sleep(5)
			sleep(10)
		except praw.errors.RateLimitExceeded:
			print "Rate limit exceeded, sleeping 10 min"
			sleep(590)
		except KeyboardInterrupt:
			running = False
		except Exception as e:
			print e
			sleep(50)
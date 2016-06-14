import utils
from textteaser import TextTeaser

def tag_message(msg, tag):
	indent = ' ' * (len(msg['personEmail']) + 2)
	return tag + ': ' + msg['text'].replace('\n', '\n{}'.format(tag+': ')).rstrip() + '\n'

def compile_messages(user, room_name):
	text, email_with_users = '', utils.get_emails_with_users(user, room_name)
	for msg in reversed(utils.get_messages_for_user(user, room_name)['items']):
		text += tag_message(msg, email_with_users[msg['personEmail']])
	return text.rstrip()

def indent_tagged(text, tags):
	last_tag, indented = '', ''
	for line in text:
		tag = None
		for t in tags:
			if line[:len(t)] == t:
				tag = t
		if tag is None:
			raise Exception("No tag or tag is not in line")
		indent = ' ' * (len(tag) + 2)
		line = line.replace('\n{}'.format(tag+': '), '\n' + indent)
		if last_tag == tag:
			indented += indent + line[len(tag)+2:] + '\n'
		else:
			indented += line + '\n'
			last_tag = tag
	return indented

def summarize(title, user, room_name):
	text = compile_messages(user, room_name)
	tt = TextTeaser()
	return indent_tagged(tt.summarize(title, text), utils.get_emails_with_users(user, room_name).values())
	
print summarize('summary', 'chris', 'Pipeline Discussions')

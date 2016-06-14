 #!/usr/bin/env python -W ignore

import utils
from datetime import datetime
from textteaser import TextTeaser

def tag_message(msg, tag):
	indent = ' ' * (len(msg['personEmail']) + 2)
	return tag + ': ' + msg['text'].replace('\n', '\n{}'.format(tag+': ')).rstrip() + '\n'

def compile_messages(user, room_name, days_limit=None, hours_limit=None, min_limit=None):
	text, email_with_users = '', utils.get_emails_with_users(user, room_name)
	for msg in reversed(utils.get_messages_for_user(user, room_name)['items']):
		if 'text' in msg:
			time = datetime.strptime(msg['created'], '%Y-%m-%dT%H:%M:%S.%fZ')
			diff = abs((datetime.now() - time).days)
			print str(diff) + ' ' + msg['text']
			if days_limit == None and hours_limit == None and min_limit == None or \
				days_limit != None and diff <= days_limit or \
				hours_limit != None and diff * 24 <= hours_limit or \
				min_limit != None and diff * 24 * 60 <= days_limit:
				text += tag_message(msg, email_with_users[msg['personEmail']])
	return text.rstrip()

def indent_tagged(text, tags):
	if text == None:
		None
	if tags == None:
		return text
	last_tag, indented = '', ''
	for line in text:
		tag = None
		for t in tags:
			if line[:len(t)] == t:
				tag = t
		if tag is None:
			indented  = indented.rstrip() + line + '\n'
			continue
		indent = ' ' * (len(tag) + 2)
		line = line.replace('\n{}'.format(tag+': '), '\n' + indent)
		if last_tag == tag:
			indented += indent + line[len(tag)+2:] + '\n'
		else:
			indented += line + '\n'
			last_tag = tag
	return indented

"""
Use get_transcript to get a transcript of chat messages
"""
def get_transcript(user, room_name, days_limit=None, hours_limit=None, min_limit=None):
	return indent_tagged(compile_messages(user, room_name, days_limit, hours_limit, min_limit).splitlines(), \
		utils.get_emails_with_users(user, room_name).values())

"""
Use summarize to summarize chat messages in a room with NLP
"""
def summarize(title, user, room_name, days_limit=None, hours_limit=None, min_limit=None):
	text = compile_messages(user, room_name, days_limit, hours_limit, min_limit)
	tt = TextTeaser()
	return indent_tagged(tt.summarize(title, text), utils.get_emails_with_users(user, room_name).values())

print summarize('cool title', 'chris', 'Hacker Squad', None, 5)
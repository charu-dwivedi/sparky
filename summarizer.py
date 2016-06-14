 #!/usr/bin/env python -W ignore

import utils
from datetime import datetime
from textteaser import TextTeaser

def compile_messages(user, room_name):
    text = ''
    for msg in reversed(utils.get_messages_for_user(user, room_name)['items']):
        text += msg['text'] + '\n'
    return text

def summarize(title, user, room_name):
    text = compile_messages(user, room_name)
    tt = TextTeaser()
    return tt.summarize(title, text)

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
import utils
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

for line in summarize('summary', 'chris', 'Pipeline Discussions'):
    print line


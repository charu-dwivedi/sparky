import utils
from datetime import datetime
import pytz
from textteaser import TextTeaser

def tag_message(msg, tag):
    indent = ' ' * (len(msg['personEmail']) + 2)
    return tag + ': ' + msg['text'].replace('\n', '\n{}'.format(tag+': ')).rstrip() + '\n'

def tag_file(msg, tag):
    text = ''
    for f in msg['files']:
        file_msg = 'FILE: %s' % f
        text += tag + ': ' + 'FILE: {}'.format(f) + '\n'
    return text

def compile_messages(user, room_name, msg_limit=None, days_limit=None, hours_limit=None, min_limit=None):
    text, email_with_users = '', utils.get_emails_with_users(user, room_name)
    now = pytz.utc.localize(datetime.utcnow())
    messages = None
    if not msg_limit:
        messages = utils.get_messages(user, room_name)
    else:
        messages = utils.get_messages(user, room_name, msg_limit)
    if not messages or 'items' not in messages:
        raise Exception('Could not get messages')
    for msg in reversed(messages['items']):
        if 'text' in msg:
            time = pytz.utc.localize(datetime.strptime(msg['created'], '%Y-%m-%dT%H:%M:%S.%fZ'))
            if days_limit == None and hours_limit == None and min_limit == None or \
                days_limit != None and abs((now - time).days) <= days_limit or \
                hours_limit != None and abs((now - time).total_seconds()) // 3600 <= hours_limit or \
                min_limit != None and abs((now - time).seconds) // 60 <= min_limit:\
                text += tag_message(msg, email_with_users[msg['personEmail']])
        """
        if 'files' in msg:
            text += tag_file(msg, email_with_users[msg['personEmail']])
        """
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
def get_transcript(user, room_name, msg_limit=None, days_limit=None, hours_limit=None, min_limit=None):
    return indent_tagged(compile_messages(user, room_name, msg_limit, days_limit, hours_limit, min_limit).splitlines(), \
        utils.get_emails_with_users(user, room_name).values())

"""
Use summarize to summarize chat messages in a room with NLP
"""
def summarize(user, room_name, msg_limit=None, days_limit=None, hours_limit=None, min_limit=None, title=None):
    if title == None:
        title = '%s Summary' % room_name
    text = compile_messages(user, room_name, msg_limit, days_limit, hours_limit, min_limit)
    tt = TextTeaser()
    return indent_tagged(tt.summarize(title, text), utils.get_emails_with_users(user, room_name).values())

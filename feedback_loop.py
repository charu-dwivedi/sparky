from Tkinter import StringVar
import time
import speechtest
import langprocess
import re
#TODO: Import NLP, parser, using black box for now


def uppercase(matchobj):
    return matchobj.group(0).upper()

def capitalize(s):
    return re.sub('^([a-z])|[\.|\?|\!]\s*([a-z])|\s+([a-z])(?=\.)', uppercase, s)


def iterate(top, text):
    user_input = ""
    while not user_input:
        user_input = speechtest.speechrec()
    text.set(user_input)
    langprocess.process(user_input)
    text.set(text.get() +  'You: ' + user_input + '\n\n')
    top.update_idletasks()
    time.sleep(1)
    sparky_output = 'Of course, your meeting is setup.'
    text.set(text.get() + 'Sparky: ' + sparky_output + '\n\n'

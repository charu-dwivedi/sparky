import time
import voice as speech
import re
from Tkinter import StringVar
from speech_processor import process

# TODO: Import NLP, parser, using black box for now

def uppercase(matchobj):
    return matchobj.group(0).upper()

def capitalize(s):
    return re.sub('^([a-z])|[\.|\?|\!]\s*([a-z])|\s+([a-z])(?=\.)', uppercase, s)

def iterate(top, text):
    user_input = ""
    text.set('')
    while not user_input:
    	user_input = speech.speechrec()
    print user_input
    text.set(user_input)
    top.update_idletasks()
    user='charu'
    sparky_output = process(user, user_input, text, top)
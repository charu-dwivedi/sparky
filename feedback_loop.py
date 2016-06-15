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
	langprocess.process('charu', user_input, text)
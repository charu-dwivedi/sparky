from Tkinter import StringVar
import time
import speechtest as speech
import langprocess
import re
import audio_ui as aui
#TODO: Import NLP, parser, using black box for now


def uppercase(matchobj):
    return matchobj.group(0).upper()

def capitalize(s):
    return re.sub('^([a-z])|[\.|\?|\!]\s*([a-z])|\s+([a-z])(?=\.)', uppercase, s)

def iterate(top, text):
    audio_ui = aui.AudioUI(top,text)
    user_input = ""
    text.set('')
    while not user_input:
    	user_input = speech.speechrec()
    text.set(user_input)
    top.update_idletasks()
    sparky_output = langprocess.process(user_input, text, top)
#    audio_ui.respond(sparky_output)

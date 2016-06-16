from Tkinter import StringVar
import time
import speechtest
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
    user_input = audio_ui.listen()
    sparky_output = langprocess.process(user_input)
#    audio_ui.respond(sparky_output)

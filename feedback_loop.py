from Tkinter import StringVar
import time

#TODO: Import NLP, parser, using black box for now

def iterate(top, text):
    user_input = 'Can I set up a meeting?'
    text.set(text.get() +  'You: ' + user_input + '\n\n')
    top.update_idletasks()
    time.sleep(1)
    sparky_output = 'Of course, your meeting is setup.'
    text.set(text.get() + 'Sparky: ' + sparky_output + '\n\n')

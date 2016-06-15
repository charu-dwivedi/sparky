from Tkinter import StringVar
import time
import speechtest
import langprocess
#TODO: Import NLP, parser, using black box for now

def iterate(top, text):
	user_input = ""
	while not user_input:
		user_input = speechtest.speechrec()
	text.set(user_input)
	langprocess.process(user_input)
	'''
    user_input = 'Can I set up a 	meeting?'
    text.set(text.get() +  '	You: ' + user_input + '\n\n')
    top.update_idletasks()
    time.sleep(1)
    sparky_output = 'Of course, your meeting is setup.'
    text.set(text.get() + 'Sparky: ' + sparky_output + '\n\n
    '''
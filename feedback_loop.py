from Tkinter import StringVar
import time
import speechtest
import langprocess
#TODO: Import NLP, parser, using black box for now

def iterate(top, text):
	user_input = speechtest.speechrec()
	text.set(user_input)
	#voice_output = process(user_input)
	speechtest.speech_play_test(user_input)
	speechtest.audio_file_remove()
	'''
    user_input = 'Can I set up a meeting?'
    text.set(text.get() +  'You: ' + user_input + '\n\n')
    top.update_idletasks()
    time.sleep(1)
    sparky_output = 'Of course, your meeting is setup.'
    text.set(text.get() + 'Sparky: ' + sparky_output + '\n\n
    '''
# NOTE: this requires PyAudio because it uses the Microphone class
from gtts import gTTS
import pygame
import speech_recognition as sr
import smtplib
# Import the email modules we'll need
from email.mime.text import MIMEText
import os
import time
import pyvona
from winsound import *
# Open a plain text file for reading.  For this example, assume that
# the text file contains only ASCII characters.

def speech_play_test(voice_output):
     audio_file = "test.mp3"
     tts = gTTS(text=voice_output, lang="en")
     tts.save(audio_file)
     pygame.mixer.init()
     pygame.mixer.music.load(audio_file)
     pygame.mixer.music.play()
     while pygame.mixer.music.get_busy() == True:
         continue
     pygame.mixer.music.stop()
     pygame.mixer.music.load("test2.mp3")

def audio_file_remove():
     audio_file = "test.wav"
     os.remove(audio_file)
     #Cannot remove audio file, have to remove it when entire application close

def speechrec():
    PlaySound('ask.wav', SND_FILENAME)
    r = sr.Recognizer()
    with sr.Microphone() as source:                # use the default microphone as the audio source
        audio = r.listen(source)                   # listen for the first phrase and extract it into audio data
    try:
        banana = r.recognize_google(audio, language = "en-us", show_all=False)   # recognize speech using Google Speech Recognition
        PlaySound('understood.wav', SND_FILENAME)
        return banana
    except:                            # speech is unintelligible
        errormess = "Could not understand audio, please try again"
        speech_play_test(errormess)
        return errormess
'''
receiver = "chrchon@cisco.com"

# me == the sender's email address
# you == the recipient's email address
print "Who would you like to send an email to?"
person = speechrec()
chrisname = "Chris"
if chrisname.lower() in person:
    receiver = "chrchon@cisco.com"
    print "Sending to Chris"

print "What would you like in the message?"
message_body = speechrec()



msg = MIMEText(message_body)

msg['Subject'] = message_body
msg['From'] = "chdwived@cisco.com"
msg['To'] = receiver




# Send the message via our own SMTP server, but don't include the
# envelope header.
s = smtplib.SMTP('localhost')
s.sendmail("chdwived@cisco.com", receiver, msg.as_string())
s.quit()
'''

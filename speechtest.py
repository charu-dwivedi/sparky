# NOTE: this requires PyAudio because it uses the Microphone class
import speech_recognition as sr
import smtplib
from gtts import gTTS
# Import the email modules we'll need
from email.mime.text import MIMEText
import pygame
import os
import time
# Open a plain text file for reading.  For this example, assume that
# the text file contains only ASCII characters.

def speech_rec():
    r = sr.Recognizer()
    with sr.Microphone() as source:                # use the default microphone as the audio source
        audio = r.listen(source)                   # listen for the first phrase and extract it into audio data
    try:
        banana = r.recognize_google(audio, language = "en-us", show_all=False)   # recognize speech using Google Speech Recognition
        print banana
        return banana
    except LookupError:                            # speech is unintelligible
        print("Could not understand audio")
        errormess = "error"
        return errormess


def speech_play_test():
    audio_file = "test.mp3"
    tts = gTTS(text="Hello!", lang="en")
    tts.save(audio_file)
    pygame.mixer.init()
    pygame.mixer.music.load(audio_file)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue

    #Cannot remove audio file, have to remove it when entire application closes
    
speech_rec()

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
from Tkinter import StringVar
import speechtest as speech

class AudioUI:
    class __AudioUI:
        def __init__(self, text, top):
            self.text = text
            self.top = top

        def __update(self, s):
            self.text.set(self.text.get() + s)
            self.top.update_idletasks()

        def clear(self):
            self.text.set('')
            self.top.update_idletasks()

        def get_text(self):
            return self.text.get()

        def listen(self):
            user_input = None
            while not user_input:
                user_input = speech.speechrec()
            print user_input
            self.__update('You: ' + user_input + '\n\n')
            return user_input

        def respond(self, s):
            self.__update('Sparky: ' + s + '\n\n')
            self.top.update_idletasks()
            speech.speech_play_test(str)

    instance = None
    def __init__(self, text, top):
        if not AudioUI.instance:
            AudioUI.instance = AudioUI.__AudioUI(text,top)
        else:
            AudioUI.instance.text = text
    def __getattr__(self, name):
        return getattr(self.instance, name)

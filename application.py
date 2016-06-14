import Tkinter
from PIL import Image, ImageTk
import feedback_loop as fbl

top = Tkinter.Tk()
photo = ImageTk.PhotoImage( Image.open("images\microphone.png"))

label = Tkinter.Label(image=photo)
label.image = photo # keep a reference!
#label.pack()

top.configure(background="white")
top.minsize(width=550, height=700)
top.maxsize(width=550, height=700)

text = Tkinter.StringVar()
text.set('Welcome to the Spark Voice Assistant! Please click the button above and give Sparky a command!\n')
def iterate():
    fbl.iterate(top, text)

button = Tkinter.Button(top, image=photo, command=iterate, bg="#fff", relief="ridge")
button.pack()

message = Tkinter.Message(top, textvariable=text, bg="#fff", width=500)
message.pack()

#Icon used from flaticon.com, author: Freepik

top.mainloop()
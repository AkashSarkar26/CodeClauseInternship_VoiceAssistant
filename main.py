from tkinter import *
from PIL import Image, ImageTk
from assistant import GetAI

# create root window
root = Tk()
# root window title and dimension
root.title("Akash: Your AI assistant")
# Set geometry (widthxheight)
root.geometry('500x400')
 
# all widgets will be here
mic_string_var = StringVar()

chatbox = Text(root, bg="#ededed", fg="black", font=("Arial", 10),
               width=48, height=6, padx=10)
chatbox.config(state=DISABLED)
chatbox.place(relx=0.5, rely=0.7, anchor='center')
 
# chatbox_scrollbar = Scrollbar(chatbox)
# chatbox_scrollbar.place(relheight=1.1, relx=0.99, rely=-0.05)

chatai = GetAI(root=root, status_text_var=mic_string_var, chatbox=chatbox)

# add mic button to the root window
mic_icon_image = Image.open("mic.png")
mic_icon_photo = ImageTk.PhotoImage(mic_icon_image)
mic_button = Button(root, image=mic_icon_photo,
                    command=chatai.generateResponse, height=90, width=90,
                    borderwidth=0)
mic_button.place(relx=0.5, rely=0.25, anchor=CENTER)

# add a label to the root window
mic_string_var.set("Hi, click on the mic to speak")
status_label = Label(root, textvariable=mic_string_var,
                     font=("Arial", 18))
status_label.place(relx=0.5, rely=0.45, anchor='center')


# Execute Tkinter
root.mainloop()


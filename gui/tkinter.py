from Tkinter import *

class App:
    def __init__(self, master):
        frame = Frame(master, width=800, height=200)
        frame.pack()
        frame2 = Frame(master, bd=1, relief=SUNKEN, width=300, height=200)
        frame2.pack()
        self.button = Button(frame, text="quit", command=frame.quit)
        self.button.pack()

        self.label = Label(frame, text="hi there")
        self.label.pack()

root = Tk()
root.title("hello")
app =  App(root)

root.mainloop()
root.destroy()



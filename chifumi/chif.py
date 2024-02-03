from random import * 
from tkinter import *


global window 
window = Tk()
global textvar
textvar = StringVar()
mainLabel = Label(window, textvariable=textvar, width = 25)
mainLabel.place(x = 30, y = 10)
a = ["pierre", "ciseaux", "feuille"]


def getResult(type_):
    global textvar


    computer = randint(0, 2)

    if computer == type_:
        return textvar.set("Egalité avec " + a[computer])
    if type_ == 0:
        if computer == 2:
            textvar.set("Computer à gagné avec " + a[computer])
        else: 
            textvar.set("Vous à gagné avec " + a[type_])
    elif type_ == 1:
        if computer == 0:
            textvar.set("Computer à gagné avec " + a[computer])
        else: 
            textvar.set("Vous à gagné avec " + a[type_])
    elif type_ == 2:
        if computer == 1:
            textvar.set("Computer à gagné avec " + a[computer])
        else: 
            textvar.set("Vous à gagné avec " + a[type_])

 
def createbtns():
    p = Button(window, text="Pierre", width=10, command = lambda v=0: getResult(0))
    f = Button(window, text="feuille", width=10, command = lambda v=0: getResult(2))
    c = Button(window, text="Ciseaux", width=10, command = lambda v=0: getResult(1))
    p.place(x = 50, y = 50)
    f.place(x = 50, y = 80)
    c.place(x = 50, y = 110)



def openWindow():
    window.title("Chifumi")
    window.geometry("250x250")
    createbtns()


openWindow()


window.mainloop()

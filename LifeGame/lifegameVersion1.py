from tkinter import *
import random as random
import math as math

global window
global mainCanvasd
global keepBoxes
global windowData
global x
global y
global isLooping
global domainOfCalculation

isLooping = True
keepBoxes = {}
window = Tk()
windowData = {"windowWidth": 800, "windowHeight": 600, "calculationSpeed": 1000, "probabilitySpawn": 50}
window.geometry("250x800")
window.title("Life")
domainOfCalculation = {"startOn": 0, "endOn": "inf", "keepTrack":0 }
keepBoxes = {}


def _updateTextLocalSing(t, complement):
    global x 
    global y  
    global isLooping

    if isLooping == False:
        return
    
    a = "0"
    b = "0"
    try:
        _ = int(complement[0].get())
        a = str(complement[0].get())
    except:
        a = "0"
    try:
        _ = int(complement[1].get())
        b = str(complement[1].get())
    except:
        b = "0"

    t.set('' + str(complement[0].get()) + 'x' + str(complement[1].get())  + '')
    t.set("" + a + "x" + b)
    a = window.after(100, lambda v=0: _updateTextLocalSing(t, [x, y]))


def _clientHandler_(request, object, complement):
    global isLooping
    if request == 0:
        try:
            complement[0] = int(complement[0].get())
            complement[1] = int(complement[1].get())
            complement[2] = int(complement[2].get())
            complement[3] = int(complement[3].get())
            complement[4] = int(complement[4].get())
            complement[5] = int(complement[5].get())
        except:
            object.set("Invalid Input !")
            return 0
        if complement[0] > 10 and complement[1] > 10 and complement[0] < 4000 and complement[1] < 4000:
            windowData["windowHeight"] = complement[1]
            windowData["windowWidth"] = complement[0]
            windowData["calculationSpeed"] = complement[2]
            windowData["probabilitySpawn"] = complement[3]
            domainOfCalculation["startOn"] = complement[4]
            domainOfCalculation["endOn"] = complement[5]
            window.geometry('' + str(complement[0]) + 'x' + str(complement[1]) + '')
            initForm()
            isLooping = False
            update_init = _intelligent_update_()
            return 0 
        else:
            object.set('Invalid Dimensions !')
            return 1
    


def _init_main__menu():

    global x 
    global y 

    errorText = StringVar()

    errorText.set("Enter Window Dimensions")

    errorLabel = Label(window, textvariable=errorText, width = 20)
    errorLabel.place(x = 50, y = 20)

    holderLabel_x = StringVar()

    holderLabel_x.set("Enter x axis")

    x = holderLabel_x

    dimension_x_holder = Entry(window, textvariable=holderLabel_x, width = 10)
    dimension_x_holder.place(x = 30, y = 70)

    holderLabel_y = StringVar()

    holderLabel_y.set("Enter y axis")

    y = holderLabel_y

    dimension_y_holder = Entry(window, textvariable=holderLabel_y, width = 10)
    dimension_y_holder.place(x = 160, y = 70)

    ValidateHolder = StringVar()

    ValidateHolder.set("Window: '0x0'")

    preview = Label(window, textvariable=ValidateHolder, width = 20)
    preview.place(x = 50, y = 130)

    _ = Label(window, text = "Enter Calculation speed in ms", width = 25)
    _.place(x = 30, y = 180)
    calcSpeedText = StringVar()
    calcSpeedHolder = Entry(window, textvariable=calcSpeedText, width=15)
    calcSpeedHolder.place(x=70, y = 230)

    percentageOfLivabilityText = StringVar()
    percentageOfLivabilityHolder = Entry(window, textvariable=percentageOfLivabilityText, width=15)
    percentageOfLivabilityHolder.place(x= 70, y = 350) 
    _a = Label(window, text = "Enter the probability of a box \n being alive at spawn (in %)", width = 35)
    _a.place(x = -5, y = 300)

    
    holderTextLabel = Label(window, text = "Enter Start Point", width = 15)
    holderTextLabel.place(x=60, y= 420)
    setStartText = StringVar()
    setStartPoint = Entry(window, width = 15, textvariable=setStartText)
    setStartPoint.place(x = 70, y = 450)


    
    holderTextLabel_ = Label(window, text = "Enter End Point", width = 15)
    holderTextLabel_.place(x=60, y= 510)
    EndText = StringVar()
    setEndPoint = Entry(window, width = 15, textvariable=EndText)
    setEndPoint.place(x = 70, y = 550)


    launchPage = Button(window, text='Start Simulation', width = 18, command = lambda v=0: _clientHandler_(0, errorText, [holderLabel_x, holderLabel_y, calcSpeedText, percentageOfLivabilityText, setStartText, EndText]))
    launchPage.place(x = 55, y = 640)


    _updateTextLocalSing(ValidateHolder, [holderLabel_x, holderLabel_y])






def Dispatcher(box):
    box["data"]["isFull"] = not box["data"]["isFull"]







def initForm():
    global window
    global mainCanvas

    mainCanvas = Canvas(window, width=windowData["windowWidth"], height=windowData["windowHeight"], bg='white')

    mainCanvas.place(x = 0, y = 0)

    learnModifications = []

    for i in range(0, (windowData["windowWidth"] // 20)):
        for v in range(0, windowData["windowHeight"] // 20):
            digit = random.randint(0, 100)
            if digit <= windowData["probabilitySpawn"]:
                digit = 1
            else:
                digit = 0
            if digit ==1:
                digit = 1
                rectangle = mainCanvas.create_rectangle(i*20, v*20, (i*20)+20, (v*20) + 20, fill="white")
                keepBoxes['x=' + str(i) + ', y=' + str(v)] = {"position" : {"x" : i, "y" : v}, "data": {"isFull": digit, "boxObject": rectangle}}
                rectangle.bind("<Button-1>", lambda v=0: Dispatcher(keepBoxes))
            else:
                digit = 0
                rectangle = mainCanvas.create_rectangle(i*20, v*20, (i*20)+20, (v*20) + 20, fill="black")
                keepBoxes['x=' + str(i) + ', y=' + str(v)] = {"position" : {"x" : i, "y" : v}, "data": {"isFull": digit, "boxObject": rectangle}}
                rectangle.bind("<Button-1>", lambda v=0: Dispatcher(keepBoxes))

    return learnModifications


def _intelligent_update_():
    
    global keepBoxes
    for i in range(0, windowData["windowWidth"] // 20):
        for v in range(0, windowData["windowHeight"] // 20):
            if keepBoxes["x=" + str(i) + ", y="  + str(v)]["data"]["isFull"] == 0:
                r =  0
                if i - 1 > 0: 
                    if keepBoxes["x=" + str(i - 1) + ", y=" + str(v)]["data"]["isFull"] == True:
                        r = r + 1
                    if v - 1 > 0:
                        if keepBoxes["x=" + str(i - 1) + ", y=" + str(v - 1)]["data"]["isFull"] == True:
                            r = r + 1
                    if v + 1 < windowData["windowHeight"] // 20:
                        if keepBoxes["x=" + str(i - 1) + ", y=" + str(v + 1)]["data"]["isFull"] == True:
                            r = r + 1
                if v - 1 > 0:
                    if i + 1 < windowData["windowWidth"]// 20:
                        if keepBoxes["x=" + str(i + 1) + ", y=" + str(v - 1)]["data"]["isFull"] == True:
                            r = r + 1
                    if keepBoxes["x=" + str(i) + ", y=" + str(v - 1)]["data"]["isFull"] == True:
                        r = r + 1

                if i + 1 < windowData["windowWidth"]// 20:
                    if v + 1 < windowData["windowHeight"]// 20:
                        if keepBoxes["x=" + str(i + 1) + ", y=" + str(v + 1)]["data"]["isFull"] == True:
                            r = r + 1
                    if keepBoxes["x=" + str(i + 1) + ", y=" + str(v)]["data"]["isFull"] == True:
                        r = r + 1
                
                if v + 1 < windowData["windowHeight"]// 20:
                    if keepBoxes["x=" + str(i) + ", y=" + str(v + 1)]["data"]["isFull"] == True:
                        r = r + 1

                if r == 3:
                    
                    keepBoxes["x=" + str(i) + ", y=" + str(v)]["data"]["isFull"] = 1
                    mainCanvas.itemconfig(keepBoxes["x=" + str(i) + ", y=" + str(v)]["data"]["boxObject"], fill="white")
            else:
                r = 0
                if i - 1 > 0: 
                    if keepBoxes["x=" + str(i - 1) + ", y=" + str(v)]["data"]["isFull"] == True:
                        r = r + 1
                    if v - 1 > 0:
                        if keepBoxes["x=" + str(i - 1) + ", y=" + str(v - 1)]["data"]["isFull"] == True:
                            r = r + 1
                    if v + 1 < windowData["windowHeight"] // 20:
                        if keepBoxes["x=" + str(i - 1) + ", y=" + str(v + 1)]["data"]["isFull"] == True:
                            r = r + 1
                if v - 1 > 0:
                    if i + 1 < windowData["windowWidth"]// 20:
                        if keepBoxes["x=" + str(i + 1) + ", y=" + str(v - 1)]["data"]["isFull"] == True:
                            r = r + 1
                    if keepBoxes["x=" + str(i) + ", y=" + str(v - 1)]["data"]["isFull"] == True:
                        r = r + 1

                if i + 1 < windowData["windowWidth"]// 20:
                    if v + 1 < windowData["windowHeight"]// 20:
                        if keepBoxes["x=" + str(i + 1) + ", y=" + str(v + 1)]["data"]["isFull"] == True:
                            r = r + 1
                    if keepBoxes["x=" + str(i + 1) + ", y=" + str(v)]["data"]["isFull"] == True:
                        r = r + 1
                
                if v + 1 < windowData["windowHeight"]// 20:
                    if keepBoxes["x=" + str(i) + ", y=" + str(v + 1)]["data"]["isFull"] == True:
                        r = r + 1

                if r > 3 or r < 2:
                    keepBoxes["x=" + str(i) + ", y=" + str(v)]["data"]["isFull"] = 0
                    mainCanvas.itemconfig(keepBoxes["x=" + str(i) + ", y=" + str(v)]["data"]["boxObject"], fill="black")

    a = window.after(windowData["calculationSpeed"], lambda v=0: _intelligent_update_())


init = _init_main__menu()


window.mainloop()



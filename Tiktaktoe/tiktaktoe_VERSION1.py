from tkinter import *
'../nsi_'

mafenetre = Tk()
mafenetre.geometry("350x350")
moncanevas = Canvas(mafenetre, width=300, height=300, bg="white")
moncanevas.place(x=50,y=60)
global switch
global keepTrackBoxes
keepTrackBoxes = []
switch = 0
global possibleLines
possibleLines = [[[1,1], [2, 1], [3, 1]],[[1,2], [2,2], [3,2]], [[1,3], [2,3], [3,3]], 
[[1,1], [1, 2], [1, 3]], [[2, 1], [2,2], [2,3]], [[3,1], [3, 2], [3,3]], [[1,1], [2,2], 
[3,3]], [[3,1], [2,2], [1,3]]]



def ignition():
    for i in range(0, 10):
        if i < 3:
            moncanevas.create_rectangle(80 * (i+1),80,5,6)
        elif i < 6:
            moncanevas.create_rectangle(80 * (i-2),160,5,6)
        elif i < 9:
            moncanevas.create_rectangle(80 * (i-5),240,5,6)

def getBox(event):
    box = [0, 0, [0, 0, 0, 0]]
    if event.x - 80 < 0:
        box[0] = 1
    elif event.x - 160 < 0:
        box[0] = 2
    elif event.x - 240 < 0:
        box[0] = 3
    else:
        return [0, 0]
    if event.y - 80 < 0:
        box[1] = 1
    elif event.y - 160 < 0:
        box[1] = 2
    elif event.y - 240 < 0:
        box[1] = 3
    else:
        return [0, 0]
    return box
    
def checkLines():
    if len(keepTrackBoxes) < 5:
        return False
    for i in range(0, len(possibleLines)):
        print(possibleLines[i][0])
        if len(possibleLines[i][0]) == 3 and len(possibleLines[i][1]) == 3 and len(possibleLines[i][2]) == 3:
            if possibleLines[i][0][2] == possibleLines[i][1][2] == possibleLines[i][2][2]:
                print("WINNER !")
                return True
    global _z

    _z = False


    for i in range(0, len(possibleLines)):
        tmp_ = 2
        lmCount = 0
        for t in range(0, 3):
            if len(possibleLines[i][t]) == 3:
                lmCount = lmCount + 1
                if tmp_ == 2:
                    tmp_ = possibleLines[i][t][2]
        if lmCount == 0 or lmCount == 1:
            _z = True
    if _z == False:
        print("lost !")
            
            
    return False         

def Dipsatcher(evenement):
    global switch
    global keepTrackBoxes
    box = getBox(evenement)

    for i in range(0, len(keepTrackBoxes)):
        if keepTrackBoxes[i][0][0] == box[0] and keepTrackBoxes[i][0][1] == box[1]:
            return print("box has been used")
    x, y = evenement.x, evenement.y
    keepTrackBoxes.append([[box[0], box[1]], switch])
    for i in range(0, len(possibleLines)):
        for v in range(0, len(possibleLines[i])):
            if possibleLines[i][v][0] == box[0] and possibleLines[i][v][1] == box[1]:
                possibleLines[i][v].append(switch)
    if switch == 0:
        callback = createCross(box)
        switch = 1
    else:
        callback = createCircle(box)
        switch = 0
    checkLines()

moncanevas.bind("<Button-1>", Dipsatcher)

def createCross(box):
    global altern
    toRemovex = 0
    toRemovey = 0
    if box[0] - 1 > 0:
        toRemovex = 5
        toRemovex = 0
    if box[1] - 1 > 0:
        toRemovey = 5
    moncanevas.create_line(80 * box[0], 80 * box[1], 5 + 5 * 16* (box[0] - 1) - toRemovex , 5 + 5 * 16 * (box[1] - 1) - toRemovey)
    moncanevas.create_line(5 + 5 * 16 * (box[0] - 1) - toRemovex, 80 * box[1], 80 * box[0], 5 + 5 * 16 * (box[1] - 1) - toRemovey)
    return True

def createCircle(box):
    toRemovex = 0
    toRemovey = 0
    if box[0] - 1 > 0:
        toRemovex = 5
        toRemovex = 0
    if box[1] - 1 > 0:
        toRemovey = 5
    moncanevas.create_oval(80 * box[0], 80 * box[1], 5 + 5 * 16* (box[0] - 1) - toRemovex , 5 + 5 * 16 * (box[1] - 1) - toRemovey)
    return True


ignition()

mafenetre.mainloop()




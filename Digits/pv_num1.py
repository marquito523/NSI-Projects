from tkinter import *
import random as random

#Reference Variables as Undefined Globally

global codeHolder
global correctCode
global _hasChecked_
global numberOfIntsInPin
global xp
global window
global timer
global keepTimerRecord
global userCredentials

#Reference Global Variables as Defined Gobally
window = Tk()
codeHolder = []
correctCode = []
_hasChecked_ = [True]
numberOfIntsInPin = [1, False]
xp = [0, 500]
timer = [0, 0, 0]
keepTimerRecord = []



def calcXP(levelXP_):
    xp[0] = xp[0] + ((xp[1] * (numberOfIntsInPin[0] - 1)) // (keepTimerRecord[len(keepTimerRecord) - 1][0] + 1)) - keepTimerRecord[len(keepTimerRecord) - 1][1]
    levelXP_[1].set("Level: " + str(numberOfIntsInPin[0]) + "\n Exp: " + str(xp[0]) + 'xp')
    return True

def _nonFatalError(fail):
    print('Programmed Failed: \n --' + fail)
    return 0

def incrpin():
    global numberOfIntsInPin
    numberOfIntsInPin[0] = numberOfIntsInPin[0]  + 1
    numberOfIntsInPin[1] = True
    return True
    

def defineRandomCode(length):
    for i in range(0, len(correctCode)):
        correctCode.pop(0)
    for i in range(0, length):
        correctCode.append(random.randint(0, 9))
        print(correctCode)
    return correctCode

#recov(LAST_INT(INT ? INT;)_INT, TEXT_!_(LABEL?BUTTON))

def recov(lastInt, _text_):
    if len(codeHolder) != 0:
        if codeHolder[len(codeHolder) - 1] == lastInt:
            h = ''
            for i in range(0, len(codeHolder)):
                h = h + '•'
            updateText_(_text_, [True, h, [False]])
    return 0

#hasACorrectForm(!_TEXT_DISPLAY(WELL_DONE/YOU_HAVE_PLACE_X_CORRECTLY)_STRINGVAR?)

def hasACorrectForm(textOfHasFound):
    formOfCorrect = []
    for i in range(0, len(codeHolder)):
        if codeHolder[i] == correctCode[i]:
            formOfCorrect.append(codeHolder[i])
    if len(formOfCorrect) == numberOfIntsInPin[0] :
        _s =  updateText_(textOfHasFound, [True, "You have found the code ! Well done.", [False]])
                     
    else:
        _s =  updateText_(textOfHasFound, [True, "You have placed " + str(len(formOfCorrect)) + ' correctly.', [False]])

    return 0

#updateText(_!_TEXT_TO_UPDATE, [CUSTOM_TEXT_BOOL?, _!_CUSTOM_TEXT_STR, _!_[CUSTOM_COLOR_BOOL?, TEXT_TO_UPDATE_COLOR_LABEL, COLOR_STR]])
def updateText_(_text_, specialText):
    if specialText[0] == False:
        if len(codeHolder) != 0 and _hasChecked_[0] == True:
            h = ''
            for i in range(0, len(codeHolder) - 1):
                h = h + '•'
            _text_.set(h + str(codeHolder[len(codeHolder) - 1]))
            _v = codeHolder[len(codeHolder) - 1]
            window.after(1500, lambda v=0: recov(_v,_text_))
        else:
            h = ''
            for i in range(0, len(codeHolder) ):
                h = h + str(codeHolder[i])
            _text_.set(h)
    else:
        _text_.set(specialText[1])

        if specialText[2][0] == True:
            specialText
            specialText[2][1].config(fg= specialText[2][2])

        
    return True

#check(_!_KEYPAD_PRESSED_NUMBER_INT, _!_TASK[ADD/DELETE ?]_STR, _!_TEXT_DISPLAY_STRING_VAR_OBJECT, _!_[STRING_VAR_DISPLAYER_OF_SUCCESS_STRINGVAR, LABEL_TO_DISPLAY_LABEL], _!_TEXT_OF_HAS_FOUND_STRING)
def check(int_, task, _text_, codeState, textOfHasFound, levelXP):
    global codeHolder
    global keepTimerRecord
    ret = updateText_(codeState[0], [True, '•', [True, codeState[1], 'red']])
    rot =  updateText_(textOfHasFound, [True, '', [False]])
    if numberOfIntsInPin[1] == True:
        codeHolder = []
        numberOfIntsInPin[1] = False

    if task == 'add':
        if len(codeHolder) == numberOfIntsInPin[0]:
            print(codeHolder)
            for i in range(0, len(codeHolder)):
                codeHolder.pop(0)
            codeHolder.append(int_)
            updateText_(_text_, [False, '', [False]])
            if len(codeHolder) == numberOfIntsInPin[0] :
                _s = hasACorrectForm(textOfHasFound)
            if codeHolder == correctCode:
                updateText_(_text_, [False, '', [False]])
                updateText_(codeState[0], [True, '•', [True, codeState[1], 'green']]) #_1_0v colorRGB(#).explicit()[2]_2_2v
                txt_t = defineRandomCode(numberOfIntsInPin[0] + 1)
                keepTimerRecord.append(timer)
                res = incrpin()
                e_ = resetTimer()
                if e_ != True:
                    _nonFatalError("Failed to reset Timer")
                ret_ = calcXP(levelXP)
                if ret_ != True:
                    _nonFatalError('Failed to calculate XP')
        else:
            codeHolder.append(int_)
            if len(codeHolder) == numberOfIntsInPin[0] :
                _s = hasACorrectForm(textOfHasFound)
            if codeHolder == correctCode:
                updateText_(_text_, [False, '', [False]])
                updateText_(codeState[0], [True, '•', [True, codeState[1], 'green']]) #_1_0v colorRGB(#).explicit()[2]_2_2v
                txt_t = defineRandomCode(numberOfIntsInPin[0] + 1)
                keepTimerRecord.append(timer)
                res = incrpin()
                e_ = resetTimer()
                if e_ != True:
                    _nonFatalError("Failed to reset Timer")
                ret_ = calcXP(levelXP)
                if ret_ != True:
                    _nonFatalError('Failed to calculate XP')
                print(correctCode)
                
            else:
                updateText_(_text_, [False, '', [False]])
    else:
        try: #%error high - try function => error; 
            codeHolder.pop(len(codeHolder) - 1)
            if _hasChecked_[0] == True:
                h = ''
                for i in range(len(codeHolder) - 1):
                    h = h + '•'
                h = h + str(codeHolder[len(codeHolder) - 1])
                updateText_(_text_, [True, h, [False]])#? update \True.False: RGB 0/!!
            else:
                h = ''
                for i in range(0, len(codeHolder)):
                    h = h + str(codeHolder[i])
                updateText_(_text_, [True, h, [False]])#? update \True.False: RGB 0/!!
        except:
            if codeHolder == []:
                updateText_(_text_, [False, '', [False]])#? update \up/*


#reveal(_!_BUTTON_TEXT_TO_UPDATE[REVEAL/HIDE]?_STRINGVAR, _!_MAIN_TEXT_LABELVAR_STRING_VAR)
def reveal(__text__, _main_text_diplayer_):
    if _hasChecked_[0] == True:
        _hasChecked_[0] = False
        h = ''
        for i in range(0, len(codeHolder)):
            h = h + str(codeHolder[i])
        _r = updateText_(_main_text_diplayer_, [True, h, [False]])
        if not _r == True:
            print('Warning: no Comeback')
        _s = updateText_(__text__, [True, "Hide", [False]])
    else:
        _s = updateText_(__text__, [True, "Reveal", [False]])
        _hasChecked_[0] = True
        if len(codeHolder) == 0:
            return 0
        h = ''
        for i in range(0, len(codeHolder) - 1):
            h = h + '•'
        h = h + str(codeHolder[len(codeHolder) - 1])
        _r = updateText_(_main_text_diplayer_, [True, h, [False]])

#setup(?NONE)


def forceError(_):
    print('We have had an error. Here are the possibilities: \n ')
    for i in range(0, len(_)):
        try:
            print(str(i + 1) + ' - error could come from ' + _[i])
        except:
            print('We have had a sudden stop at forceError(setup([ARRAY]) position ' + str(i) + ' or explicitly ' + str(i + 1))
        


def setup():
    _temp = defineRandomCode(1)
    if not codeHolder or not window or not len(correctCode) == numberOfIntsInPin[0]  or not codeHolder:
        forceError([codeHolder, window, correctCode, codeHolder])
    h = ''
    for i in range(0, 25):
        h = h +'-'
    p = ' \n \n Loading Window... \n \n'
    print(h + p + h)
    window.title("LOADING...")
    window.geometry("320x300")
    a = window.after(3000, lambda v=0: init())


def resetTimer():
    global timer
    timer = [0, 0, 0]
    return True

def inittimer(timerLabel_, timerTxt_, frsc_, frationSecondsTimer_):
    a = window.after(1, lambda v=0: inittimer(timerLabel_, timerTxt_, frsc_, frationSecondsTimer_))
    if timer[2] == 1000:
        timer[2] = 0
        if timer[1] == 59:
            timer[1] = 0
            timer[0] = timer[0] + 1
        else:
            timer[1] = timer[1] + 1
    else:
        timer[2] = timer[2] + 1
    global disp_
    global disp__
    global disp___
    if timer[0] < 10:
        disp_ = '0' + str(timer[0])
    else:
        disp_ = str(timer[0])
#---
    if timer[1] < 10:
        disp__ = '0' + str(timer[1])
    else:
        disp__ = str(timer[1])
#----
    if timer[2] < 10:
        disp___ = '0' + str(timer[2])
    else:
        disp___ = str(timer[2]) 
        disp___ = disp___[0] + disp___[1]
    
    timerTxt_.set(disp_ + ':' + disp__)
    frsc_.set("." +disp___)


def init() :
    window.title("Locker")
    window.geometry("340x400")
    check_devider = [1, 1]
    text__ = StringVar()
    L = Label(window, textvariable = text__, width=0, font=('Helvetica bold', 20))
    L.place(x=150,y= 60)
    slidingText = StringVar()
    slidingText.set("Reveal")
    c=Button(window, textvariable=slidingText,width=4, command = lambda v=0 : reveal(slidingText, text__))
    c.place(x=60,y= 70)
    codeState = StringVar()
    k = Label(window, textvariable = codeState, width=0, font=('Helvetica bold', 15))
    k.place(x = 270, y = 20)
    codeState.set('•')
    textOfHasFound = StringVar()
    k.config(fg = "red")
    n=Button(window, text="Delete",width=4, command = lambda v=0 : check(v, 'remove', text__, [codeState, k], textOfHasFound, [levelLabel, levelText]))
    n.place(x=250,y= 70)
    t = Label(window, textvariable = textOfHasFound, width=0, font=('Helvetica bold', 10))
    print(correctCode)
    t.place(x = 80, y = 270)
    frsc = StringVar()
    frsc.set(".00")
    frationSecondsTimer = Label(window, textvariable = frsc, width=0, font=('Helvetica bold', 7))
    frationSecondsTimer.place(x = 35, y = 2)
    levelText = StringVar()
    levelText.set("Level: " + str(numberOfIntsInPin[0]) + "\n Exp: " + str(xp[0]))
    levelLabel = Label(window, textvariable = levelText, width=0, font=('Helvetica bold', 8))
    levelLabel.place(x = 5, y = 20)
    timerTxt = StringVar()
    timerTxt.set("00:00")
    timerLabel = Label(window, textvariable = timerTxt, width=0, font=('Helvetica bold', 8))
    timerLabel.place(x = 5, y = 0)

    for i in range(0, 10):
        if i % 3 == 0:
            check_devider[0] = 1
            check_devider[1] =  check_devider[1] + 1
        check_devider[0] =  check_devider[0] + 1
        if i + 1 < 10:
            valider_=Button(window, text=(i + 1),width=5, command = lambda v=i + 1 : check(v, 'add', text__, [codeState, k], textOfHasFound, [levelLabel, levelText]))            
            valider_.place(x= check_devider[0] * 50, y= 40 + (35 * check_devider[1]))
        else:
            valider_=Button(window, text=0,width=5, command = lambda v=0 : check(v, 'add', text__, [codeState, k], textOfHasFound, [levelLabel, levelText]))            
            valider_.place(x= (check_devider[0] + 1) * 50, y= 40 + (35 * check_devider[1]))
    _x = inittimer(timerLabel, timerTxt, frsc, frationSecondsTimer)
    h = ''
    for i in range(0, 25):
        h = h +'-'
    p = ' \n \n Window was loaded succesfully. #2222 \n \n'
    print(h + p + h)
setup()


window.mainloop()

#Codé de A à Z par Marco ASKOVIC.
from tkinter import *
import threading as freading



#VERSION 1 (SIMPLE)


codeHolder, correctCode, _hasChecked_, numberOfIntsInPin, window = [], [2,8,3,5] , [True], 4, Tk()

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
    if len(formOfCorrect) == numberOfIntsInPin:
        _s =  updateText_(textOfHasFound, [True, "You have found the code ! Well done.", [False]])
                     
    else:
        _s =  updateText_(textOfHasFound, [True, "You have placed " + str(len(formOfCorrect)) + ' correctly.', [False]])

    return

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
def check(int_, task, _text_, codeState, textOfHasFound):
    ret = updateText_(codeState[0], [True, '•', [True, codeState[1], 'red']])
    rot =  updateText_(textOfHasFound, [True, '', [False]])
    if task == 'add':
        if len(codeHolder) == 4:
            print(codeHolder)
            for i in range(0, len(codeHolder)):
                codeHolder.pop(0)
            codeHolder.append(int_)
            updateText_(_text_, [False, '', [False]])
        else:
            codeHolder.append(int_)
            if len(codeHolder) == 4:
                _s = hasACorrectForm(textOfHasFound)
            if codeHolder == correctCode:
                updateText_(_text_, [False, '', [False]])
                updateText_(codeState[0], [True, '•', [True, codeState[1], 'green']]) #_1_0v colorRGB(#).explicit()[2]_2_2v
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
    if not codeHolder or not window or not len(correctCode) == numberOfIntsInPin or not codeHolder:
        forceError([codeHolder, window, correctCode, codeHolder])
    h = ''
    for i in range(0, 25):
        h = h +'-'
    p = ' \n \n Loading Window... \n \n'
    print(h + p + h)
    window.title("LOADING...")
    window.geometry("320x300")
    a = window.after(3000, lambda v=0: init())


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
    n=Button(window, text="Delete",width=4, command = lambda v=0 : check(v, 'remove', text__, [codeState, k], textOfHasFound))
    n.place(x=250,y= 70)
    t = Label(window, textvariable = textOfHasFound, width=0, font=('Helvetica bold', 10))
    t.place(x = 80, y = 270)
    for i in range(0, 10):
        if i % 3 == 0:
            check_devider[0] = 1
            check_devider[1] =  check_devider[1] + 1
        check_devider[0] =  check_devider[0] + 1
        if i + 1 < 10:
            valider_=Button(window, text=(i + 1),width=5, command = lambda v=i + 1 : check(v, 'add', text__, [codeState, k], textOfHasFound))            
            valider_.place(x= check_devider[0] * 50, y= 40 + (35 * check_devider[1]))
        else:
            valider_=Button(window, text=0,width=5, command = lambda v=0 : check(v, 'add', text__, [codeState, k], textOfHasFound))            
            valider_.place(x= (check_devider[0] + 1) * 50, y= 40 + (35 * check_devider[1]))
    h = ''
    for i in range(0, 25):
        h = h +'-'
    p = ' \n \n Window was loaded succesfully. #2222 \n \n'
    print(h + p + h)

setup()


window.mainloop()

#Codé de A à Z par Marco ASKOVIC.

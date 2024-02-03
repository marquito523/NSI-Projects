from tkinter import *
import random as random
from pymongo import MongoClient
import smtplib
import ssl
from email.message import EmailMessage

#!                      IMPORTANT!



#Afin de faire fonctionner se programme, il vous faut:
# - Python 3.6 ou plus
# - Tous les packages importé à jour
# - Une connexion stable à internet (j'insiste sur la stabilité de la connexion) => {
#   - Connexion du lycée ne marchera pas (beaucoup de latence) => NON FONCTIONNEL
#   - Partage de connexion: Ca marchera mais surement avec une légère latence. Mais ca devrait être bon  => FONCTIONNEL
#   - Connexion Internet moyenne: (Ping de moins de 60ms; Reception à 25mb /s ; Envoie à 25mb/s) devrait marcher => FONCTIONNEL
#   - Connexion Internet Puissante: (Ping de moins de 20ms; Reception à 35mb/s ; Envoie à 38mb/s) vous proposera une latence minimale: Optimal
# }



#Le programme peut mettre quelques secondes (pas plus de 3 avec une connexion internet passable) comme celui-ci importe une data stockée
#sur le cloud afin que votre progression sur le jeu ne soit pas perdu et puisse être retrouvée depuis n'importe quel poste.

#Attention, ce programme n'est pas encore tout à fait stable, en d'autres termes, il est fort probable que si vous jouez avec ses limites
#celui-ci cesse de fonction comme les gardes fou à ma data store sont très insuffisant. (Evitez les noms avec des caracteres qui peuvent)
#confondre l'interpreteur ex: " / , / ; / + / = / $. 

#Pour recuperer votre mot de passe, vous recevrez un mail, hors celui-ci apparaitra surement dans vos spams. 

#IMPORTANT**: Ne pas mettre une fausse adresse mail qui ne marcherais pas: Le programme ne possed aucun garde de fou pour ce type de test.


#Quelques details importants:

#Je tiens à informer à tout utilisateur de ce programme que j'ai accès aux données personnelles de chaque compte créé, ce faisant,
#veuillez éviter d'utiliser des mots de passes que vous avez l'habitude d'utiliser ou autre, même si je ne compte pas les divulger
#ou encore moins me connecter à vos compte, je pense que par principe vous ne voulez pas que je connaisse ses données, même si, 
#les peu de fois que je me rends sur la DataStore, c'est pour supprimer des comptes créé qui ne sont pas utilisé...



#Aucun code n'a été copié collé dans ce programme, et l'algorythme ainsi que la syntaxe me sont propre.

#Reference Variables as Undefined Globally
email_sender = 'noresponsepad@gmail.com'
email_password = 'tdbmxpgnmprgsmmv'
email_receiver = 'marcoaskovic@hotmail.com'

global Clust
global databaseConnexion
global collection
global codeHolder
global correctCode
global _hasChecked_
global numberOfIntsInPin
global xp
global window
global timer
global keepTimerRecord
global databasePreseance
global User
global Id_
global logStatus
global loginButton
global keepCodeResetPassword
global SETTINGS_OPEN
global LoopingBeforeDsiconnection
global sensor

#Reference Global Variables as Defined Gobally

def defaultVariableValues():
    global sensor
    global codeHolder
    global correctCode
    global _hasChecked_
    global numberOfIntsInPin
    global xp
    global window
    global timer
    global keepTimerRecord
    global databasePreseance
    global User
    global Id_
    global logStatus
    global loginButton
    global keepCodeResetPassword
    global SETTINGS_OPEN
    global LoopingBeforeDsiconnection
    window = Tk()
    codeHolder = []
    correctCode = []
    _hasChecked_ = [True]
    numberOfIntsInPin = [1, False]
    xp = [0, 500]
    timer = [0, 0, 0]
    keepTimerRecord = []
    logStatus = 0
    keepCodeResetPassword = []
    SETTINGS_OPEN = [False]
    LoopingBeforeDsiconnection = [False, 0]
    sensor = False
    return


#Data {user: hsdefpad ; password: NZWbmHLwnFtlVN7Y} 


def calcXP(levelXP_):
    xp[0] = xp[0] + ((xp[1] * (numberOfIntsInPin[0] - 1)) // (keepTimerRecord[len(keepTimerRecord) - 1][0] + 1)) - keepTimerRecord[len(keepTimerRecord) - 1][1]
    levelXP_[1].set("Level: " + str(numberOfIntsInPin[0]) + "\n Exp: " + str(xp[0]) + 'xp') 
    idUpdater = {"_id": Id_}
    newValues = {"$set": {"xp": xp[0]}}
    collection.update_one(idUpdater, newValues)
    return True

def _nonFatalError(fail):
    print('Programmed Failed: \n --' + fail)
    return 0

def incrpin():
    global numberOfIntsInPin
    numberOfIntsInPin[0] = numberOfIntsInPin[0]  + 1
    numberOfIntsInPin[1] = True
    idUpdater = {"_id": Id_}
    newValues = {"$set": {"level": numberOfIntsInPin[0]}}
    collection.update_one(idUpdater, newValues)
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
    for i in range(0, len(_)):
        try:
            return
        except:
            return  



def filter(content):
    for i in range(0, len(content.get())):
        if content.get()[i] == '&' or  content.get()[i] == '$' or  content.get()[i] == ';' or  content.get()[i] == "'" or  content.get()[i] == '+' or  content.get()[i] == '-' or  content.get()[i] == '²' or  content.get()[i] == ',' or  content.get()[i] == '?' or  content.get()[i] == '!' or  content.get()[i] == '(' or  content.get()[i] == '{' or  content.get()[i] == '#':
            return False
    if len(content.get()) > 50:
       return False
    return True


def logAccount(username, password, emailContent, cred, btn, lbl, credholdermail, todelete):
    global userExists 
    global logStatus
    global databasePreseance
    global Id_
    Id_ = False
    userExists = False
    global dressUserData
    global User
    User = 0
    result = filter(username)
    if result == False:
        setupAfterFail(1)
        return
    result = filter(emailContent[1])
    if result == False:
        setupAfterFail(1)
        return
    dressUserData = {
        "username": username.get(),
        "password": password.get(),
        "level": 1,
        "xp": 0,
        "email": emailContent[1].get(),
        "other": []
        }

    if logStatus == 0:
        fetchData = collection.find({"username":username.get()})
        for result in fetchData:
            if result["password"] == dressUserData['password']:
                userExists = True
                User = result
                Id_ = result["_id"]
                databasePreseance = True
        if User == 0: 
            databasePreseance = False
            setupAfterFail(0)
            return
        else:
            xp[0] = User["xp"]
            numberOfIntsInPin[0] = User["level"]
    else:
        fetchData = collection.find({"username":username.get()})
        for result in fetchData:
            if result["username"] == dressUserData['username']:
                userExists = True
                setupAfterFail(0)
                return
        fetchDataMail = collection.find({"email":emailContent[1].get()})
        for result in fetchDataMail:
            if result["email"] == dressUserData['email']:
                userExists = True
                setupAfterFail(0)
                return

        global checkIfHas_
        checkIfHas_ = False
        for i in range(0, len(emailContent[1].get())):
            if emailContent[1].get()[i] == '@':
                checkIfHas_ = True
        if checkIfHas_ == False:
            setupAfterFail(2)
            return
        
        if userExists == False:
            databasePreseance = True
            fetch2 = collection.find({"fly": False})
            for f in fetch2:
                Id_ = f["typeCount"] + 1
            idUpdater = {"typeCount": Id_ - 1}
            newValues = {"$set": {"typeCount": Id_}}
            collection.update_one(idUpdater, newValues)
            dressUserData_ = {
            "_id": Id_,
            "username": username.get(),
            "password": password.get(),
            "level": 1,
            "xp": 0,
            "email": emailContent[1].get(),
            "other": []
            }

            mail_ = formMail(emailContent[1], """You have created an account. \n \n Welcome to Pads ! \n \n Pads is a class work made by Marco ASKOVIC. This project has praticly every system a nowdays game should have. Even if the game-objective game is very poor, the point is to test out the online system and automatic mailing system. Your mail will not be kept nor will it be abused. Any account data will be deleted 45 days after creation and will not be kept anywhere. \n \n \n Additionnal information \n \n \n Your data is stored on Mongoose 2.6.0. Data can been seen by creator and creator only.""", 1, 1)
            if mail_ == False:
                setupAfterFail(2)
                return 
            collection.insert_one(dressUserData_)
    _temp = defineRandomCode(numberOfIntsInPin[0])
    print(Id_)
    cred.destroy()
    btn.destroy()
    lbl.destroy()
    global loginButton
    loginButton.destroy()
    credholdermail.destroy()
    todelete.destroy()
    init()

def switch(txt, txt_, crd):
    global logStatus
    if logStatus == 0:
        txt.set("Sign up")
        txt_.set("Log in")
        logStatus = 1
        crd.place(x = -30, y = -30)
    else:
        txt.set("Log in")
        txt_.set("Sign up")
        logStatus = 0
        crd.place(x = -54454, y = -34430)

    
def setup():
    global window
    window.destroy()
    window = Tk()

    cred = Canvas(window, width=400, height=300)
    credHolderMail = Canvas(window, width=400, height=300)
    cred.place(x = -30, y = -30)

    credHolderMail.place(x = -333330, y = -32440)
    buttonlogtext, buttonswitchtext = StringVar(), StringVar()
    UsernameText = StringVar()
    PasswordText = StringVar()
    emailText = StringVar()
    emailText.set("Email")

    UsernameText.set("Username")
    usernameHolder = Entry(window, textvariable=UsernameText) 
    PasswordText.set("Password")
    passwordHolder = Entry(window, textvariable=PasswordText) 
    emailHolder = Entry(window, textvariable=emailText)

    cred.create_window(200, 140, window=usernameHolder)
    cred.create_window(200, 170, window=passwordHolder)

    credHolderMail.create_window(200, 110, window=emailHolder)
    errorMsgHolder = StringVar()

    _temp = defineRandomCode(1)
    if not codeHolder or not window or not len(correctCode) == numberOfIntsInPin[0]  or not codeHolder:
        forceError([codeHolder, window, correctCode, codeHolder])
    h = ''
    for i in range(0, 25):
        h = h +'-'
    p = ' \n \n Loading Window... \n \n'
    window.title("Log In")
    window.geometry("320x300")
    buttonswitchtext.set("Signup")
    buttonlogtext.set("Login")
    global loginButton
    loginButton = Button(window, textvariable=buttonlogtext,width=6, command = lambda v=0 : logAccount(UsernameText, PasswordText,[emailHolder, emailText], cred, c, t, credHolderMail, e))
    c=Button(window, textvariable=buttonswitchtext,width=6, command = lambda v=0 : switch(buttonlogtext, buttonswitchtext, credHolderMail))
    t = Label(window, textvariable=errorMsgHolder, fg = "red")
    e=Button(window, text="Fergot Password",width=6, command = lambda v=0 : hasFergotPassword(False))
    loginButton.place(x = 145, y = 165)
    c.place(x = 145, y = 200)
    t.place(x = 50, y = 150)
    e.place(x = 145, y = 245)



def setupAfterFail(v):
    global window
    window.destroy()
    window = Tk()
    cred = Canvas(window, width=400, height=300)
    credHolderMail = Canvas(window, width=400, height=300)
    cred.place(x = -30, y = -30)

    credHolderMail.place(x = -30, y = -30)
    buttonlogtext, buttonswitchtext = StringVar(), StringVar()
    UsernameText = StringVar()
    PasswordText = StringVar()

    emailText = StringVar()
    emailText.set("Email")
    UsernameText.set("Username")

    usernameHolder = Entry(window, textvariable=UsernameText) 
    PasswordText.set("Password")

    passwordHolder = Entry(window, textvariable=PasswordText) 
    emailHolder = Entry(window, textvariable=emailText)
    cred.create_window(200, 140, window=usernameHolder)

    cred.create_window(200, 170, window=passwordHolder)
    credHolderMail.create_window(200, 110, window=emailHolder)
    errorMsgHolder = StringVar()

    _temp = defineRandomCode(1)
    if not codeHolder or not window or not len(correctCode) == numberOfIntsInPin[0]  or not codeHolder:
        forceError([codeHolder, window, correctCode, codeHolder])
    h = ''
    for i in range(0, 25):
        h = h +'-'
    p = ' \n \n Loading Window... \n \n'
    window.title("Log In")
    window.geometry("320x300")
    if logStatus == 0:
        buttonswitchtext.set("Signup")
        buttonlogtext.set("Login")
        credHolderMail.place(x = -357440, y = -34340)

    else:
        buttonswitchtext.set("Login")
        buttonlogtext.set("Signup")
        credHolderMail.place(x = -30, y = -30)

    global loginButton

    loginButton = Button(window, textvariable=buttonlogtext,width=6, command = lambda v=0 : logAccount(UsernameText, PasswordText, [emailHolder, emailText], cred, c, t, credHolderMail, e))
    c=Button(window, textvariable=buttonswitchtext,width=6, command = lambda v=0 : switch(buttonlogtext, buttonswitchtext, credHolderMail))
    e=Button(window, text="Fergot Password",width=6, command = lambda v=0 : hasFergotPassword(False))
    t = Label(window, textvariable=errorMsgHolder, fg = "red")

    if logStatus == 0 and v == 0:
        errorMsgHolder.set("No matching accounts found !")
    elif logStatus == 1 and v == 0:
        errorMsgHolder.set("Username already in use !")
    elif v == 1:
        errorMsgHolder.set("Invalid Symbols or too long input.")
    else:
        errorMsgHolder.set("Provided Email is incorrect or not supported.")
    loginButton.place(x = 145, y = 175)
    c.place(x = 145, y = 210)
    t.place(x = 75, y = 20)
    e.place(x = 145, y = 245)

#------------------------------------ SETTING ?? SETTINGS FUNCTIONS - BUTTONS START------------------------------------ 

def launchInit():
    SETTINGS_OPEN[0] = not SETTINGS_OPEN[0]
    init()

def settingsPage(joining):
    global window
    window.destroy() 
    window = Tk()
    window.geometry("500x300")
    window.title("Settings")
    buttons = ["Change username", "Change password", "Change email", "Delete account"]
    if joining == True:
        SETTINGS_OPEN[0] = not SETTINGS_OPEN[0]
    for i in range(0, len(buttons)):
        createButton = Button(window, width=15, text = buttons[i], command = lambda v = i: hasClickedSettingButton([v, False]))
        createButton.place(x = 60 + (i %3)*150, y = 30 + (i // 3) * 40)
    closeSettings = Button(window, width=4, text="return", command = launchInit)
    closeSettings.place(x = 10, y = 30)



#hasClickedSetting(request: => requestType: int)

def hasClickedSettingButton(request):
    global sensor
    global window
    window.destroy()
    window = Tk()
    window.geometry("500x300")
    if request[0] == 0:
        window.title("Change Username")
        credHolderMail = Canvas(window, width=400, height=300)
        credHolderMail.place(x = 30, y = 30)
        emailText = StringVar()

        emailText.set("Username")
        emailHolder = Entry(window, textvariable=emailText)
        credHolderMail.create_window(200, 110, window=emailHolder)

        Valid = Button(window, width=4, text="Submit", command = lambda v = 0: updateFromData("username", emailText.get(), [True, "username", emailText.get()], 0))
        Return = Button(window, width=4, text="Back", command = lambda v = 0: settingsPage(False))
        Return.place(x = 10, y = 30)
        Valid.place(x = 210, y = 170)

        textVar = StringVar()
        textError = Label(window, textvariable=textVar)
        textError.place(x = 150, y = 20)

        if request[1] == True:
            textVar.set('Request result into an error.')
        elif request[1] == 2:
            textVar.set('Changes have been succesfully made.')
    elif request[0] == 1:
        window.title("Change password")
        credHolderMail = Canvas(window, width=400, height=300)
        credHolderMail.place(x = 30, y = 30)
        emailText = StringVar()

        emailText.set("Password")
        emailHolder = Entry(window, textvariable=emailText)
        credHolderMail.create_window(200, 110, window=emailHolder)

        Valid = Button(window, width=4, text="Submit", command = lambda v = 0: updateFromData("password", emailText.get(), [False], 1))
        Return = Button(window, width=4, text="Back", command = lambda v = 0: settingsPage(False))

        Return.place(x = 10, y = 30)
        Valid.place(x = 210, y = 170)
        textVar = StringVar()

        textError = Label(window, textvariable=textVar)
        textError.place(x = 150, y = 20)

        if request[1] == True:
            textVar.set('Request result into an error.')
        elif request[1] == 2:
            textVar.set('Changes have been succesfully made.')
    elif request[0] == 2:
            window.title("Change Email")
            credHolderMail = Canvas(window, width=400, height=300)
            credHolderMail.place(x = 30, y = 30)
            emailText = StringVar()
            emailText.set("Email")

            emailHolder = Entry(window, textvariable=emailText)
            credHolderMail.create_window(200, 110, window=emailHolder)

            Valid = Button(window, width=4, text="Submit", command = lambda v = 0: updateFromData("email", emailText.get(), [True, "email", emailText.get()], 0))
            Return = Button(window, width=4, text="Back", command = lambda v = 0: settingsPage(False))

            Return.place(x = 10, y = 30)
            Valid.place(x = 210, y = 170)

            textVar = StringVar()
            textError = Label(window, textvariable=textVar)
            textError.place(x = 150, y = 20)
            if request[1] == True:
                textVar.set('Request result into an error.')
            elif request[1] == 2:
                textVar.set('Changes have been succesfully made.')
    elif request[0] == 3:
            window.title("Delete Account")
            credHolderMail = Canvas(window, width=400, height=300)
            credHolderMail.place(x = 30, y = 30)

            emailText = StringVar()
            emailText.set("Password")
            emailHolder = Entry(window, textvariable=emailText)
            credHolderMail.create_window(200, 110, window=emailHolder)

            Valid = Button(window, width=4, text="Submit", command = lambda v = 0: proceedAccountDeletion(emailText))
            Return = Button(window, width=4, text="Back", command = lambda v = 0: settingsPage(False))
            Return.place(x = 10, y = 30)
            Valid.place(x = 210, y = 170)
            textVar = StringVar()

            textError = Label(window, textvariable=textVar)
            textError.place(x = 150, y = 20)

            if request[1] == 3:
                print(" onono")
                textVar.set('Database could not be fetched.')
            elif request[1] == 2:
                print("here")
                updatetxt("Account deletion. Disconnecting", textVar, 0, 0)
                return





def updatetxt(txt, txtVar, e, t):
    global window
    print(txt)
    if e == 20:
        window.destroy()
        STARTUP()
        return 
    else:
        e = e + 1
    if t == 3:
        t = 0
    else:
        t = t + 1
    txtVar.set(txt)
    h = '.' * t
    a = window.after(100, lambda v=0: updatetxt("Account deletion. Disconnecting" + str(h), txtVar, e, t)) #Repeats this function every fraction of second



def proceedAccountDeletion(password):
    global User

    if not User:
        r = collection.find({"_id":Id_})
        global t
        t = 0
        for result in r:
            t = result
        if t == 0:
            print("error")
            return
        else:
            User = t
    fetchData = collection.find({"_id":Id_})
    for result in fetchData:
        if result["password"] == User['password']:
            try:
                collection.delete_one({'_id': Id_})
                hasClickedSettingButton([3, 2])
            except:
                hasClickedSettingButton([3, 3])
                print("Error !")


    


def updateFromData(_categoryToUpdate, ValueToApply, additionalContent, comesFrom):
    global User
    if not User:
        r = collection.find({"_id":Id_})
        global t
        t = 0
        for result in r:
            t = result
        if t == 0:
            print("error")
            return
        else:
            User = t

    if additionalContent[0] == False:
            try:
                idUpdater = {"_id": Id_}
                newValues = {"$set": {_categoryToUpdate: ValueToApply}}
                collection.update_one(idUpdater, newValues)
                hasClickedSettingButton([comesFrom, 2])
            except:
                print("Unexpected Error")
                hasClickedSettingButton([comesFrom, 1])

    else:
        fetchData = collection.find({additionalContent[1]:additionalContent[2]})
        for result in fetchData:
            hasClickedSettingButton([comesFrom, True])
            return 
        try:
            idUpdater = {"_id": Id_}
            newValues = {"$set": {_categoryToUpdate: ValueToApply}}
            collection.update_one(idUpdater, newValues)
            hasClickedSettingButton([comesFrom, 2])
        except:
            print("Unexpected Error")

        
            




#------------------------------------ SETTING ?? SETTINGS FUNCTIONS - BUTTONS END ------------------------------------ 
    
   # a = window.after(3000, lambda v=0: init())

def sendMail(emailHolder):
    global tmpuser
    global found
    found = False
    f = False
    for i in range(0, len(emailHolder.get())):
        if emailHolder.get()[i] == '@':
            f = True
    if f == False:
        hasFergotPassword(True)
        return
    fetchData = collection.find({"email":emailHolder.get()})
    for result in fetchData:
        tmpuser = result
        found = True
    if found == False:
        hasFergotPassword(True)
        return
    else:
        text = """The password of your account """ + tmpuser['username'] + """ is < """ + tmpuser["password"] + """ >."""
        formMail(tmpuser, text, 0, 0)


def formMail(tmpuser, text, __, t):

    if t == 0:
            try:
                h = ''
                for i in range(0, len(keepCodeResetPassword)):
                    h = h + str(keepCodeResetPassword[i])
                subject = 'noResponse'
                body = text
                em = EmailMessage()
                em['From'] = email_sender
                em['To'] = tmpuser['email']
                em['Subject'] = subject
                em.set_content(body)

                # Add SSL (layer of security)
                context = ssl.create_default_context()

                # Log in and send the email
                with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                    smtp.login(email_sender, email_password)
                    smtp.sendmail(email_sender, tmpuser['email'], em.as_string())
                return True
            except:
                if __ == 0:
                    hasFergotPassword(True) 
                elif __ == 1:
                    return False
    elif t == 1:
        try:
            h = ''
            for i in range(0, len(keepCodeResetPassword)):
                h = h + str(keepCodeResetPassword[i])
            subject = 'noResponse'
            body = text
            em = EmailMessage()
            em['From'] = email_sender
            em['To'] = tmpuser.get()
            em['Subject'] = subject
            em.set_content(body)

            # Add SSL (layer of security)
            context = ssl.create_default_context()

            # Log in and send the email
            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                smtp.login(email_sender, email_password)
                smtp.sendmail(email_sender, tmpuser.get(), em.as_string())
            return True
        except:
                if __ == 0:
                    hasFergotPassword(True) 
                elif __ == 1:
                    return False
        


def hasFergotPassword(_):
    global window
    window.destroy()
    window = Tk()
    window.geometry("320x300")

    cred = Canvas(window, width=400, height=300)
    cred.place(x = -30, y = -30)
    emailHolder = StringVar()
    emailHolder.set("Username")
    emailEntry = Entry(window, textvariable=emailHolder) 
    cred.create_window(200, 140, window=emailEntry)

    c=Button(window, text="Send",width=6, command = lambda v=0 : sendMail(emailHolder))
    l=Button(window, text="Return",width=6, command = lambda v=0 : setup())
    t = Label(window, text="Please check your spams.")

    if _ == True:
        f = Label(window, text="Could not find a corresponding account !", fg = 'red')
        f.place(x = 60, y = 20)
    c.place(x = 145, y = 180)
    t.place(x = 100, y = 50)
    l.place(x = 145, y = 220)


    emailHolder.set("Email")
def resetTimer():
    global timer
    timer = [0, 0, 0]
    return True

def inittimer(timerLabel_, timerTxt_, frsc_, frationSecondsTimer_):

    a = window.after(1, lambda v=0: inittimer(timerLabel_, timerTxt_, frsc_, frationSecondsTimer_)) #Repeats this function every fraction of second

    if SETTINGS_OPEN[0] == False:
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
            disp___ = str(timer[2]) #Transformation of DISP___ from XXX to 'XXX'

            disp___ = disp___[0] + disp___[1] #Uses the array advantages to remove a digit without any mathematical equation: 'XXX'.susbrting(2) becomes XX
        
        timerTxt_.set(disp_ + ':' + disp__)
        frsc_.set("." +disp___)


def STARTUP():

    a = defaultVariableValues()

    global window
    global Clust
    global databaseConnexion
    global collection

    window.destroy()
    window = Tk()
    window.geometry("320x300")

    L = Label(window, text = "Connecting to dataStore...", width=0, font=('Helvetica bold', 30))
    L.place(x=150,y= 60)

    Clust = MongoClient("mongodb+srv://hsdefpad:NZWbmHLwnFtlVN7Y@cluster0.gy0id0g.mongodb.net/?retryWrites=true&w=majority") #Connexion à la DataStore (raison d'un léger chargement en début de lancement.)
    databaseConnexion = Clust["PADUSERS"]
    collection = databaseConnexion["PADUSERS"]
    setup()



def init() :

    global window
    window.destroy()
    window = Tk()
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

    Settings=Button(window, text="Settings",width=5, command = lambda v=0: settingsPage(True))      
    Settings.place(x = 15, y = 370)      

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
STARTUP()


window.mainloop()

#Codé de A à Z par Marco ASKOVIC.







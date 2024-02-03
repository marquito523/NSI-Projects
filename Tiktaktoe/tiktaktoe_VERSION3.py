
#Afin de faire fonctionner se programme, il vous faut:
# - Python 3.6 ou plus
# - Tous les packages importé à jour
# - Une connexion stable à internet (j'insiste sur la stabilité de la connexion) => {
#   - Connexion du lycée ne marchera pas (beaucoup de latence) => NON FONCTIONNEL
#   - Partage de connexion: Ca marchera mais surement avec une légère latence. Mais ca devrait être bon  => FONCTIONNEL
#   - Connexion Internet moyenne: (Ping de moins de 60ms; Reception à 25mb /s ; Envoie à 25mb/s) devrait marcher => FONCTIONNEL
#   - Connexion Internet Puissante: (Ping de moins de 20ms; Reception à 35mb/s ; Envoie à 38mb/s) vous proposera une latence minimale: Optimal
# }





#MISE EN ROUTE

#Bonjour madame. Je me permet de vous laisser cette note afin de vous expliquer comment utiliser ce programme afin de pouvoir 
#justifier la présence de plusieurs centaine de ligne.
#Si vous avez deux ordinateurs à votre disposition, allez voir "DEUX ORDINATEURS" un peu plus bas.
#Si vous n'en avez qu'un seul, allez voir "UN-SEUL-ORDINATEUR"


#DEUX ORDINATEURS

#Si vous avez deux ordinateurs à votre disposition, ouvrez dans chacun des ordinateurs un interpreteur avec ce programme dedans.
#Assurez vous que dans chacun des ordinateur vous avez Pymongo. Si ce n'est pas le cas, allez voir un peu plus bas "PYMONGO-INSTALLATION"



#PYMONGO-INSTALLATION

#Assurez vous d'avoir la bibliothèque pymongo (si ce n'est pas le cas: dans la console: pour visual studio (code): "pip install pymongo")
#                                                                                       pour EduPython: Outil / Installer un package avec PIP / écrire "pymongo" / installer / attendre



#UN-SEUL-ORDINATEUR


#Tout d'abord, vous allez avoir besoin de deux pages differentes d'interpreteurs, les deux ayant ce programme:
#ex: Ouvrez deux fois EduPython et mettez ce programme dans les deux. Pareil pour Visual Studio Code / Visual Studio / etc...
#Assurez vous d'avoir pymongo sur votre python. Si ce n'est pas le cas, allé voir "PYMONGO-INSTALLATION"
#Lancez le programme sur les deux page ce qui ouvrera les deux fenetres. Avec une des deux, créez une partie. Avec l'autre, rejoingnez la partie que
#vous venez de créer. 












#Le programme est entièrement fait par ma personne. Aucun bout de code n'à été prit d'internet (je précise, étant quand même fier de ce fait)
#C'est d'ailleurs mon premier jeu 'en ligne' (le serveur que j'utilise n'est oas veritabelement un serveur mais une dataStore parce que j'ai pas les moyens d'en louer...)




from pymongo import MongoClient
from tkinter import *
from random import * 
Clust = MongoClient("mongodb+srv://hsdefpad:NZWbmHLwnFtlVN7Y@cluster0.gy0id0g.mongodb.net/?retryWrites=true&w=majority")
databaseConnexion = Clust["TIKTAKTOEGAMES"]
collection = databaseConnexion["TIKTAKTOEGAMES"]
global window
global findGames
global SoloGame
global CreateGame
global AnimEnded
global OwnsGame
global Turn
AnimEnded = False
window = Tk()
OwnsGame = 2
global storeObjects
storeObjects = {'buttons': [], 'windows': []}
global serverCreationDict
global preventIsActive 
global inGameUsingInteractionServer
global refreshRate
refreshRate = 0
preventIsActive = False
global keepIdOfJoin
keepIdOfJoin = 0
serverCreationDict = {
    "name": "", 
    "RequestsPassword": [False],
}


global holdGameIDOwner
holdGameIDOwner = ""


def initGame(library, server):
    window.geometry("350x350")
    moncanevas = Canvas(window, width=300, height=300, bg="white")
    moncanevas.place(x=50,y=60)
    global keepTrackBoxes
    keepTrackBoxes = server["KeepTrackBoxes"]
    global possibleLines
    possibleLines = server["PossibleLines"]
    global winner
    winner = 5



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
        global winner
        if len(keepTrackBoxes) < 5:
            return False
        for i in range(0, len(possibleLines)):
            if len(possibleLines[i][0]) == 3 and len(possibleLines[i][1]) == 3 and len(possibleLines[i][2]) == 3:
                if possibleLines[i][0][2] == possibleLines[i][1][2] == possibleLines[i][2][2]:
                    winner = possibleLines[i][0][2]
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
        if OwnsGame != Turn:
            return
        if winner != 5:
            return
        global keepTrackBoxes
        box = getBox(evenement)

        for i in range(0, len(keepTrackBoxes)):
            if keepTrackBoxes[i][0][0] == box[0] and keepTrackBoxes[i][0][1] == box[1]:
                return print("box has been used")
        x, y = evenement.x, evenement.y
        keepTrackBoxes.append([[box[0], box[1]], Turn])
        idUpdater = {"gameID": server["gameID"]}
        newValues = {"$set": {"KeepTrackBoxes": keepTrackBoxes}}
        collection.update_one(idUpdater, newValues)

        for i in range(0, len(possibleLines)):
            for v in range(0, len(possibleLines[i])):
                if possibleLines[i][v][0] == box[0] and possibleLines[i][v][1] == box[1]:
                    possibleLines[i][v].append(Turn)
                    idUpdater = {"gameID": server["gameID"]}
                    newValues = {"$set": {"PossibleLines": possibleLines}}
                    collection.update_one(idUpdater, newValues)
        if Turn == 0:
            idUpdater = {"gameID": server["gameID"]}
            newValues = {"$set": {"Turn": 1}}
            collection.update_one(idUpdater, newValues)
            callback = createCross(box)
        else:
            callback = createCircle(box)
            idUpdater = {"gameID": server["gameID"]}
            newValues = {"$set": {"Turn": 0}}
            collection.update_one(idUpdater, newValues)
        checkLines()

    moncanevas.bind("<Button-1>", Dipsatcher)



    def destroyCan(function, Has):
        moncanevas.destroy()
        if Has[0] == True:
            function(Has[1])
        return


    def objectDestroy(obj):
        obj.destroy()
        createWindow()

    def callOutWinner():
        global winner
        global lab
        if winner == OwnsGame:
            lab = Label(window, text='You won !', width = 10)
            lab.place(x = 10, y = 10)
            a = window.after(2000, lambda v=0: destroyCan(objectDestroy, [True, lab]))
        else:
            lab = Label(window, text='You lost !', width = 10)
            lab.place(x = 10, y = 10)
            a = window.after(2000, lambda v=0: destroyCan(objectDestroy, [True, lab]))



        
    def updatePanel(t):
        global inGameUsingInteractionServer
        global keepTrackBoxes
        global possibleLines
        global Turn
        global winner
        if winner != 5:
            t = False
            return callOutWinner()
        requestRefresh = collection.find({"gameID": server["gameID"]})
        serverState = 0
        for i in requestRefresh:
            if i["gameID"] == server["gameID"]:
                serverState = i
                break
        if serverState == 0:
            t = False
            moncanevas.destroy()
            createWindow()
            return print("Server Ended while being in the game")
        possibleLines = serverState["PossibleLines"]
        keepTrackBoxes = serverState["KeepTrackBoxes"]
        inGameUsingInteractionServer = serverState
        Turn = serverState["Turn"]
        if serverState["NOP"] < 2:
            return print("Player has left !")
        for i in range(0, len(serverState["KeepTrackBoxes"])):
            if serverState["KeepTrackBoxes"][i][1] == 0:
                _t = createCross(serverState["KeepTrackBoxes"][i][0])
            else:
                _t = createCircle(serverState["KeepTrackBoxes"][i][0])
        if t == True:
            a = window.after(150, lambda v=0: updatePanel(True))
        return



    
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
        checkLines()
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
        checkLines()
        return True

    _ =updatePanel(True)
    ignition()



def comparePassword(server, password, library):
    global storeObjects
    refreshServer = collection.find({"gameID": server["gameID"]})
    isOnline = False
    for i in refreshServer:
        if i["gameID"] == server["gameID"]:
            isOnline = True
    if isOnline == False:
        label_ = Label(window, text="Server has been deleted. Redirecting...", width =15)
        storeObjects["buttons"].append(label_)
        label_.place(x = 115, y = 40)
        a = window.after(500, lambda v=0: commandButton("find"))
        return
    if server["RequestsPassword"][1] == password.get():
        idUpdater = {"gameID": server["gameID"]}
        newValues = {"$set": {"NOP": 2}}
        collection.update_one(idUpdater, newValues)
        idUpdater = {"gameID": server["gameID"]}
        newValues = {"$set": {"launch": True}}
        collection.update_one(idUpdater, newValues)
        kptl = loadingAnimationText(library["variationloader"], {"animationLength": 60, "animationSpeed": 5, "functionToLaunch": __start_game_preperation__}, server)
    else:
        print("ayo")
        return False




def connexionLaunched(server, library):
    global findGames
    global SoloGame
    global CreateGame
    global exists_
    global storeObjects
    global keepIdOfJoin
    global preventIsActive
    fetchData = collection.find({"gameID":server["gameID"]})
    exists_ = False
    for i in fetchData: 
        exists_ = True
        if i["NOP"] > 2:
            return
    keepIdOfJoin = server["gameID"]
    if exists_ == True:
        if server["RequestsPassword"][0] == True and preventIsActive == False:
            for i in range(0, len(storeObjects["buttons"])):
                storeObjects["buttons"][i].destroy()
            storeObjects = {'buttons': [], 'windows': []}
            passwordVar = StringVar()
            passwordEntry = Entry(window, textvariable=passwordVar)
            validateButton = Button(window, width=15, text="Submit", command=lambda v=0: comparePassword(server, passwordVar, library))
            returnButton = Button(window, text="Return", width=10, command= lambda v=0: commandButton("find"))
            storeObjects["buttons"].append(validateButton)
            storeObjects["buttons"].append(passwordEntry)      
            storeObjects["buttons"].append(returnButton)      
            validateButton.place(x = 115, y =200)
            passwordEntry.place(x=115, y = 150)
            returnButton.place(x= 10, y = 40)
        else:
            idUpdater = {"gameID": server["gameID"]}
            newValues = {"$set": {"NOP": 2}}
            collection.update_one(idUpdater, newValues)
            idUpdater = {"gameID": server["gameID"]}
            newValues = {"$set": {"launch": True}}
            collection.update_one(idUpdater, newValues)
            kptl = loadingAnimationText(library["variationloader"], {"animationLength": 60, "animationSpeed": 5, "functionToLaunch": __start_game_preperation__}, server)


def __start_game_preperation__(library, server):
        holder = library.get("destroyButtons", {"buttons": [], "windows": []})
        for i in range(0, len(holder["buttons"])):
            holder["buttons"][i].destroy()
        for i in range(0, len(holder["windows"])):
            holder["windows"][i].destroy()
        findGames.destroy()
        SoloGame.destroy()
        CreateGame.destroy()
        initGame(library, server)     

def loadingAnimationText(textVariable, library, server):
    animationLength = library.get("animationLength", 15)
    animationSpeed = library.get("animnationSpeed", 60)
    if library.get("Counter", 0) >= animationLength:
        if library.get("functionToLaunch", 0) != 0:
            library.get("functionToLaunch", 0)(library, server)
        return True
    else:
        library.update({"Counter": library.get("Counter", 0) + 1})
        textVariable.set( "." + "." * (library.get("Counter", 0)%3))
        a = window.after(animationSpeed, lambda v=0: loadingAnimationText(textVariable, library, server))

def commandButton(type_):
    global serverCreationDict
    global refreshRate
    global OwnsGame
    global storeObjects
    global preventIsActive
    serverCreationDict = {
        "name": "",
        "RequestsPassword": [False],
    }
    if preventIsActive == True:
        return
    if type_ == "find":
        refreshRate = refreshRate + 1
        for i in range(0, len(storeObjects["buttons"])):
            storeObjects["buttons"][i].destroy()
        for i in range(0, len(storeObjects["windows"])):
            storeObjects["windows"][i].destroy()
        storeObjects = {'buttons': [], 'windows': []}
        OwnsGame = 1
        yeld = []
        fetchData = collection.find({"NOP": 1})
        global game
        game = 0
        for i in fetchData:
            if i["NOP"] < 2:
                yeld.append(i)
                game = i
        if game == 0:
            newLabel = Label(window, text='No available servers found. \n \n Search algorythem functionnal: \n The lack of servers is not due to an outage. \n \n Possible errors will appear below: \n Output: 0 (no error) | Errors: nil (no error) \n \n Refresh rate: ' + str(refreshRate), width= 70)
            refresh = Button(window, text='Refresh', width= 10, command = lambda v=0: commandButton("find"))
            create = Button(window, text='Create Server', width= 10, command = lambda v=0: commandButton("create"))
            storeObjects["buttons"].append(newLabel)
            storeObjects["buttons"].append(refresh)
            storeObjects["buttons"].append(create)
            refresh.place(x = 130, y= 270)
            newLabel.place(x= -75, y= 110)
            create.place(x= 130, y= 310)
        else:
            loadingVariation = StringVar()
            loadingLabel = Label(window, textvariable=loadingVariation, width=10)
            loadingLabel.place(x= 280, y= 370)
            for i in range(0, len(yeld)):
                newButton =Button(window, text= "Join " + yeld[i]["Name"] + str(i + 1), width = 15, command = lambda v = i: connexionLaunched(yeld[v], {"textloader": loadingLabel, "variationloader": loadingVariation, "Counter": 0, "destroyButtons": storeObjects}))
                newButton.place(x = 105, y = 50 + 30 * (i + 1))
                storeObjects["buttons"].append(newButton)
    elif type_ == "create":
            for i in range(0, len(storeObjects["buttons"])):
                storeObjects["buttons"][i].destroy()
            for i in range(0, len(storeObjects["windows"])):
                storeObjects["windows"][i].destroy()
            storeObjects = {'buttons': [], 'windows': []}
            OwnsGame = 0
            serverNameVar = StringVar()
            changeVisibilityVar = StringVar()
            serverPasswordVar = StringVar()
            serverPasswordVar.set("Set Password")
            changeVisibilityVar.set("Set Private")
            serverName = Entry(window, textvariable=serverNameVar)
            serverPassword = Entry(window, textvariable=serverPasswordVar)
            changeVisibility = Button(window, textvariable=changeVisibilityVar, width=15, command= lambda v=0: createServerInteraction("CHANGE_VISIBILITY", [changeVisibilityVar, [serverPassword, serverPasswordVar]], 0))
            instructionLabel = Label(window, width=15, text='Enter Server Name')
            createServer = Button(window, text='Create Server', width= 15, command= lambda v=0: createServerInteraction("CREATESERVER", serverName, serverPasswordVar))
            storeObjects["buttons"].append(serverName)
            storeObjects["buttons"].append(changeVisibility)
            storeObjects["buttons"].append(instructionLabel)
            storeObjects["buttons"].append(createServer)
            storeObjects["buttons"].append(serverPassword)
            serverName.place(x = 110, y = 130)
            instructionLabel.place(x = 115, y = 105)
            createServer.place(x = 115, y = 300)
            changeVisibility.place(x= 115, y = 180)
            serverPassword.place(x= 5000, y = 50000)



def createServerInteraction(type_, buttonVariationText, password):
    global serverCreationDict
    global holdGameIDOwner
    if type_ == "CHANGE_VISIBILITY": 
        if serverCreationDict["RequestsPassword"][0] == False:
            serverCreationDict["RequestsPassword"] = [True, ""]
            buttonVariationText[1][0].place(x = 115, y = 230)
            buttonVariationText[0].set("Set Public")
        else:
            serverCreationDict["RequestsPassword"][0] = False
            serverCreationDict["RequestsPassword"].pop()
            buttonVariationText[1][0].place(x = 50000, y = 50000)
            buttonVariationText[0].set("Set Private") 
    elif type_ == "CREATESERVER":
        probableID = findAvailableID()
        if probableID == False:
            return print("No available ID ! Fatal Error.")
        serverCreationDict["name"] = buttonVariationText.get()
        if  serverCreationDict["RequestsPassword"][0] == True:
            serverCreationDict["RequestsPassword"][1] = password.get()
        holdGameIDOwner = probableID
        ServerParam = {
            "gameID": probableID,
            "Name": serverCreationDict["name"],
            "RequestsPassword": serverCreationDict["RequestsPassword"],
            "NOP": 1,
            "lanch": False,
            "KeepTrackBoxes": [],
            "PossibleLines": [[[1,1], [2, 1], [3, 1]],[[1,2], [2,2], [3,2]], [[1,3], [2,3], [3,3]], 
            [[1,1], [1, 2], [1, 3]], [[2, 1], [2,2], [2,3]], [[3,1], [3, 2], [3,3]], [[1,1], [2,2], 
            [3,3]], [[3,1], [2,2], [1,3]]],
            "Turn": 0
        }
        collection.insert_one(ServerParam)
        preventFromMoving()



def preventFromMoving():
    global preventIsActive
    global storeObjects
    preventIsActive = True
    for i in range(0, len(storeObjects["buttons"])):
        storeObjects["buttons"][i].destroy()
    for i in range(0, len(storeObjects["windows"])):
        storeObjects["windows"][i].destroy()
    storeObjects = {'buttons': [], 'windows': []}
    WaitingStatusVar = StringVar()
    WaitingStatusVar.set("Waiting For Player...")
    WaitingLabel = Label(window, textvariable=WaitingStatusVar, width=25)
    DeleteButton = Button(window, text="Delete Server", width = 15, command = deleteServer)
    storeObjects["buttons"].append(WaitingLabel)
    storeObjects["buttons"].append(DeleteButton)
    WaitingLabel.place(x = 75, y = 100)
    DeleteButton.place(x = 110, y= 250)  
    detectConnexion(WaitingStatusVar)


def detectConnexion(var):
    global preventIsActive
    global holdGameIDOwner
    global _server_
    _server_ = 0
    fetchData = collection.find({"gameID":holdGameIDOwner})
    for i in fetchData:
        if i["gameID"] == holdGameIDOwner:
            _server_ = i
    if _server_ == 0:
        if preventIsActive == False:
            return
    if _server_["NOP"] == 2:
        findGames.destroy()
        SoloGame.destroy() 
        CreateGame.destroy()
        connexionLaunched(_server_, {"variationloader": var})
        return
    a = window.after(30, lambda v=0: detectConnexion(var))


            


def deleteServer():
    global preventIsActive
    global holdGameIDOwner
    fetchData = collection.find({"gameID":holdGameIDOwner})
    for i in fetchData:
        if i["gameID"] == holdGameIDOwner:
            collection.delete_one({"gameID": holdGameIDOwner})
            preventIsActive = False
    preventIsActive = False
    commandButton("create")
    return

def windowClosing():
    global holdGameIDOwner
    global keepIdOfJoin
    fetchData = collection.find({"gameID":holdGameIDOwner})
    for i in fetchData:
        if i["gameID"] == holdGameIDOwner:
            collection.delete_one({"gameID": holdGameIDOwner})
    for i in fetchData:
        if i["gameID"] == keepIdOfJoin:
            print("deleted")
            collection.delete_one({"gameID": keepIdOfJoin})
    
    window.destroy()



window.protocol("WM_DELETE_WINDOW", windowClosing)




def findAvailableID():
    global id_to_use
    id_to_use = False
    for i in range(0, 1000):
        ID = genID()
        fetchData = collection.find({"gameID":ID})
        global a
        a = 0
        for i in fetchData:
            a = 1
            if i["gameID"] == ID:
                print("ID in use !")
            else:
                id_to_use = ID
                break
        if a == 0:
            return ID
    return id_to_use
                
 


def playSolo():
    window.destroy()
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


def genID():
    randomID = randint(0, 999999999999)
    randomID = "id" + str(randomID) + (randint(0, 10) * "-")
    return randomID



def createWindow():
    global findGames
    global SoloGame
    global CreateGame
    global window
    window.title("Find Game")
    window.geometry("340x400")
    findGames, CreateGame, SoloGame = Button(window, text = "Find Session",width=10, command= lambda v=0: commandButton("find")), Button(window, text = "Create Session", width=10, command= lambda v=0: commandButton("create")), Button(window, text = "Play Offline", width=10, command= lambda v=0: playSolo())
    findGames.place(x= 10, y=10)
    CreateGame.place(x= 130, y = 10)
    SoloGame.place(x= 250, y = 10)




createWindow()





window.mainloop()
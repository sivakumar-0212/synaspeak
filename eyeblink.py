import cv2
import time
import cvzone
from cvzone.FaceMeshModule import FaceMeshDetector
from cvzone.PlotModule import LivePlot
 
cap = cv2.VideoCapture(0)
detector = FaceMeshDetector(maxFaces=1)
plotY = LivePlot(640, 360, [20, 50], invert=True)
 
idList = [22, 23, 24, 26, 110, 157, 158, 159, 160, 161, 130, 463,252,253,254,256,339,359,384,385,386,387,388,359]

ratioList = []
symbol=""
bstate="opened"
counter = 0
color = (255, 0, 255)
blink_start_time = None
oblink_start = None
i=1
word=""
sent=""
 
while True:
 
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
 
    success, img = cap.read()
    img, faces = detector.findFaceMesh(img, draw=False)
 
    if faces:
        face = faces[0]
        for id in idList:
            cv2.circle(img, face[id], 5,color, cv2.FILLED)
 
        leftUp = face[159]
        leftDown = face[23]
        leftLeft = face[130]
        leftRight = face[243]
        llenghtVer, _ = detector.findDistance(leftUp, leftDown)
        llenghtHor, _ = detector.findDistance(leftLeft, leftRight)
        rightup = face[386]
        rightdown = face[253]
        rightright = face[359]
        rightleft = face[463]
        rlenghtVer,_= detector.findDistance(rightup,rightdown)
        rlenghtHor, _=detector.findDistance(rightleft,rightright)
 
        # cv2.line(img, leftUp, leftDown, (0, 200, 0), 3)
        # cv2.line(img, leftLeft, leftRight, (0, 200, 0), 3)
 
        lratio = int((llenghtVer / llenghtHor) * 100)
        rratio = int((rlenghtVer/rlenghtHor)*100)
        ratio = int((rratio+lratio)/2)
        
        ratioList.append(ratio)
        if len(ratioList) > 3:
            ratioList.pop(0)
        ratioAvg = sum(ratioList) / len(ratioList)
 
        if ratioAvg <= 33 and counter == 0:
            bstate="closed"
            
            if blink_start_time is None:
                blink_start_time = time.time()
                
            if oblink_start is not None:
                oblink_end = time.time()
                oblink_dur = oblink_end - oblink_start
                print(f"open Duration: {oblink_dur:.2f} seconds")
            
                if(oblink_dur >= 2.0):
                    if(symbol == ".-"):
                        letter="A"
                    elif(symbol == "-..."):
                        letter="B"
                    elif(symbol == "-.-."):
                        letter="C"
                    elif(symbol == "-.."):
                        letter="D"
                    elif(symbol == "."):
                        letter="E"
                    elif(symbol == "..-."):
                        letter="F"
                    elif(symbol == "--."):
                        letter="G"
                    elif(symbol == "...."):
                        letter="H"
                    elif(symbol == ".."):
                        letter="I"
                    elif(symbol == ".---"):
                        letter="J"
                    elif(symbol == "-.-"):
                        letter="K"
                    elif(symbol == ".-.."):
                        letter="L"
                    elif(symbol == "--"):
                        letter="M"
                    elif(symbol == "-."):
                        letter="N"
                    elif(symbol == "---"):
                        letter="O"
                    elif(symbol == ".--."):
                        letter="P"
                    elif(symbol == "--.-"):
                        letter="Q"
                    elif(symbol == ".-."):
                        letter="R"
                    elif(symbol == "..."):
                        letter="S"
                    elif(symbol == "-"):
                        letter="T"
                    elif(symbol == "..-"):
                        letter="U"
                    elif(symbol == "...-"):
                        letter="V"
                    elif(symbol == ".--"):
                        letter="W"
                    elif(symbol == "-..-"):
                        letter="X"
                    elif(symbol == "-.--"):
                        letter="Y"
                    elif(symbol == "--.."):
                        letter="Z"
                    elif(symbol == ".----"):
                        letter="1"
                    elif(symbol == "..---"):
                        letter="2"
                    elif(symbol == "...--"):
                        letter="3"
                    elif(symbol == "....-"):
                        letter="4"
                    elif(symbol == "....."):
                        letter="5"
                    elif(symbol == "-...."):
                        letter="6"
                    elif(symbol == "--..."):
                        letter="7"
                    elif(symbol == "---.."):
                        letter="8"
                    elif(symbol == "----."):
                        letter="9"
                    elif(symbol == "-----"):
                        letter="0"
                    else:
                        letter="ERROR"
                        word=""
                    word = word + letter
                    symbol=""
                    
                if(oblink_dur >=4.0):
                    sent=sent+" "+word
                    word=""               
                
                oblink_start = None
    
            color = (0,200,0)
            counter = 1
            
        if counter != 0:
            counter += 1
            if counter > 10:
                counter = 0
                color = (255,0, 255)
                
        elif  ratioAvg > 33:
            bstate="opened"
            if blink_start_time is not None:
                blink_end_time = time.time()
                blink_duration = blink_end_time - blink_start_time
                print(f"Blink Duration: {blink_duration:.2f} seconds")
                blink_start_time = None
                
                if(blink_duration>=0.80):
                    print(i)
                    value="-"
                else:
                    value="."
                    print(i)
                i+=1
                symbol=symbol+value
                print(symbol)
                
                if oblink_start is None:
                    oblink_start=time.time()
 
        cvzone.putTextRect(img,f'Blink state :{bstate}', (100, 50),scale=2,colorR=color)
        cvzone.putTextRect(img,f'word :{word}', (100, 100),thickness=2,scale=2,colorR=color)
        cvzone.putTextRect(img,f'sentance :{sent}', (100,450),thickness=2,scale=2,colorR=color)

        
        imgPlot = plotY.update(ratioAvg, color)
        img = cv2.resize(img, (640, 360))
        imgStack = cvzone.stackImages([img, imgPlot], 2, 1)
    else:
        img = cv2.resize(img, (700, 360))
        imgStack = cvzone.stackImages([img, img], 2, 1)
 
    cv2.imshow("Image", imgStack)
    cv2.waitKey(25)
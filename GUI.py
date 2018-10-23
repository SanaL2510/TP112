import numpy as np
import cv2
import tkinter 
import PIL.Image
import PIL.ImageTk
import makeup
import imutils
from imutils import face_utils
from tkinter import *
import os
import webscrapeTopRated
import webbrowser
import twilioSMS
from tkinter.filedialog import askopenfilename


####################

def loadSwatches(data):
    images = []
    dirpath = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/")
    pathToFeature = dirpath + "/Colors/%s" %(data.currentFeature)
    files = os.listdir(pathToFeature)
    for image in files:
        path = pathToFeature + "/" + image
        images += [path]
    swatches = []
    for pic in range(len(images)):
        photo = cv2.imread(images[pic])
        photo = cv2.cvtColor(photo, cv2.COLOR_BGR2RGB)
        photo = imutils.resize(photo, width = 36, inter = cv2.INTER_CUBIC)
        photo2 = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(photo))
        photoData = [photo2, pic*36 + data.scrollX, photo]
        swatches += [photoData]
    return swatches

def loadTopProducts(feature, data):
    dirpath = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/")
    pathToFeature = dirpath + "/Top Products/%s" %(feature)
    files = os.listdir(pathToFeature)
    images = []
    for image in files:                                
        path = pathToFeature + "/" + image
        images += [path]
    products = []
    for pic in range(len(images)):
        photo = cv2.imread(images[pic])
        photo = cv2.cvtColor(photo, cv2.COLOR_BGR2RGB)
        photo = imutils.resize(photo, width = 100, inter = cv2.INTER_CUBIC)
        photo2 = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(photo))
        photoData = [photo2, pic*100 + data.scrollY, photo]
        products += [photoData]
    return products

def convertPhoto(data):
    img = cv2.cvtColor(data.image, cv2.COLOR_BGR2RGB)
    img = imutils.resize(img, width = 500, inter = cv2.INTER_CUBIC)
    photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(img))
    return photo 

def makeover(data):
    image = cv2.imread(data.imagePath)
    for product in data.products:
        data.objects[product].img = image
    for product in data.products:
        image = data.objects[product].editPhoto()
    return image

def drawSwatches(canvas, data):
    for i in range(len(data.swatches)):
        placement = i * 36
        canvas.create_image(placement + data.scrollX, data.height - 36, image = data.swatches[i][0], anchor = tkinter.NW)

def drawTopProducts(canvas, data):
    for i in range(len(data.topProducts)):
        placement = i*100
        canvas.create_image(600, placement + data.scrollY, image = data.topProducts[i][0], anchor = tkinter.NW)

def init(data): 
    print(data.imagePath)
    data.image = cv2.imread(data.imagePath)
    data.photo = convertPhoto(data)
    data.dimX, data.dimY, nc = data.img.shape
    data.products = ["lips", "shadow", "liner", "brows", "contour", "highlight", "blush"] 
    data.currentFeature = data.products[0]
    data.targets = {"lips" : webscrapeTopRated.getTopProducts("lips"), 
    "shadow" : webscrapeTopRated.getTopProducts("shadow"), 
    "liner" : webscrapeTopRated.getTopProducts("liner"), 
    "brows" : webscrapeTopRated.getTopProducts("brows"), 
    "contour" : webscrapeTopRated.getTopProducts("contour"), 
    "highlight" : webscrapeTopRated.getTopProducts("highlight"), 
    "blush" : webscrapeTopRated.getTopProducts("blush")}
    # data.edited = dict()
    data.scrollX = 0
    data.scrollY = 0
    data.swatches = loadSwatches(data)
    data.topProducts = {"lips" : loadTopProducts("lips", data), 
    "shadow" : loadTopProducts("shadow", data), 
    "liner" : loadTopProducts("liner", data), 
    "brows" : loadTopProducts("brows", data), 
    "contour" : loadTopProducts("contour", data), 
    "highlight" : loadTopProducts("highlight", data), 
    "blush" : loadTopProducts("blush", data)}
    data.lips = makeup.Lips(data.image, "lips", 0.1, None)
    data.shadow = makeup.Shadow(data.image, "shadow", 0.1, None)
    data.liner = makeup.Liner(data.image, "liner", 0.6, None)
    data.brows = makeup.Brows(data.image, "brows", 0.1, None)
    data.contour = makeup.Contour(data.image, "contour", 0.1, None)
    data.highlight = makeup.Highlight(data.image, "highlight", 0.1, None)
    data.blush = makeup.Blush(data.image, "blush", 0.1, None)
    data.objects = {"lips" : data.lips, 
    "shadow" : data.shadow, 
    "liner" : data.liner, 
    "brows" : data.brows, 
    "contour" : data.contour, 
    "highlight" : data.highlight, 
    "blush" : data.blush}
    data.popup = False 
    data.input = ""
    print("Done")

def mousePressed(event, data):
    if 0 <= event.x <= 500 and data.height-36 <= event.y <= data.height:
        index = (event.x - data.scrollX)//36
        currentImage = data.swatches[index][2]
        currentColor = currentImage[17, 17]
        (r, g, b) = (int(currentColor[0]), int(currentColor[1]), int(currentColor[2]))
        data.objects[data.currentFeature].color = (b, g, r)
    for j in range(0, data.height, data.height//len(data.products)):
        if 500 <= event.x <= 600:
            if j <= event.y <= j + data.height//len(data.products):
                data.currentFeature = data.products[j//(data.height//len(data.products))]
                data.scrollX = 0
                data.scrollY = 0
                event.x = 0
                event.y = 0
                print(data.currentFeature)
    if 15 <= event.x <= 105 and data.height - 165 <= event.y <= data.height - 120:
        if data.objects[data.currentFeature].alphaMax >= data.objects[data.currentFeature].alpha:
            data.objects[data.currentFeature].alpha += 0.025
            print(data.objects[data.currentFeature].alpha)    
    if 15 <= event.x <= 105 and data.height - 105 <= event.y <= data.height - 60:
        if data.objects[data.currentFeature].alphaMin < data.objects[data.currentFeature].alpha:
            data.objects[data.currentFeature].alpha -= 0.025
            print(data.objects[data.currentFeature].alpha)
    if 600 < event.x <= data.width:
        index = ((event.y - data.scrollY) - 50)//100
        link = "http://sephora.com" + data.targets[data.currentFeature][index]
        webbrowser.open(link)
    if 380 <= event.x <= 470 and data.height - 105 <= event.y <= data.height - 60:
        data.popup = True
    if 310 <= event.x <= 360 and 200 <= event.y <= 250:
        path = os.path.dirname(data.imagePath) + "finalImage.jpg"
        cv2.imwrite(path, data.image)
        try:
            twilioSMS.getPhotoSendMessage(path, int(data.input))
            data.input = ""
            data.popup = False
        except:
            data.popup = False
    data.image = makeover(data)
    data.photo = convertPhoto(data)
    data.swatches = loadSwatches(data)


def keyPressed(event, data):
    if event.keysym == "Left":
        data.scrollX += 10
        print(data.scrollX)
    if event.keysym == "Right":
        data.scrollX -= 10
        print(data.scrollX)
    if event.keysym == "Up":
        data.scrollY += 10
        print(data.scrollY)
    if event.keysym == "Down":
        data.scrollY -= 10
        print(data.scrollY)
    if data.popup == True and str(event.char) in "1234567890":
        data.input = str(data.input) 
        data.input += str(event.char)
        data.input = int(data.input)
    if data.popup == True and event.keysym == "BackSpace":
        data.input = str(data.input) 
        if len(data.input) > 0:
            data.input = data.input[0:-1]
            data.input = int(data.input)
        else: 
            data.input = ""


def redrawAll(canvas, data):
    canvas.create_image(0, 0, image = data.photo, anchor = tkinter.NW)
    for i in range(len(data.swatches)):
        placement = i * 36
        canvas.create_image(placement + data.scrollX, data.height - 36, image = data.swatches[i][0], anchor = tkinter.NW)
    canvas.create_rectangle(600, 0, data.width, data.height, fill = "white", width = 0)
    for i in range(len(data.topProducts[data.currentFeature])):
        placement = i*100 + 50
        canvas.create_image(600, placement + data.scrollY, image = data.topProducts[data.currentFeature][i][0], anchor = tkinter.NW)
    for j in range(0, data.height, round(data.height/len(data.products))):
        index = j//(data.height//len(data.products))
        canvas.create_rectangle(500, j, 600, j+100, fill = "white", width = 10) 
        canvas.create_text(550, j + 50, text = "%s" %(data.products[index]), fill = "Black", font = "Arial 15")
    canvas.create_rectangle(605, 0, data.width, 50, fill = "white", width = 0)
    canvas.create_text(612, 0, text = "Bestsellers", fill = "Black", font = "Arial 15", anchor = tkinter.NW)
    canvas.create_text(610, 20, text = "on Sephora", fill = "Black", font = "Arial 15", anchor = tkinter.NW)
    canvas.create_rectangle(15, data.height - 165, 105, data.height - 120, fill = "white", width = 5)
    canvas.create_text(60, data.height - 143, text = "%s" %("sharpen"), fill = "Black", font = "Arial 15")
    canvas.create_rectangle(15, data.height - 105, 105, data.height - 60, fill = "white", width = 5)
    canvas.create_text(60, data.height - 83, text = "%s" %("blend"), fill = "Black", font = "Arial 15")
    canvas.create_rectangle(380, data.height - 105, 470, data.height - 60, fill = "white", width = 5)
    canvas.create_text(425, data.height - 83, text = "%s" %("text me!"), fill = "Black", font = "Arial 15")
    if data.popup == True:
        canvas.create_rectangle(200, 200, 300, 250, fill = "white", width = 5)
        canvas.create_text(250, 225, text = "%s" %(str(data.input)), fill = "Black", font = "Arial 10")
        canvas.create_rectangle(310, 200, 360, 250, fill = "white", width = 5)
        canvas.create_text(335, 225, text = "Done!", fill = "Black")

    # for i in range(len(data.swatches)):
    #     xPlacement = i*36 + 18
    #     canvas.create_image(xPlacement, data.height - 18, \
    #         image = "C:/Users/sanam/Documents/CMU/Year 1/Semester 2/15-112 Fundamentals of Programming/Term Project/Colors/%s" \
    #         %(data.swatches[i]))
    

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    root = tkinter.Tk()

    data.imagePath = askopenfilename()
    data.img = cv2.imread(data.imagePath)
    data.img = cv2.cvtColor(data.img, cv2.COLOR_BGR2RGB)
    data.img = imutils.resize(data.img, width = 500, inter = cv2.INTER_CUBIC)

    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()

    data.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(data.img))
    canvas.create_image(0, 0, image = data.photo, anchor = tkinter.NW)

    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    redrawAll(canvas, data)
    print("Done")
    # and launch the app
    root.mainloop()  # blocks until window is closed

run(710, 600) 
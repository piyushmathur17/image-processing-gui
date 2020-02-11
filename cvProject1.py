#!/usr/bin/env python
# coding: utf-8

# In[3]:


from tkinter import *
import os
from PIL import Image
import ctypes
from PIL import ImageTk
from PIL import ImageOps
from tkinter import filedialog
from tkinter import messagebox
import imghdr
from collections import*
import numpy as np
import cv2
import scipy
from scipy import ndimage


# In[2]:


undoStack=[]


# In[3]:


def sobel(canvas):
    canvas.data.cropPopToHappen=False
    canvas.data.colourPopToHappen=False
    canvas.data.drawOn=False
    img = np.asarray(canvas.data.image)
    
    im=img
    im = im.astype('int32')
    dx = ndimage.sobel(im, 0)  # horizontal derivative
    dy = ndimage.sobel(im, 1)  # vertical derivative
    mag = np.hypot(dx, dy)  # magnitude
    mag *= 255.0 / np.max(mag)

    
    canvas.data.image=Image.fromarray(mag.astype(np.uint8))
    canvas.data.undoQueue.append(canvas.data.image.copy())
    canvas.data.imageForTk=makeImageForTk(canvas)
    drawImage(canvas)


def smoothenImg3(canvas):
    canvas.data.cropPopToHappen=False
    canvas.data.colourPopToHappen=False
    canvas.data.drawOn=False
    img = np.asarray(canvas.data.image)
    
    kernel = np.ones((3,3),np.float32)/9
    dst = cv2.filter2D(img,-1,kernel)
    
    canvas.data.image=Image.fromarray(dst)
    canvas.data.undoQueue.append(canvas.data.image.copy())
    canvas.data.imageForTk=makeImageForTk(canvas)
    drawImage(canvas)
def smoothenImg5(canvas):
    canvas.data.cropPopToHappen=False
    canvas.data.colourPopToHappen=False
    canvas.data.drawOn=False
    img = np.asarray(canvas.data.image)
    
    kernel = np.ones((5,5),np.float32)/25
    dst = cv2.filter2D(img,-1,kernel)
    
    canvas.data.image=Image.fromarray(dst)
    canvas.data.undoQueue.append(canvas.data.image.copy())
    canvas.data.imageForTk=makeImageForTk(canvas)
    drawImage(canvas)
def smoothenImg7(canvas):
    canvas.data.cropPopToHappen=False
    canvas.data.colourPopToHappen=False
    canvas.data.drawOn=False
    img = np.asarray(canvas.data.image)
    
    kernel = np.ones((7,7),np.float32)/49
    dst = cv2.filter2D(img,-1,kernel)
    
    canvas.data.image=Image.fromarray(dst)
    canvas.data.undoQueue.append(canvas.data.image.copy())
    canvas.data.imageForTk=makeImageForTk(canvas)
    drawImage(canvas)


def smoothenImg(canvas):
    
    canvas.data.colourPopToHappen=False
    canvas.data.cropPopToHappen=False
    canvas.data.drawOn=False
    emtWindow=Toplevel(canvas.data.mainWindow)
    emtWindow.title("Smoothen")
    Width=50
    Height=50
    canvas.data.emtCanvasWidth=14
    canvas.data.emtCanvasHeight=20
    emtCanvas = Canvas(emtWindow, width=Width,                         height=Height)
    
    emtCanvas.pack()
    smoothButtonsInit(emtWindow,canvas)
    #emtCanvas.data.image=canvas.data.image.copy()
    canvas.data.imageForTk=makeImageForTk(canvas)
    drawImage(canvas)
    
def smoothButtonsInit(root, canvas):
    backgroundColour="gray50"
    buttonWidth=14
    buttonHeight=2
    emttoolKitFrame=Frame(root)
    s1=Button(emttoolKitFrame, text="3X3",                      background=backgroundColour ,                      width=buttonWidth, height=buttonHeight,                       command=lambda:smoothenImg3(canvas))
    s1.grid(row=0,column=0)
    s2=Button(emttoolKitFrame, text="5X5",                        background=backgroundColour,                         width=buttonWidth,height=buttonHeight,                         command=lambda: smoothenImg5(canvas))
    s2.grid(row=1,column=0)
    s3=Button(emttoolKitFrame, text="7X7",                            background=backgroundColour ,                            width=buttonWidth, height=buttonHeight,                            command=lambda: smoothenImg7(canvas))
    s3.grid(row=2,column=0)
   
    resetButton=Button(emttoolKitFrame, text="Reset",                       background=backgroundColour ,width=buttonWidth,                       height=buttonHeight, command=lambda: reset(canvas))
    resetButton.grid(row=3,column=0)
    saveChanges=Button(emttoolKitFrame,text="saveChanges",                        background=backgroundColour, width=buttonWidth,                        height=buttonHeight,command=lambda: saveChanges(canvas))
    saveChanges.grid(row=4,column=0)
    #Please comment this button out if you use this on any OS apart from Windows
    
    emttoolKitFrame.pack(side=LEFT)


# In[19]:


def closeHistWindow(canvas):
    if canvas.data.image!=None:
        save(canvas)
        canvas.data.undoQueue.append(canvas.data.image.copy())
        canvas.data.histWindowClose=True

def histogram(canvas):
    canvas.data.colourPopToHappen=False
    canvas.data.cropPopToHappen=False
    canvas.data.drawOn=False
    histWindow=Toplevel(canvas.data.mainWindow)
    histWindow.title("Histogram")
    canvas.data.histCanvasWidth=350
    canvas.data.histCanvasHeight=475
    histCanvas = Canvas(histWindow, width=canvas.data.histCanvasWidth,                         height=canvas.data.histCanvasHeight)
    histCanvas.pack()
    # provide sliders to the user to manipulate red, green and blue amounts in the image
    redSlider=Scale(histWindow, from_=-100, to=100,                     orient=HORIZONTAL, label="R")
    redSlider.pack()
    blueSlider=Scale(histWindow, from_=-100, to=100,                     orient=HORIZONTAL, label="B")
    blueSlider.pack()
    greenSlider=Scale(histWindow, from_=-100, to=100,                      orient=HORIZONTAL, label="G")
    greenSlider.pack()
    OkHistFrame=Frame(histWindow)
    OkHistButton=Button(OkHistFrame, text="OK",                         command=lambda: closeHistWindow(canvas))
    OkHistButton.grid(row=0,column=0)
    OkHistFrame.pack(side=BOTTOM)
    initialRGB=(0,0,0)
    changeColours(canvas, redSlider, blueSlider,                   greenSlider, histWindow, histCanvas, initialRGB)


def changeColours(canvas, redSlider, blueSlider,                   greenSlider, histWindow, histCanvas, previousRGB):
    undoStack.append(canvas.data.image)
    flag=0
    if canvas.data.histWindowClose==True:
        histWindow.destroy()
        canvas.data.histWindowClose=False
    else:
        # the slider value indicates the % by which the red/green/blue
        # value of the pixels of the image need to incresed (for +ve values)
        # or decreased (for -ve values)
        if canvas.data.image!=None and histWindow.winfo_exists() :
            R, G, B= canvas.data.image.split()
            sliderValR=redSlider.get()
            (previousR, previousG, previousB)= previousRGB
            scaleR=(sliderValR-previousR)/100.0
            R=R.point(lambda i: i+ int(round(i*scaleR)))
            sliderValG=greenSlider.get()
            scaleG=(sliderValG-previousG)/100.0
            G=G.point(lambda i: i+ int(round(i*scaleG)))
            sliderValB=blueSlider.get()
            scaleB=(sliderValB-previousB)/100.0
            B=B.point(lambda i: i+ int(round(i*scaleB)))
            canvas.data.image = Image.merge(canvas.data.image.mode, (R, G, B))
            if (previousR!=scaleR or previousG!=scaleG or previousB!=scaleB) : flag=1
            if flag!=1:
                undoStack.pop()
                
            canvas.data.imageForTk=makeImageForTk(canvas)
            drawImage(canvas)
            displayHistogram(canvas, histWindow, histCanvas)
            previousRGB=(sliderValR, sliderValG, sliderValB)
            canvas.after(200, lambda: changeColours(canvas, redSlider,                blueSlider, greenSlider,  histWindow, histCanvas, previousRGB))

def displayHistogram(canvas,histWindow, histCanvas):
    histCanvasWidth=canvas.data.histCanvasWidth
    histCanvasHeight=canvas.data.histCanvasHeight
    margin=50
    if canvas.data.image!=None:
        histCanvas.delete(ALL)
        im=canvas.data.image
        #x-axis 
        histCanvas.create_line(margin-1, histCanvasHeight-margin+1,                               margin-1+ 258, histCanvasHeight-margin+1)
        xmarkerStart=margin-1
        for i in range(0,257,64):
            xmarker="%d" % (i)
            histCanvas.create_text(xmarkerStart+i,                                   histCanvasHeight-margin+7, text=xmarker)
        #y-axis
        histCanvas.create_line(margin-1,                                histCanvasHeight-margin+1, margin-1, margin)
        ymarkerStart= histCanvasHeight-margin+1
        for i in range(0, histCanvasHeight-2*margin+1, 50):
            ymarker="%d" % (i)
            histCanvas.create_text(margin-1-10,                                   ymarkerStart-i, text=ymarker)
            
        R, G, B=im.histogram()[:256], im.histogram()[256:512],                  im.histogram()[512:768]
        for i in range(len(R)):
            pixelNo=R[i]
            histCanvas.create_oval(i+margin,                             histCanvasHeight-pixelNo/100.0-1-margin, i+2+margin,                            histCanvasHeight-pixelNo/100.0+1-margin,                                    fill="red", outline="red")
        for i in range(len(G)):
            pixelNo=G[i]
            histCanvas.create_oval(i+margin,                             histCanvasHeight-pixelNo/100.0-1-margin, i+2+margin,                            histCanvasHeight-pixelNo/100.0+1-margin,                                    fill="green", outline="green")
        for i in range(len(B)):
            pixelNo=B[i]
            histCanvas.create_oval(i+margin,                            histCanvasHeight-pixelNo/100.0-1-margin, i+2+margin,                            histCanvasHeight-pixelNo/100.0+1-margin,                                   fill="blue", outline="blue")

def colourPop(canvas):
    canvas.data.cropPopToHappen=False
    canvas.data.colourPopToHappen=True
    canvas.data.drawOn=False
    messagebox.showinfo(title="Colour Pop", message="Click on a part of the image which you want in colour" , parent=canvas.data.mainWindow)
    if canvas.data.cropPopToHappen==False:
        canvas.data.mainWindow.bind("<ButtonPress-1>", lambda event: getPixel(event, canvas))


def getPixel(event, canvas):
    # have to check if Colour Pop button is pressed or not, otherwise, the root
    # events which point to different functions based on what button has been
    # pressed will get mixed up
    try: # to avoid confusion between the diffrent events
        # asscoaited with crop and colourPop
        if canvas.data.colourPopToHappen==True and            canvas.data.cropPopToHappen==False and canvas.data.image!=None :
            data=[]
            # catch the location of the pixel selected by the user
            # multiply it by the scale to get pixel's olaction of the
            #actual image
            canvas.data.pixelx=            int(round((event.x-canvas.data.imageTopX)*canvas.data.imageScale))
            canvas.data.pixely=            int(round((event.y-canvas.data.imageTopY)*canvas.data.imageScale))
            pixelr, pixelg, pixelb=             canvas.data.image.getpixel((canvas.data.pixelx, canvas.data.pixely))
            # the amount of deviation allowed from selected pixel's value
            tolerance=60 
            for y in range(canvas.data.image.size[1]):
                for x in range(canvas.data.image.size[0]):
                    r, g, b= canvas.data.image.getpixel((x, y))
                    avg= int(round((r + g + b)/3.0))
                    # if the deviation of each pixel value > tolerance,
                    # make them gray else keep them coloured
                    if (abs(r-pixelr)>tolerance or
                        abs(g-pixelg)>tolerance or
                        abs(b-pixelb)>tolerance ):
                        R, G, B= avg, avg, avg
                    else:
                        R, G, B=r,g,b
                    data.append((R, G, B))
            canvas.data.image.putdata(data)
            save(canvas)
            canvas.data.undoQueue.append(canvas.data.image.copy())
            canvas.data.imageForTk=makeImageForTk(canvas)
            drawImage(canvas)
    except:
        pass
    canvas.data.colourPopToHappen=False
    

def crop(canvas):
    canvas.data.colourPopToHappen=False
    canvas.data.drawOn=False
    # have to check if crop button is pressed or not, otherwise,
    # the root events which point to
    # different functions based on what button has been pressed
    # will get mixed up 
    canvas.data.cropPopToHappen=True
    messagebox.showinfo(title="Crop",                           message="Draw cropping rectangle and press Enter" ,                          parent=canvas.data.mainWindow)
    if canvas.data.image!=None:
        canvas.data.mainWindow.bind("<ButtonPress-1>",                                     lambda event: startCrop(event, canvas))
        canvas.data.mainWindow.bind("<B1-Motion>",                                    lambda event: drawCrop(event, canvas))
        canvas.data.mainWindow.bind("<ButtonRelease-1>",                                     lambda event: endCrop(event, canvas))

def startCrop(event, canvas):
    # detects the start of the crop rectangle
    if canvas.data.endCrop==False and canvas.data.cropPopToHappen==True:
        canvas.data.startCropX=event.x
        canvas.data.startCropY=event.y

def drawCrop(event,canvas):
    # keeps extending the crop rectange as the user extends
    # his desired crop rectangle
    if canvas.data.endCrop==False and canvas.data.cropPopToHappen==True:
        canvas.data.tempCropX=event.x
        canvas.data.tempCropY=event.y
        canvas.create_rectangle(canvas.data.startCropX,                                 canvas.data.startCropY,
                                 canvas.data.tempCropX, \
            canvas.data.tempCropY, fill="gray", stipple="gray12", width=0)

def endCrop(event, canvas):
    # set canvas.data.endCrop=True so that button pressed movements
    # are not caught anymore but set it to False when "Enter"
    # is pressed so that crop can be performed another time too
    if canvas.data.cropPopToHappen==True:
        canvas.data.endCrop=True
        canvas.data.endCropX=event.x
        canvas.data.endCropY=event.y
        canvas.create_rectangle(canvas.data.startCropX,                                 canvas.data.startCropY,
                                 canvas.data.endCropX, \
            canvas.data.endCropY, fill="gray", stipple="gray12", width=0 )
        canvas.data.mainWindow.bind("<Return>",                                 lambda event: performCrop(event, canvas))

def performCrop(event,canvas):
    canvas.data.image=    canvas.data.image.crop(    (int(round((canvas.data.startCropX-canvas.data.imageTopX)*canvas.data.imageScale)),
    int(round((canvas.data.startCropY-canvas.data.imageTopY)*canvas.data.imageScale)),
    int(round((canvas.data.endCropX-canvas.data.imageTopX)*canvas.data.imageScale)),
    int(round((canvas.data.endCropY-canvas.data.imageTopY)*canvas.data.imageScale))))
    canvas.data.endCrop=False
    canvas.data.cropPopToHappen=False
    save(canvas)
    canvas.data.undoQueue.append(canvas.data.image.copy())
    canvas.data.imageForTk=makeImageForTk(canvas)
    drawImage(canvas)
    
    
    
def rotateFinished(canvas, rotateWindow, rotateSlider, previousAngle):
    if canvas.data.rotateWindowClose==True:
        rotateWindow.destroy()
        canvas.data.rotateWindowClose=False
    else:
        if canvas.data.image!=None and rotateWindow.winfo_exists():
            canvas.data.angleSelected=rotateSlider.get()
            if canvas.data.angleSelected!= None and                canvas.data.angleSelected!= previousAngle:
                canvas.data.image=                canvas.data.image.rotate(float(canvas.data.angleSelected))
                canvas.data.imageForTk=makeImageForTk(canvas)
                drawImage(canvas)
        canvas.after(200, lambda:rotateFinished(canvas,                    rotateWindow, rotateSlider, canvas.data.angleSelected) )


def closeRotateWindow(canvas):
    if canvas.data.image!=None:
        save(canvas)
        canvas.data.undoQueue.append(canvas.data.image.copy())
        canvas.data.rotateWindowClose=True
    
def rotate(canvas):
    canvas.data.colourPopToHappen=False
    canvas.data.cropPopToHappen=False
    canvas.data.drawOn=False
    rotateWindow=Toplevel(canvas.data.mainWindow)
    rotateWindow.title("Rotate")
    rotateSlider=Scale(rotateWindow, from_=0, to=360, orient=HORIZONTAL)
    rotateSlider.pack()
    OkRotateFrame=Frame(rotateWindow)
    OkRotateButton=Button(OkRotateFrame, text="OK",                          command=lambda: closeRotateWindow(canvas))
    OkRotateButton.grid(row=0,column=0)
    OkRotateFrame.pack(side=BOTTOM)
    rotateFinished(canvas, rotateWindow, rotateSlider, 0)

def closeBrightnessWindow(canvas):
    if canvas.data.image!=None:
        save(canvas)
        canvas.data.undoQueue.append(canvas.data.image.copy())
        canvas.data.brightnessWindowClose=True

def changeBrightness(canvas, brightnessWindow, brightnessSlider,                      previousVal):
    if canvas.data.brightnessWindowClose==True:
        brightnessWindow.destroy()
        canvas.data.brightnessWindowClose=False
        
    else:
        # increasing pixel values according to slider value increases
        #brightness we change ot according to the difference between the
        # previous value and the current slider value
        if canvas.data.image!=None and brightnessWindow.winfo_exists():
            sliderVal=brightnessSlider.get()
            scale=(sliderVal-previousVal)/100.0
            canvas.data.image=canvas.data.image.point(                lambda i: i+ int(round(i*scale)))  
            canvas.data.imageForTk=makeImageForTk(canvas)
            drawImage(canvas)
            canvas.after(200,             lambda: changeBrightness(canvas, brightnessWindow,                                      brightnessSlider, sliderVal))

def brightness(canvas):
    canvas.data.colourPopToHappen=False
    canvas.data.cropPopToHappen=False
    canvas.data.drawOn=False
    brightnessWindow=Toplevel(canvas.data.mainWindow)
    brightnessWindow.title("Brightness")
    brightnessSlider=Scale(brightnessWindow, from_=-100, to=100,                           orient=HORIZONTAL)
    brightnessSlider.pack()
    OkBrightnessFrame=Frame(brightnessWindow)
    OkBrightnessButton=Button(OkBrightnessFrame, text="OK",                               command=lambda: closeBrightnessWindow(canvas))
    OkBrightnessButton.grid(row=0,column=0)
    OkBrightnessFrame.pack(side=BOTTOM)
    changeBrightness(canvas, brightnessWindow, brightnessSlider,0)
    #brightnessSlider.set(0)

def reset(canvas):
    canvas.data.colourPopToHappen=False
    canvas.data.cropPopToHappen=False
    canvas.data.drawOn=False
    ### change back to original image
    if canvas.data.image!=None:
        canvas.data.image=canvas.data.originalImage.copy()
        save(canvas)
        canvas.data.undoQueue.append(canvas.data.image.copy())
        canvas.data.imageForTk=makeImageForTk(canvas)
        drawImage(canvas)

def mirror(canvas):
    canvas.data.colourPopToHappen=False
    canvas.data.cropPopToHappen=False
    canvas.data.drawOn=False
    if canvas.data.image!=None:
        canvas.data.image=ImageOps.mirror(canvas.data.image)
        save(canvas)
        canvas.data.undoQueue.append(canvas.data.image.copy())
        canvas.data.imageForTk=makeImageForTk(canvas)
        drawImage(canvas)

def flip(canvas):
    canvas.data.colourPopToHappen=False
    canvas.data.cropPopToHappen=False
    canvas.data.drawOn=False
    if canvas.data.image!=None:
        canvas.data.image=ImageOps.flip(canvas.data.image)
        save(canvas)
        canvas.data.undoQueue.append(canvas.data.image.copy())
        canvas.data.imageForTk=makeImageForTk(canvas)
        drawImage(canvas)


def transpose(canvas):
    canvas.data.colourPopToHappen=False
    canvas.data.cropPopToHappen=False
    canvas.data.drawOn=False
    # I treated the image as a continuous list of pixel values row-wise
    # and simply excnaged the rows and the coloums
    # in oder to make it rotate clockewise, I reversed all the rows
    if canvas.data.image!=None:
        imageData=list(canvas.data.image.getdata())
        newData=[]
        newimg=Image.new(canvas.data.image.mode,                (canvas.data.image.size[1], canvas.data.image.size[0]))
        for i in range(canvas.data.image.size[0]):
            addrow=[]
            for j in range(i, len(imageData), canvas.data.image.size[0]):
                addrow.append(imageData[j])
            addrow.reverse()
            newData+=addrow 
        newimg.putdata(newData)
        canvas.data.image=newimg.copy()
        save(canvas)
        canvas.data.undoQueue.append(canvas.data.image.copy())
        canvas.data.imageForTk=makeImageForTk(canvas)
        drawImage(canvas)
    
############### FILTERS ######################
        

def invert(canvas):
    canvas.data.colourPopToHappen=False
    canvas.data.cropPopToHappen=False
    canvas.data.drawOn=False
    if canvas.data.image!=None:
        canvas.data.image=ImageOps.invert(canvas.data.image)
        save(canvas)
        canvas.data.undoQueue.append(canvas.data.image.copy())
        canvas.data.imageForTk=makeImageForTk(canvas)
        drawImage(canvas)

def posterize(canvas):
    canvas.data.colourPopToHappen=False
    canvas.data.cropPopToHappen=False
    canvas.data.drawOn=False
    # we basically reduce the range of colurs from 256 to 5 bits
    # and so, assign a single new value to each colour value
    # in each succesive range
    posterData=[]
    if canvas.data.image!=None:
        for col in range(canvas.data.imageSize[1]):
            for row in range(canvas.data.imageSize[0]):
                r, g, b= canvas.data.image.getpixel((row, col))
                if r in range(32):
                    R=0
                elif r in range(32, 96):
                    R=64
                elif r in range(96, 160):
                    R=128
                elif r in range(160, 224):
                    R=192
                elif r in range(224,256):
                    R=255
                if g in range(32):
                    G=0
                elif g in range(32, 96):
                    G=64
                elif g in range(96, 160):
                    G=128
                elif r in range(160, 224):
                    g=192
                elif r in range(224,256):
                    G=255
                if b in range(32):
                    B=0
                elif b in range(32, 96):
                    B=64
                elif b in range(96, 160):
                    B=128
                elif b in range(160, 224):
                    B=192
                elif b in range(224,256):
                    B=255
                posterData.append((R, G, B))
        canvas.data.image.putdata(posterData)
        save(canvas)
        canvas.data.undoQueue.append(canvas.data.image.copy())
        canvas.data.imageForTk=makeImageForTk(canvas)
        drawImage(canvas)



################ EDIT MENU FUNCTIONS ############################

def keyPressed(canvas, event):
    if event.keysym=="z":
        undo(canvas)
    elif event.keysym=="y":
        redo(canvas)
        

# we use deques so as to make Undo and Redo more efficient and avoid
# memory space isuues 
# after each change, we append the new version of the image to
# the Undo queue
def undo(canvas):
    if len(canvas.data.undoQueue)>0:
        # the last element of the Undo Deque is the
        # current version of the image
        lastImage=canvas.data.undoQueue.pop()
        # we would want the current version if wehit redo after undo
        canvas.data.redoQueue.appendleft(lastImage)
    if len(canvas.data.undoQueue)>0:
        # the previous version of the image
        canvas.data.image=canvas.data.undoQueue[-1]
    save(canvas)
    canvas.data.imageForTk=makeImageForTk(canvas)
    drawImage(canvas)

def redo(canvas):
    if len(canvas.data.redoQueue)>0:
        canvas.data.image=canvas.data.redoQueue[0]
    save(canvas)
    if len(canvas.data.redoQueue)>0:
        # we remove this version from the Redo Deque beacuase it
        # has become our current image
        lastImage=canvas.data.redoQueue.popleft()
        canvas.data.undoQueue.append(lastImage)
    canvas.data.imageForTk=makeImageForTk(canvas)
    drawImage(canvas)

############# MENU COMMANDS ################

def saveAs(canvas):
    # ask where the user wants to save the file
    if canvas.data.image!=None:
        filename=asksaveasfilename(defaultextension=".jpg")
        im=canvas.data.image
        im.save(filename)

def save(canvas):
    if canvas.data.image!=None:
        im=canvas.data.image
        im.save(canvas.data.imageLocation)
def undoChanges(canvas):
    if canvas.data.image!=None:
       # if len(undoStack)>=1:
            #canvas.data.image=undoStack.pop()
        #else : canvas.data.image=canvas.data.originalImage
        canvas.data.image=canvas.data.originalImage.copy()
        save(canvas)
        canvas.data.imageForTk=makeImageForTk(canvas)
        drawImage(canvas)
        
        

def newImage(canvas):
    imageName=filedialog.askopenfilename()
    filetype=""
    #make sure it's an image file
    try: filetype=imghdr.what(imageName)
    except:
        messagebox.showinfo(title="Image File",        message="Choose an Image File!" , parent=canvas.data.mainWindow)
    # restrict filetypes to .jpg, .bmp, etc.
    if filetype in ['jpeg', 'bmp', 'png', 'tiff']:
        canvas.data.imageLocation=imageName
        im= Image.open(imageName)
        canvas.data.image=im
        undoStack.append(im)
        canvas.data.originalImage=im.copy()
        canvas.data.undoQueue.append(im.copy())
        canvas.data.imageSize=im.size #Original Image dimensions
        canvas.data.imageForTk=makeImageForTk(canvas)
        drawImage(canvas)
    else:
        messagebox.showinfo(title="Image File",        message="Choose an Image File!" , parent=canvas.data.mainWindow)

######## CREATE A VERSION OF IMAGE TO BE DISPLAYED ON THE CANVAS #########

def makeImageForTk(canvas):
    im=canvas.data.image
    if canvas.data.image!=None:
        # Beacuse after cropping the now 'image' might have diffrent
        # dimensional ratios
        imageWidth=canvas.data.image.size[0] 
        imageHeight=canvas.data.image.size[1]
        #To make biggest version of the image fit inside the canvas
        if imageWidth>imageHeight:
            resizedImage=im.resize((canvas.data.width,                int(round(float(imageHeight)*canvas.data.width/imageWidth))))
            # store the scale so as to use it later
            canvas.data.imageScale=float(imageWidth)/canvas.data.width
        else:
            resizedImage=im.resize((int(round(float(imageWidth)*canvas.data.height/imageHeight)),                                    canvas.data.height))
            canvas.data.imageScale=float(imageHeight)/canvas.data.height
        # we may need to refer to ther resized image atttributes again
        canvas.data.resizedIm=resizedImage
        return ImageTk.PhotoImage(resizedImage)
 
def drawImage(canvas):
    if canvas.data.image!=None:
        # make the canvas center and the image center the same
        canvas.create_image(canvas.data.width/2.0-canvas.data.resizedIm.size[0]/2.0,
                        canvas.data.height/2.0-canvas.data.resizedIm.size[1]/2.0,
                            anchor=NW, image=canvas.data.imageForTk)
        canvas.data.imageTopX=int(round(canvas.data.width/2.0-canvas.data.resizedIm.size[0]/2.0))
        canvas.data.imageTopY=int(round(canvas.data.height/2.0-canvas.data.resizedIm.size[1]/2.0))


############# Enhancement Techniques ##############



def sharpen(canvas):
    canvas.data.cropPopToHappen=False
    canvas.data.colourPopToHappen=False
    canvas.data.drawOn=False
    
    src= np.asarray(canvas.data.image)
    
    kernel = np.array([[-1,-1,-1], 
                   [-1, 9,-1],
                   [-1,-1,-1]])
    sharpened = cv2.filter2D(src, -1, kernel)
   
    abs_dst = sharpened
    
    
    canvas.data.image=Image.fromarray(abs_dst)
    canvas.data.undoQueue.append(canvas.data.image.copy())
    canvas.data.imageForTk=makeImageForTk(canvas)
    drawImage(canvas)



def emtButtonsInit(root, canvas):
    backgroundColour="gray50"
    buttonWidth=14
    buttonHeight=2
    emttoolKitFrame=Frame(root)
    fourier=Button(emttoolKitFrame, text="fourier",                      background=backgroundColour ,                      width=buttonWidth, height=buttonHeight,                       command=lambda:fourierTransform(canvas))
    fourier.grid(row=0,column=0)
    sharpened=Button(emttoolKitFrame, text="sharpen image",                        background=backgroundColour,                         width=buttonWidth,height=buttonHeight,                         command=lambda: sharpen(canvas))
    sharpened.grid(row=1,column=0)
    smoothen=Button(emttoolKitFrame, text="smoothen",                            background=backgroundColour ,                            width=buttonWidth, height=buttonHeight,                            command=lambda: smoothenImg(canvas))
    smoothen.grid(row=0,column=1)
    negativeButton=Button(emttoolKitFrame, text="negative",                           background=backgroundColour ,                           width=buttonWidth,height=buttonHeight,                            command=lambda: invert(canvas))
    negativeButton.grid(row=1,column=1)
    contrastButton=Button(emttoolKitFrame, text="contrast",                           background=backgroundColour,                            width=buttonWidth,height=buttonHeight,                            command=lambda: contrast(canvas))
    contrastButton.grid(row=0,column=2)
    logButton=Button(emttoolKitFrame, text="log transform",                        background=backgroundColour,                         width=buttonWidth,height=buttonHeight,                         command=lambda: logTransform(canvas))
    logButton.grid(row=1,column=2)
    flipButton=Button(emttoolKitFrame, text="Flip",                      background=backgroundColour ,                      width=buttonWidth,height=buttonHeight,                       command=lambda: flip(canvas))
    flipButton.grid(row=0,column=3)
    transposeButton=Button(emttoolKitFrame, text="Transpose",                           background=backgroundColour, width=buttonWidth,                           height=buttonHeight,command=lambda: transpose(canvas))
    transposeButton.grid(row=1,column=3)
    binaryButton=Button(emttoolKitFrame, text="binary",                      background=backgroundColour ,width=buttonWidth,                      height=buttonHeight,command=lambda: binaryImage(canvas))
    binaryButton.grid(row=0,column=4)
    mirrorButton=Button(emttoolKitFrame, text="Sobel Edge detection",                        background=backgroundColour,                         width=buttonWidth,height=buttonHeight,                         command=lambda: sobel(canvas))
    mirrorButton.grid(row=1,column=4)
    
    resetButton=Button(emttoolKitFrame, text="Reset",                       background=backgroundColour ,width=buttonWidth,                       height=buttonHeight, command=lambda: reset(canvas))
    resetButton.grid(row=0,column=5)
    saveChanges=Button(emttoolKitFrame,text="saveChanges",                        background=backgroundColour, width=buttonWidth,                        height=buttonHeight,command=lambda: saveChanges(canvas))
    saveChanges.grid(row=1,column=5)
    #Please comment this button out if you use this on any OS apart from Windows
    
    emttoolKitFrame.pack(side=LEFT)
    
def changeContrast(canvas, brightnessWindow, brightnessSlider,                      previousVal):
    if canvas.data.brightnessWindowClose==True:
        brightnessWindow.destroy()
        canvas.data.brightnessWindowClose=False
        
    else:
        # increasing pixel values according to slider value increases
        #brightness we change ot according to the difference between the
        # previous value and the current slider value
        if canvas.data.image!=None and brightnessWindow.winfo_exists():
            sliderVal=brightnessSlider.get()
            scale=(sliderVal)/100.0
            temp=canvas.data.image
            canvas.data.image=temp.point(                lambda i: min(255,int(round(i*scale))))  
            canvas.data.imageForTk=makeImageForTk(canvas)
            drawImage(canvas)
            canvas.after(200,             lambda: changeContrast(canvas, brightnessWindow,                                      brightnessSlider, sliderVal))

    
def contrast(canvas):
    canvas.data.cropPopToHappen=False
    canvas.data.colourPopToHappen=False
    canvas.data.drawOn=False
    src = np.asarray(canvas.data.image.copy())
    
    brightnessWindow=Toplevel(canvas.data.mainWindow)
    brightnessWindow.title("Contrast")
    brightnessSlider=Scale(brightnessWindow, from_=25, to=200,                           orient=HORIZONTAL)
    brightnessSlider.pack()
    OkBrightnessFrame=Frame(brightnessWindow)
    OkBrightnessButton=Button(OkBrightnessFrame, text="OK",                               command=lambda: closeBrightnessWindow(canvas))
    OkBrightnessButton.grid(row=0,column=0)
    OkBrightnessFrame.pack(side=BOTTOM)
    changeContrast(canvas, brightnessWindow, brightnessSlider,100)
    brightnessSlider.set(100)

    '''im=np.zeros(shape=(len(src),len(src[0]),3))
    while canvas.data.image!=None and brightnessWindow.winfo_exists():
        sliderVal=brightnessSlider.get()
        scale=(sliderVal)/100.0
        
        for i in range(0,len(im)):
            for j in range(0,len(im[0])):
                im[i][j][0]=min(255,int(src[i][j][0]*scale))
                im[i][j][1]=min(255,int(src[i][j][1]*scale))
                im[i][j][2]=min(255,int(src[i][j][2]*scale))
        canvas.data.image=Image.fromarray(im)
        .canvas.data.imageForTk=makeImageForTk(canvas)
        drawImage(canvas)
        time.sleep(0.1)
        

    brightnessSlider.set(0)'''
   
    
    
def binaryImage(canvas):
    canvas.data.cropPopToHappen=False
    canvas.data.colourPopToHappen=False
    canvas.data.drawOn=False
    src = np.asarray(canvas.data.image)
    im_gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)

    ret,thresh_img = cv2.threshold(im_gray,127,255,cv2.THRESH_BINARY)
    thresh = 127
    
    canvas.data.image=Image.fromarray(thresh_img)
    canvas.data.undoQueue.append(canvas.data.image.copy())
    canvas.data.imageForTk=makeImageForTk(canvas)
    drawImage(canvas)

def closeEmtWindow(canvas):
    if canvas.data.image!=None:
        save(canvas)
        canvas.data.undoQueue.append(canvas.data.image.copy())
        canvas.data.emtWindowClose=True

def Enhancements(canvas):
    
    canvas.data.colourPopToHappen=False
    canvas.data.cropPopToHappen=False
    canvas.data.drawOn=False
    emtWindow=Toplevel(canvas.data.mainWindow)
    emtWindow.title("Enhancement")
    Width=100
    Height=50
    canvas.data.emtCanvasWidth=50
    canvas.data.emtCanvasHeight=300
    emtCanvas = Canvas(emtWindow, width=Width,                         height=Height)
    
    emtCanvas.pack()
    emtButtonsInit(emtWindow,canvas)
    #emtCanvas.data.image=canvas.data.image.copy()
    canvas.data.imageForTk=makeImageForTk(canvas)
    drawImage(canvas)
    

def fourierTransform(canvas):
    
    canvas.data.cropPopToHappen=False
    canvas.data.colourPopToHappen=False
    canvas.data.drawOn=False
    img = np.asarray(canvas.data.image)
    
    img= cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    f = np.fft.fft2(img)
    fshift = np.fft.fftshift(f)
    magnitude_spectrum = 20*np.log(np.abs(fshift))
    magnitude_spectrum = np.asarray(magnitude_spectrum, dtype=np.uint8)
    iam = np.concatenate((img, magnitude_spectrum), axis=1)
    e=Image.fromarray(iam.astype(np.uint8))
    
    canvas.data.image=e
    canvas.data.undoQueue.append(canvas.data.image.copy())
    canvas.data.imageForTk=makeImageForTk(canvas)
    drawImage(canvas)


def logTransform(canvas):
    canvas.data.cropPopToHappen=False
    canvas.data.colourPopToHappen=False
    canvas.data.drawOn=False
    src = np.asarray(canvas.data.image)
    im_gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    thresh_img=(np.log(im_gray+1)/(np.log(1+np.max(im_gray))))*255
    thresh_img=np.array(thresh_img,dtype=np.uint8)
    canvas.data.image=Image.fromarray(thresh_img)
    canvas.data.undoQueue.append(canvas.data.image.copy())
    canvas.data.imageForTk=makeImageForTk(canvas)
    drawImage(canvas)




def negative(canvas):
    
    canvas.data.cropPopToHappen=False
    canvas.data.colourPopToHappen=False
    canvas.data.drawOn=False
    src = np.asarray(canvas.data.image)
    im_gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)

    ret,thresh_img = cv2.threshold(im_gray,127,255,cv2.THRESH_BINARY)
    thresh = 127
    
    canvas.data.image=Image.fromarray(thresh_img)
    canvas.data.undoQueue.append(canvas.data.image.copy())
    canvas.data.imageForTk=makeImageForTk(canvas)
    drawImage(canvas)






############ INITIALIZE ##############

def init(root, canvas):

    buttonsInit(root, canvas)
    menuInit(root, canvas)
    canvas.data.image=None
    canvas.data.angleSelected=None
    canvas.data.rotateWindowClose=False
    canvas.data.brightnessWindowClose=False
    canvas.data.brightnessLevel=None
    canvas.data.histWindowClose=False
    canvas.data.emtWindowClose=False
    #canvas.data.emtWindow=False
    canvas.data.solarizeWindowClose=False
    canvas.data.posterizeWindowClose=False
    canvas.data.colourPopToHappen=False
    canvas.data.cropPopToHappen=False
    canvas.data.endCrop=False
    canvas.data.drawOn=True
    
    canvas.data.undoQueue=deque([], 10)
    canvas.data.redoQueue=deque([], 10)
    canvas.pack()

def buttonsInit(root, canvas):
    backgroundColour="gray50"
    buttonWidth=14
    buttonHeight=2
    toolKitFrame=Frame(root)
    cropButton=Button(toolKitFrame, text="Crop",                      background=backgroundColour ,                      width=buttonWidth, height=buttonHeight,                       command=lambda:crop(canvas))
    cropButton.grid(row=2,column=0)
    rotateButton=Button(toolKitFrame, text="Rotate",                        background=backgroundColour,                         width=buttonWidth,height=buttonHeight,                         command=lambda: rotate(canvas))
    rotateButton.grid(row=3,column=0)
    brightnessButton=Button(toolKitFrame, text="Brightness",                            background=backgroundColour ,                            width=buttonWidth, height=buttonHeight,                            command=lambda: brightness(canvas))
    brightnessButton.grid(row=4,column=0)
    histogramButton=Button(toolKitFrame, text="Histogram",                           background=backgroundColour ,                           width=buttonWidth,height=buttonHeight,                            command=lambda: histogram(canvas))
    histogramButton.grid(row=5,column=0)
    mirrorButton=Button(toolKitFrame, text="Mirror",                        background=backgroundColour,                         width=buttonWidth,height=buttonHeight,                         command=lambda: mirror(canvas))
    mirrorButton.grid(row=6,column=0)
    flipButton=Button(toolKitFrame, text="Flip",                      background=backgroundColour ,                      width=buttonWidth,height=buttonHeight,                       command=lambda: flip(canvas))
    flipButton.grid(row=7,column=0)
    transposeButton=Button(toolKitFrame, text="Transpose",                           background=backgroundColour, width=buttonWidth,                           height=buttonHeight,command=lambda: transpose(canvas))
    transposeButton.grid(row=8,column=0)
   
    resetButton=Button(toolKitFrame, text="Reset",                       background=backgroundColour ,width=buttonWidth,                       height=buttonHeight, command=lambda: reset(canvas))
    resetButton.grid(row=9,column=0)
    #Please comment this button out if you use this on any OS apart from Windows
    
    enhancementButton=Button(toolKitFrame, text="Enhancements",                          background=backgroundColour,height=2*buttonHeight,                          width=buttonWidth,command=lambda: Enhancements(canvas))
    enhancementButton.grid(row=0,column=0)
    restButton=Button(toolKitFrame, text="Restoration",                          background=backgroundColour,height=2*buttonHeight,                          width=buttonWidth,command=lambda: Restoration(canvas))
    restButton.grid(row=1,column=0)
    toolKitFrame.pack(side=LEFT)
    
def menuInit(root, canvas):
    menubar=Menu(root)
    menubar.add_command(label="New", command=lambda:newImage(canvas))
    menubar.add_command(label="Save", command=lambda:save(canvas))
    menubar.add_command(label="Save As", command=lambda:saveAs(canvas))
    menubar.add_command(label="Undo",command=lambda:undoChanges(canvas))
    ## Edit pull-down Menu
    editmenu = Menu(menubar, tearoff=0)
    editmenu.add_command(label="Undo   Z", command=lambda:undo(canvas))
    editmenu.add_command(label="Redo   Y", command=lambda:redo(canvas))
    menubar.add_cascade(label="Edit", menu=editmenu)
    root.config(menu=menubar)
    ## Filter pull-down Menu
    filtermenu = Menu(menubar, tearoff=0)
    filtermenu.add_command(label="black and White",                            command=lambda:covertGray(canvas))
    filtermenu.add_command(label="Invert",                            command=lambda:invert(canvas))
    filtermenu.add_command(label="Posterize",                            command=lambda:posterize(canvas))
    menubar.add_cascade(label="Filter", menu=filtermenu)
    root.config(menu=menubar)
    


# In[20]:


def gaussianImg(canvas):
    canvas.data.cropPopToHappen=False
    canvas.data.colourPopToHappen=False
    canvas.data.drawOn=False
    src = np.asarray(canvas.data.image)
    image=src
    row,col,ch= image.shape
    mean = abs(image.mean()-50)
    var = 5
    sigma = var**0.5
    gauss = np.random.normal(mean,sigma,(row,col,ch))
    gauss = gauss.reshape(row,col,ch)
    noisy = image + gauss
    
    canvas.data.image=Image.fromarray(noisy.astype(np.uint8))
    canvas.data.undoQueue.append(canvas.data.image.copy())
    canvas.data.imageForTk=makeImageForTk(canvas)
    drawImage(canvas)
    
def sap(canvas):
    canvas.data.cropPopToHappen=False
    canvas.data.colourPopToHappen=False
    canvas.data.drawOn=False
    src = np.asarray(canvas.data.image)
    image=src
    prob=0.05
    output = np.zeros(image.shape,np.uint8)
    thres = 1 - prob 
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            rdn = np.random.random()
            if rdn < prob:
                output[i][j] = 0
            elif rdn > thres:
                output[i][j] = 255
            else:
                output[i][j] = image[i][j]
    canvas.data.image=Image.fromarray(output)
    canvas.data.undoQueue.append(canvas.data.image.copy())
    canvas.data.imageForTk=makeImageForTk(canvas)
    drawImage(canvas)
    
    
def rayleighImg(canvas):
    canvas.data.cropPopToHappen=False
    canvas.data.colourPopToHappen=False
    canvas.data.drawOn=False
    src = np.asarray(canvas.data.image)
    image=src
    meanvalue = image.mean()
    modevalue = np.sqrt(2 / np.pi) * meanvalue
    s = np.random.rayleigh(modevalue, image.shape)
    thresh_img=src+s
    canvas.data.image=Image.fromarray(thresh_img.astype(np.uint8))
    canvas.data.undoQueue.append(canvas.data.image.copy())
    canvas.data.imageForTk=makeImageForTk(canvas)
    drawImage(canvas)

    
    
def uniImg(canvas):
    canvas.data.cropPopToHappen=False
    canvas.data.colourPopToHappen=False
    canvas.data.drawOn=False
    src = np.asarray(canvas.data.image)
    image =src
    row,col,ch = image.shape
    gauss = np.random.randn(row,col,ch)
    gauss = gauss.reshape(row,col,ch)        
    noisy = image + image * gauss
    
    canvas.data.image=Image.fromarray(noisy.astype(np.uint8))
    canvas.data.undoQueue.append(canvas.data.image.copy())
    canvas.data.imageForTk=makeImageForTk(canvas)
    drawImage(canvas)    
    
    
    
def closeresttWindow(canvas):
    if canvas.data.image!=None:
        save(canvas)
        canvas.data.undoQueue.append(canvas.data.image.copy())
        canvas.data.emtWindowClose=True

def Restoration(canvas):
    
    canvas.data.colourPopToHappen=False
    canvas.data.cropPopToHappen=False
    canvas.data.drawOn=False
    emtWindow=Toplevel(canvas.data.mainWindow)
    emtWindow.title("Restoration")
    Width=100
    Height=50
    canvas.data.emtCanvasWidth=20
    canvas.data.emtCanvasHeight=50
    emtCanvas = Canvas(emtWindow, width=Width,                         height=Height)
    
    emtCanvas.pack()
    restButtonsInit(emtWindow,canvas)
    #emtCanvas.data.image=canvas.data.image.copy()
    canvas.data.imageForTk=makeImageForTk(canvas)
    drawImage(canvas)
    
    

def restButtonsInit(root, canvas):
    backgroundColour="gray50"
    buttonWidth=14
    buttonHeight=2
    emttoolKitFrame=Frame(root)
    gaussian=Button(emttoolKitFrame, text="gaussian",                      background=backgroundColour ,                      width=buttonWidth, height=buttonHeight,                       command=lambda:gaussianImg(canvas))
    gaussian.grid(row=0,column=0)
    sp=Button(emttoolKitFrame, text="s&p",                        background=backgroundColour,                         width=buttonWidth,height=buttonHeight,                         command=lambda: sap(canvas))
    sp.grid(row=1,column=0)
    uni=Button(emttoolKitFrame, text="uniform noise",                            background=backgroundColour ,                            width=buttonWidth, height=buttonHeight,                            command=lambda: uniImg(canvas))
    uni.grid(row=0,column=1)
    rayleigh=Button(emttoolKitFrame, text="rayleigh",                           background=backgroundColour ,                           width=buttonWidth,height=buttonHeight,                            command=lambda: rayleighImg(canvas))
    rayleigh.grid(row=1,column=1)
  
    resetButton=Button(emttoolKitFrame, text="Reset",                       background=backgroundColour ,width=buttonWidth,                       height=buttonHeight, command=lambda: reset(canvas))
    resetButton.grid(row=0,column=2)
    saveChanges=Button(emttoolKitFrame,text="saveChanges",                        background=backgroundColour, width=buttonWidth,                        height=buttonHeight,command=lambda: saveChanges(canvas))
    saveChanges.grid(row=1,column=2)
    #Please comment this button out if you use this on any OS apart from Windows
    
    emttoolKitFrame.pack(side=LEFT)
    


# In[21]:


def run():
    # create the root and the canvas
    root = Tk()
    root.title("Image Editor")
    canvasWidth=800
    canvasHeight=500
    canvas = Canvas(root, width=canvasWidth, height=canvasHeight,                     background="black")
    # Set up canvas data and call init
    class Struct: pass
    canvas.data = Struct()
    canvas.data.width=canvasWidth
    canvas.data.height=canvasHeight
    canvas.data.mainWindow=root
    init(root, canvas)
    root.bind("<Key>", lambda event:keyPressed(canvas, event))
    # and launch the app
    root.mainloop()  # This call BLOCKS (so your program waits)


# In[22]:


def main():
    run()


# In[23]:


main()


# In[ ]:





# In[ ]:





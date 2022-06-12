import cv2
from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk, ImageColor
import tkmacosx as tkm
import numpy as np
from tkmacosx import ColorVar


window = Tk()
window.title("Kimera")
window.geometry("600x600")
# def resize(owo):
#     print("Resize")
#     global capture
#     # Change the height of capture to 5/6 of the window height
#     capture.configure(height=window.winfo_height())
    
# window.bind('<Configure>', resize)
filter = cv2.COLOR_BGR2RGB
flipBool = False
global tintColor
tintColor = False
CheckVar1 = IntVar()

#background image
img = PhotoImage(file="C:/Users/nnn10/Downloads/CameraBG.png")
bg = Label(window,image=img)
bg.place(x=-4, y=-4)

# set height of video capture
camera = cv2.VideoCapture(0)
capture = Label(window, height=525, width=475)
capture.place(relx=0.4, rely=0.55, anchor=CENTER)

def flipImage():
    global flipBool
    if flipBool == False:
        flipBool = True
        return 
    if flipBool == True:
        flipBool = False
        return

def savingprereq():
    savingprereq.photoct = 0

def saveImage(top, photoFrame, livevid, tkimage):
    cv2.imwrite("Polaroid" + str(savingprereq.photoct) + ".png", livevid) 
    savingprereq.photoct +=1
    photoFrame.imgtk=tkimage
    photoFrame.configure(image=tkimage)
    print("Saved")

def captureImage():
    global window
    top = Toplevel(window)
    top.geometry("525x620")
    top.title("Photo")
    top.configure(background='#f0eded')
    
    photoFrame = Label(top, height=525, width=475)
    photoFrame.place(relx=0.5, rely=0.46, anchor=CENTER)
    
    image=camera.read()[1]
    livevid = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    global filter
    if filter != cv2.COLOR_BGR2RGB and not tintColor:
        livevid = cv2.cvtColor(livevid, filter)
    global flipBool
    if flipBool:
        livevid = cv2.flip(livevid, 1)
    if tintColor != False and CheckVar1.get() == 1:
        livevid = cv2.addWeighted(livevid, 0.8, (np.full(livevid.shape, tintColor, np.uint8)), 0.2, 0)
    i = Image.fromarray(livevid)
    tkimage = ImageTk.PhotoImage(image=i)
    photoFrame.imgtk=tkimage
    photoFrame.configure(image=tkimage)
    # turn tkimage to list
    
    livevid = cv2.cvtColor(livevid, filter)
    if flipBool:
        livevid = cv2.flip(livevid, 1)
    if tintColor != False and CheckVar1.get() == 1:
        livevid = cv2.addWeighted(livevid, 0.8, (np.full(livevid.shape, tintColor, np.uint8)), 0.2, 0)
    
    save = tkm.Button(top, text = "Save Photo", command = lambda:saveImage(top, photoFrame, livevid, tkimage), borderless=True)
    save.place(relx=0.85, rely=0.95, anchor=CENTER)
    
# Default Camera
def video():
    livevid = cv2.cvtColor(camera.read()[1], filter)
    global flipBool
    if flipBool:
        livevid = cv2.flip(livevid, 1)
    global tintColor
    if tintColor != False and CheckVar1.get() == 1:
        livevid = cv2.addWeighted(livevid, 0.8, (np.full(livevid.shape, tintColor, np.uint8)), 0.2, 0)
    i = Image.fromarray(livevid)
    tkimage = ImageTk.PhotoImage(image=i)

    capture.imgtk=tkimage
    capture.configure(image=tkimage)
    capture.after(15, video)

def resetFilter():
    global filter
    if CheckVar1.get() == 1:
        coloron.toggle()
    filter = cv2.COLOR_BGR2RGB

def grayscale():
    global filter
    if CheckVar1.get() == 1:
        coloron.toggle()
    filter = cv2.COLOR_BGR2GRAY

#stuff
savingprereq()

#click photo button
Click = Image.open("C:/Users/nnn10/Downloads/Shutter.png")
ClickResize = Click.resize((70,70), resample=5)
ClickPIMG = ImageTk.PhotoImage(ClickResize)
snapshot = tkm.CircleButton(window, radius=30, image=ClickPIMG, command = captureImage, borderless=True)

#coloring the image
coloron = tk.Checkbutton(window, text = "Tint", onvalue = 1, offvalue = 0, variable = CheckVar1)
slidervalue = ColorVar(value='#ffffff')
def selectColorTint(owo):
    global tintColor
    tintColor = ImageColor.getrgb(slidervalue.get())
colorify = tkm.Colorscale(window, value='hex', variable=slidervalue, mousewheel=1, command=selectColorTint)

reset = tkm.Button(window, borderless=True, text = "Reset", command = resetFilter)
grayify = tkm.Button(window, text = "Grayscale", command = grayscale, borderless=True)
flip = tkm.Button(window, text = "Mirror Image", command = flipImage, borderless=True)

snapshot.place(relx=0.9, rely=0.35, anchor=CENTER)
reset.place(relx=0.9, rely=0.55, anchor=CENTER)
grayify.place(relx=0.9, rely=0.75, anchor=CENTER)
flip.place(relx=0.9, rely=0.95, anchor=CENTER)
colorify.place(relx=0.595, rely=0.0725, anchor=CENTER)
coloron.place(relx=0.3, rely=0.0675, anchor=CENTER)

video()
# grayscale()
window.resizable(False, False)
window.mainloop()

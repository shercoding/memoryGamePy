from tkinter import *
import cv2
import numpy as np
from PIL import Image, ImageTk
import math
import pygame
import random
import os

lastclicked = False
lastclicked_item = 20
counter = 0
pygame.mixer.init()

current_directory = os.getcwd()
sound_folder_path = os.path.join(current_directory, "sounds")
img_folder_path = os.path.join(current_directory, "pics")
mp3_file_path = os.path.join(sound_folder_path, "sound.mp3")

pic1_path = os.path.join(img_folder_path, "1.jpg")
pic2_path = os.path.join(img_folder_path, "2.jpg")
pic3_path = os.path.join(img_folder_path, "3.jpg")
pic4_path = os.path.join(img_folder_path, "4.jpg")
pic5_path = os.path.join(img_folder_path, "5.jpg")
pic6_path = os.path.join(img_folder_path, "6.jpg")
pic7_path = os.path.join(img_folder_path, "7.jpg")
pic8_path = os.path.join(img_folder_path, "8.jpg")

print(pic1_path)

sound_file = mp3_file_path
sound = pygame.mixer.Sound(sound_file)

window = Tk()
window.geometry("470x600")
window.title('Memory Game')
window.resizable(False, False)

# read image


def load_and_resize_image(path):
    image = cv2.imread(path)
    if image is not None:
        image = cv2.resize(image, (100, 100), interpolation=cv2.INTER_LINEAR)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image


# List of paths to images
image_paths = [
    pic1_path,
    pic2_path,
    pic3_path,
    pic4_path,
    pic5_path,
    pic6_path,
    pic7_path,
    pic8_path
]

imageIndexes = [0, 0, 0, 0, 0, 0, 0, 0]
# Load and resize images
images = [load_and_resize_image(path) for path in image_paths]

proj2dto3d = np.array([[1, 0, -50],
                       [0, 1, -50],
                       [0, 0, 0],
                       [0, 0, 1]], np.float32)

ry = np.array([[1, 0, 0, 0],
               [0, 1, 0, 0],
               [0, 0, 1, 0],
               [0, 0, 0, 1]], np.float32)

trans = np.array([[1, 0, 0, 0],
                  [0, 1, 0, 0],
                  [0, 0, 1, 500],  # 400 to move the image in z axis
                  [0, 0, 0, 1]], np.float32)

proj3dto2d = np.array([[500, 0, 50, 0],
                       [0, 500, 50, 0],
                       [0, 0, 1, 0]], np.float32)

# Function to rotate the image


def rotate_image(num, counter, clockwise, image, label, i):
    global images
    global ay
    ay_sign = 1 if clockwise else -1

    if clockwise:
        if counter < num:
            ay = float(counter * (math.pi / 180.0))
            counter += 5  # increase angle by 3 degrees
    else:
        if counter > num:
            ay = float(counter * (math.pi / -180.0))
            counter -= 5  # increase angle by 3 degrees

    ry[0, 0] = math.cos(ay * ay_sign)
    ry[0, 2] = -math.sin(ay * ay_sign)
    ry[2, 0] = math.sin(ay * ay_sign)
    ry[2, 2] = math.cos(ay * ay_sign)

    r = ry
    final = proj3dto2d.dot(trans.dot(r.dot(proj2dto3d)))

    dst = cv2.warpPerspective(
        image,
        final,
        (100, 100),
        None,
        cv2.INTER_LINEAR,
        cv2.BORDER_CONSTANT,
        (18, 52, 86))

    img = cv2.cvtColor(dst, 1)
    imgPIL = Image.fromarray(img)
    imgTk = ImageTk.PhotoImage(image=imgPIL)

    label.configure(image=imgTk)
    label.image = imgTk

    if (counter == 95 or counter == -4):
        return

    if clockwise:
        window.after(2, lambda: rotate_image(
            num, counter, clockwise, image, label, i))
    else:
        window.after(2, lambda: rotate_image(
            num, counter, clockwise, image, label, i))


# Function to handle button click event
firstRotatation = True
firstRotatationChanged = [None] * 16

for i in range(16):
    firstRotatationChanged[i] = True


def on_label_click(event, i, imageIndex, image, label):

    global firstRotatationChanged
    global counter
    global lastclicked_item
    global lastImageIndex
    global dont
    dont = True

    if counter == 0:
        lastclicked_item = i
        lastImageIndex = imageIndex
        counter += 1
    else:
        if imageIndex != lastImageIndex:
            rotate_image(
                91, 0, True,
                images[lastImageIndex],
                labels[lastclicked_item],
                lastclicked_item)
            firstRotatationChanged[lastclicked_item] = False

            rotate_image(
                91, 0, True,
                image,
                label,
                i)
            dont = False

            firstRotatationChanged[i] = False
        lastclicked_item = 20
        counter = 0

    if (dont):
        if (firstRotatationChanged[i]):
            rotate_image(91, 0, True, image, labels[i], i)
            firstRotatationChanged[i] = False
        else:
            rotate_image(0, 91, False, image, labels[i], i)
            firstRotatationChanged[i] = True
        sound.play()


frames = []
imgPILs = []
imgTks = []
labels = []

label1 = Label()
label2 = Label()
label3 = Label()
label4 = Label()
label5 = Label()
label6 = Label()
label7 = Label()
label8 = Label()
label9 = Label()
label10 = Label()
label11 = Label()
label12 = Label()
label13 = Label()
label14 = Label()
label15 = Label()
label16 = Label()

labels.append(label1)
labels.append(label2)
labels.append(label3)
labels.append(label4)
labels.append(label5)
labels.append(label6)
labels.append(label7)
labels.append(label8)
labels.append(label9)
labels.append(label10)
labels.append(label11)
labels.append(label12)
labels.append(label13)
labels.append(label14)
labels.append(label15)
labels.append(label16)

for i in range(8):
    imgPIL = Image.fromarray(images[i])
    imgTk = ImageTk.PhotoImage(image=imgPIL)
    imgTks.append(imgTk)

# Create 8 frames and add them to the list
for i in range(16):
    global windowsX, windowsY
    windowsX = 0.01
    windowsY = 0.01
    match i:
        case 0:
            windowsX = 0.01
            windowsY = 0.01
        case 1:
            windowsX = 0.26
            windowsY = 0.01
        case 2:
            windowsX = 0.51
            windowsY = 0.01
        case 3:
            windowsX = 0.76
            windowsY = 0.01
        case 4:
            windowsX = 0.01
            windowsY = 0.20
        case 5:
            windowsX = 0.26
            windowsY = 0.20
        case 6:
            windowsX = 0.51
            windowsY = 0.20
        case 7:
            windowsX = 0.76
            windowsY = 0.20
        case 8:
            windowsX = 0.01
            windowsY = 0.39
        case 9:
            windowsX = 0.26
            windowsY = 0.39
        case 10:
            windowsX = 0.51
            windowsY = 0.39
        case 11:
            windowsX = 0.76
            windowsY = 0.39
        case 12:
            windowsX = 0.01
            windowsY = 0.58
        case 13:
            windowsX = 0.26
            windowsY = 0.58
        case 14:
            windowsX = 0.51
            windowsY = 0.58
        case 15:
            windowsX = 0.76
            windowsY = 0.58

    frame = Frame(window, width=100, height=100,
                  highlightbackground='#123456', highlightthickness=3)
    frame.pack()
    frame.place(relx=windowsX, rely=windowsY) 
    frames.append(frame)

for i in range(16):
    imageIndex = random.randint(0, 7)

    while (imageIndexes[imageIndex] == 2):
        imageIndex = random.randint(0, 7)

    imageIndexes[imageIndex] += 1

    print(i, imageIndex)

    labels[i] = Label(frames[i], image=imgTks[imageIndex],
                      bg="#123456", anchor='center')
    labels[i].pack()
    labels[i].config(cursor="hand2", )
    labels[i].bind("<Button-1>", lambda event, i=i, imageIndex=imageIndex, image=images[imageIndex],
                   label=labels[i]: on_label_click(event, i, imageIndex, image, label))
    rotate_image(91, 0, True, images[imageIndex], labels[i], i)
    firstRotatationChanged[i] = False

window.mainloop()

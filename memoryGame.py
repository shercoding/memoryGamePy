# from pygame import *
import tkinter as tkr
import PIL as p
import PIL.ImageTk as ptk
from PIL import ImageTk, Image, ImageDraw
from tkinter.ttk import *

window = tkr.Tk()
window.geometry("500x500")
window.title('Memory Game')


def on_label_click(event):
    print('on_label_click')


frame = tkr.Frame(window, width=100, height=100,
                  highlightbackground='red', highlightthickness=3)
frame.pack()
frame.place(relx=0.01, rely=0.01)

# Create an object of tkinter ImageTk
orginal_img = Image.open(
    "D:/Schule/Naechtes_Halbjahr/Python/MemoryGame/pics/1.png").resize((100, 100))

img = ImageTk.PhotoImage(orginal_img)
 
# Create a Label Widget to display the text or Image
label = tkr.Label(frame, image=img, bg="green", anchor='center')
label.pack()
 
label.bind("<Button-1>", on_label_click)

window.mainloop()

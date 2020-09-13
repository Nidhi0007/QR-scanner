import numpy as np
import cv2
import tkinter as tk
from PIL import Image, ImageTk
import numpy as np
import pyzbar.pyzbar as pyzbar
import datetime
import pymysql
import sys



window = tk.Tk()  #Makes main window
window.wm_title("QR SCANNER")
window.config(background="#FFFFFF")
window.geometry("700x650")
window.maxsize(700,650)


imageFrame = tk.Frame(window, width=600, height=500)
imageFrame.place(x=30,y=80)


imageLabel = tk.Label(imageFrame)
imageLabel.grid(row=0, column=0)

cap = None
font = cv2.FONT_HERSHEY_PLAIN
def toggle():
    global cap

    cap = cv2.VideoCapture(0)
    
    if but3.config('text')[-1]=='START':
        but3.config(text='STOP')
        print("start is pressed")
        imageLabel.pack()
        show_frame()
    else:
        but3.config(text='START')
        cap.release()
        resultLabel.config(text="Result")
        dateLabel.configure(text="Inserted on")
        imageLabel.pack_forget()
        print("stop is pressed")

    
    
    
def show_frame():

    _, frame = cap.read()
    
    decodedObjects = pyzbar.decode(frame)
    print(decodedObjects)
    
    for obj in decodedObjects:
        # print("Data", obj.data)
        cv2.putText(frame, str(obj.data), (50, 50), font, 2,
                    (255, 0, 0), 3)
        date = datetime.datetime.now()
        resultLabel.config(text=obj.data)
        
        dateLabel.configure(text=date)
        db = pymysql.connect("localhost","root","","qrscanner" )
        cursor = db.cursor()
        # Create a new record
        sql = "INSERT IGNORE INTO `qrscannertb` (`datetime`, `link`) VALUES (%s, %s)"

        # Execute the query
        cursor.execute(sql, (date,obj.data))
        cap.release()
        # the connection is not autocommited by default. So we must commit to save our changes.
        db.commit()
        version = cursor.fetchone()
        print("DATABASE VERSION : %s" % version)
        
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    imageLabel.imgtk = imgtk
    imageLabel.configure(image=imgtk)
    imageLabel.after(10, show_frame)
    








sliderFrame = tk.Frame(window, width=643, height=150)
sliderFrame.place(x=30,y=10)
but3 = tk.Button(window,text="START", width=50,font=("Ariel Bold",15),bg='blue',fg='white', command=toggle)
but3.place(x=70,y=30)
resultLabel = tk.Label(window, text="Result", width=50,font=("Ariel Bold",15),bg='blue',fg='white')
resultLabel.place(x=70,y=80)
dateLabel = tk.Label(window, text="Inserted On", width=50,font=("Ariel Bold",15),bg='blue',fg='white')
dateLabel.place(x=70,y=110)


window.mainloop()
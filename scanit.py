import cv2
from tkinter import *
import tkinter as tk
from PIL import ImageTk
import PIL
from PIL import ImageDraw,ImageFont
import numpy as np
from PIL import Image
from urllib.request import urlopen
from pathlib import Path
from skimage.filters import threshold_local
import glob,os
import time,datetime



#mainFrame
window_pop = Tk()
window_pop.configure(background='white')
window_pop.title("Scan IT!")
width = window_pop.winfo_screenwidth()
height = window_pop.winfo_screenheight()
window_pop.geometry(f'{width}x{height}')
# Size for displaying Image
w = 385;h = 535
size = (w, h)

# window_pop.iconbitmap('./use_image/Scanit!.ico')
window_pop.resizable(0, 0)
run = False

#url checking
label_heading = tk.Label(window_pop, text="Enter your IP Camera url", width=30, height=1, fg="black", bg="white",font=('times', 18, ' bold '))
label_heading.place(x=29, y=5)

txt = tk.Entry(window_pop, borderwidth=4, width=45, bg="white", fg="black", font=('times', 16, ' bold '))
txt.place(x=29, y=35)
txt.insert(0,'http://192.168.0.100:8080/shot.jpg')


#mainRun
def Run_thesetup():
    global capture_button, crop_capture, crop_images, pdf_get, pdf_button_func, scanned_imgs
    url = txt.get()
    crop_capture = 0

    pdf_get = 0
    scanned_imgs = []

    capture_button = tk.Button(window_pop, text='Capture', bg="#8ab6d6", fg="black", width=24,
                               height=1, font=('times', 22), command=crop_image, activebackground='#114e60')
    capture_button.place(x=500, y=620)

    pdf_img = PIL.Image.open('./use_image/download.png')
    pdf_img = pdf_img.resize((200, 90), PIL.Image.ANTIALIAS)
    sp_img1 = ImageTk.PhotoImage(pdf_img)

    pdf_button_func = Button(window_pop, borderwidth=0, command=pdf_gen, image=sp_img1, bg='white')
    pdf_button_func.pack()
    pdf_button_func.image = sp_img1
    pdf_button_func.place(x=600, y=690)
    try:
        if url == '':
            notice = tk.Label(window_pop, text='Check the URL!!', width=20, height=1, fg="white", bg="firebrick1",
                            font=('times', 13, ' bold '))
            notice.place(x=24, y=68)
            window_pop.after(2000, destroy_widget, notice)
        else:
            global display, imageFrame, cp1, img
            imageFrame = tk.Frame(window_pop)
            imageFrame.place(x=500, y=80)

            display = tk.Label(imageFrame)
            display.grid()

            cp1 = tk.Button(window_pop, text='Turn off', bg="spring green", fg="black", width=12,height=1, font=('times', 14), command=destroy_cam,
                           activebackground='yellow')
            cp1.place(x=430, y=33)

            def show_frame():
                global img
                img_resp = urlopen(url)
                img_arr = np.array(bytearray(img_resp.read()), dtype=np.uint8)
                frame = cv2.imdecode(img_arr, -1)
                frame = cv2.rotate(frame, cv2.cv2.ROTATE_90_CLOCKWISE)
                cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
                rgb = cv2.cvtColor(cv2image, cv2.COLOR_RGBA2RGB)
                img = PIL.Image.fromarray(rgb)
                img1 = img.resize(size, PIL.Image.ANTIALIAS)
                imgtk = ImageTk.PhotoImage(image=img1)
                display.imgtk = imgtk
                display.configure(image=imgtk)
                display.after(10, show_frame)
            show_frame()
    except Exception as e:
        print(e)
        #IP Error
        notice1 = tk.Label(window_pop, text='ERROR IP Not found', width=20, height=1, fg="white", bg="firebrick1",
                        font=('times', 13, ' bold '))
        notice1.place(x=24, y=68)
        window_pop.after(2000, destroy_widget, notice1)
        imageFrame.destroy()
        display.destroy()
        cp1.destroy()
        capture_button.destroy()

def destroy_widget(widget):
    widget.destroy()

def destroy_cam():
    imageFrame.destroy()
    display.destroy()
    cp1.destroy()
    capture_button.destroy()


def crop_image():
    global cropping, crop_capture, run, scanned_imgs
    run = True
    repn = Path('Cropped_image')
    if repn.is_dir():
        pass
    else:
        os.mkdir('Cropped_image')
    crop_capture += 1

    img1 = img.copy()
    img1 = cv2.cvtColor(np.asarray(img1), cv2.COLOR_RGB2BGR)
    cn = './Cropped_image/img_' + str(crop_capture) + '.jpg'
    cv2.imwrite(cn, img1)

    imlab2 = tk.Label(window_pop, text="Orignal: "+ cn[16:], width=22, height=1, fg="white", bg="black",font=('times', 15, ' bold '))
    imlab2.place(x=900, y=140)

    imageFrame2 = tk.Frame(window_pop)
    imageFrame2.place(x=900, y=170)

    display2 = tk.Label(imageFrame2)
    display2.grid()

    cv2image = cv2.cvtColor(img1, cv2.COLOR_BGR2RGBA)
    rgb = cv2.cvtColor(cv2image, cv2.COLOR_RGBA2RGB)
    img2 = PIL.Image.fromarray(rgb)
    img2 = img2.resize((270, 480), PIL.Image.ANTIALIAS)
    imgtk = ImageTk.PhotoImage(image=img2)
    display2.imgtk = imgtk
    display2.configure(image=imgtk)
    window_pop.after(10000, destroy_widget, display2)
    window_pop.after(10000, destroy_widget, imageFrame2)
    window_pop.after(10000, destroy_widget, imlab2)

    imgr = cv2.imread(cn)
    imgr = cv2.cvtColor(imgr, cv2.COLOR_BGR2GRAY)
    t = threshold_local(imgr, 17, offset=15, method='gaussian')
    imgr = (imgr > t).astype('uint8') * 255
    repn = Path('Processed_image')
    if repn.is_dir():
        pass
    else:
        os.mkdir('Processed_image')
    cn1 = './Processed_image/img_' + str(crop_capture) + '.jpg'
    cv2.imwrite(cn1,imgr)
    scanned_imgs.append(cn1)
    print(scanned_imgs)
    imlab4 = tk.Label(window_pop, text="Scanned: "+ cn[16:], width=22, height=1, fg="white", bg="black",
                     font=('times', 15, ' bold '))
    imlab4.place(x=210, y=140)

    imageFrame4 = tk.Frame(window_pop)
    imageFrame4.place(x=210, y=170)

    display4 = tk.Label(imageFrame4)
    display4.grid()

    cv2image4 = cv2.cvtColor(imgr, cv2.COLOR_GRAY2RGBA)
    rgb4 = cv2.cvtColor(cv2image4, cv2.COLOR_RGBA2RGB)
    img4 = PIL.Image.fromarray(rgb4)
    img4 = img4.resize((270, 480), PIL.Image.ANTIALIAS)
    imgtk4 = ImageTk.PhotoImage(image=img4)
    display4.imgtk = imgtk4
    display4.configure(image=imgtk4)
    window_pop.after(10000, destroy_widget, display4)
    window_pop.after(10000, destroy_widget, imageFrame4)
    window_pop.after(10000, destroy_widget, imlab4)

def pdf_gen():
    global pdf_get, pdf_button_func, run, scanned_imgs
    print(run)
    if run == False:
        notice = tk.Label(window_pop, text='Scan The Image First!!', width=20, height=1, fg="white", bg="firebrick1",
                        font=('times', 13, ' bold '))
        notice.place(x=24, y=68)
        window_pop.after(2000, destroy_widget, notice)
        destroy_cam()
        pdf_button_func.destroy()
    else:
        pdf_button_func.destroy()
        pdf_get+=1

        ## Generate folder for PDF
        repn = Path('pdf_downloaded')
        if repn.is_dir():
            pass
        else:
            os.mkdir('pdf_downloaded')

        img = PIL.Image.new('RGB', (100, 30), color=(255, 255, 255))
        fnt = ImageFont.truetype('./use_image/arial.ttf', 13)
        d = ImageDraw.Draw(img)
        d.text((5, 10), "Scanned PDF ", font=fnt,fill=(0, 0, 0))
        img.save('./Processed_image/z.jpg')
        scanned_imgs.append('./Processed_image/z.jpg')
        #Generate PDF
        image_list = []
        for image in scanned_imgs:
            img = PIL.Image.open(image)
            img = img.convert('RGB')
            image_list.append(img)
        image_list.pop(-1)
        ts = time.time()
        timeStam = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
        Hour, Minute, Second = timeStam.split(":")
        img.save('./pdf_downloaded/Scanned_'+str(pdf_get)+'_'+str(Hour)+'_'+str(Minute)+'_'+str(Second)+'.pdf',save_all=True, append_images=image_list)
        notice = tk.Label(window_pop, text='PDF Generated!!', width=20, height=1, fg="black", bg="spring green",
                        font=('times', 13, ' bold '))
        notice.place(x=24, y=68)
        window_pop.after(2000, destroy_widget, notice)
        destroy_cam()


cp = tk.Button(window_pop, text='Turn on', bg="#33FFBD", fg="white", width=12,
               height=1, font=('times', 14), command=Run_thesetup, activebackground='yellow')
cp.place(x=430, y=33)

window_pop.mainloop()
#!/usr/bin/python

from os import *
import os
from pathlib import Path
from PIL import ImageTk
import PIL.Image
import glob
import random
import shutil
import Tkinter as tk
from Tkinter import *

res_dir = './res/'
art_dir = './res/art/'
good_dir = './res/good/'
bad_dir = './res/bad/'
ok_dir = './res/ok/'
img_dir = './img/'

if (os.path.exists(img_dir)):
	if (not os.path.isdir(img_dir)):
		print ("Unable to find img folder")
		quit()
else:
	print ("Unable to find img folder")
	quit()

#check directory exists else make it
if (os.path.exists(res_dir)):
	if (not os.path.isdir(res_dir)):
		print ("Unable to setup 'res' folder")
		quit()
	try:
		if (not os.path.exists(art_dir)):
			os.mkdir(art_dir)
		if (not os.path.exists(good_dir)):
			os.mkdir(good_dir)
		if (not os.path.exists(bad_dir)):
			os.mkdir(bad_dir)
		if (not os.path.exists(ok_dir)):
			os.mkdir(ok_dir)
	except:
		print ("Unable to setup 'res' folder")
else:
	try:
		os.mkdir(res_dir)
		os.mkdir(art_dir)
		os.mkdir(bad_dir)
		os.mkdir(good_dir)
		os.mkdir(ok_dir)
	except:
		print ("Unable to setup file/folders")
		quit()

img_list = glob.glob(img_dir + '*.jpg')
cur_photo = None
cur_id = None

root = tk.Tk()
root.title("Image Classifier")
root.geometry("600x675")
root.configure(bg="grey")

img_list_size = len(img_list)
if (not img_list_size):
	w = Label(root, text="Classification of image set has been completed. Thank you for your help :)", width=600)
	w.pack()
if (img_list_size):
	photo_id = [i for i in range(1, img_list_size + 1)]
	cur_id = random.randint(0, img_list_size - 1)
	cur_photo = ImageTk.PhotoImage(PIL.Image.open(img_list[cur_id]))
	img_l = Label(root, image=cur_photo, compound=CENTER)
	img_l.image = cur_photo
	img_l.pack()
	img_t = Label(root, text="Rate Image #" + str(photo_id[cur_id]), compound=CENTER, width=600)
	img_t.pack()
	w = Label(root, text="Press ['1' for bad] ['2' for ok] ['3' for good] ['4' for artsy] [<esc> to exit]", compound=CENTER, width=600)
	w.pack()
	m = Label(root, text="", width=600)
	m.pack() 
def updateImage():
	global cur_photo, img_list, cur_id
	img_list_size = len(img_list)
	if (img_list_size):
		cur_id = random.randint(0, img_list_size - 1)
		cur_photo = ImageTk.PhotoImage(PIL.Image.open(img_list[cur_id]))
		img_l.configure(image=cur_photo, compound=CENTER)
		img_l.image = cur_photo
		img_t.configure(text="Rate Image #" + str(photo_id[cur_id]), compound=CENTER, width=600)
		w.configure(text="Press ['1' for bad] ['2' for ok] ['3' for good] ['4' for artsy] [<esc> to exit]", compound=CENTER, width=600)
	else:
		img_l.configure(image='', borderwidth=0, highlightthickness=0, width=600)
		img_t.configure(text="", width=600)
		w.configure(text="Completed Set! Thank You\n<esc> to exit", width=600)
		m.configure(text="", width=600)

def movefile(press):
	global img_list
	if (len(img_list)):
		old_path = img_list[cur_id]
		old_id = photo_id[cur_id]
		base_name = os.path.basename(img_list[cur_id])
		del photo_id[cur_id]
		del img_list[cur_id]
		if (press == '1'):
			new_path = bad_dir + base_name
			message = "Image " + str(old_id) + " moved to bad"
			m.configure(text=message)
			shutil.move(old_path, new_path)
			updateImage()
		elif (press == '2'):
			new_path = ok_dir + base_name
			message = "Image " + str(old_id) + " moved to ok"
			m.configure(text=message)
			shutil.move(old_path, new_path)
			updateImage()
		elif (press == '3'):
			new_path = good_dir + base_name
			message = "Image " + str(old_id) + " moved to good"
			m.configure(text=message)
			shutil.move(old_path, new_path)
			updateImage()
		elif (press == '4'):
			new_path = art_dir + base_name
			message = "Image " + str(old_id) + " moved to artsy"
			m.configure(text=message)
			shutil.move(old_path, new_path)
			updateImage()

def keypress(event):
	if (event.keysym == 'Escape'):
		root.destroy()
	else:
		pass
		press = event.char
		if (press in ['1', '2', '3', '4']):
			movefile(press)
		else:
			pass

root.bind_all('<Key>', keypress);
root.mainloop()

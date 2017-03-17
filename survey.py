#!/usr/bin/python

from os import *
import os
import sys
from pathlib import Path
from PIL import ImageTk
import PIL.Image
import glob
import random
import shutil
import Tkinter as tk
from Tkinter import *
import tkMessageBox
from argparse import ArgumentParser
import argparse

cur_photo, img_list, cur_id = None, None, None
root, photo_id = None, None
res_dir = './res/'
best_dir = './res/best/'
good_dir = './res/good/'
bad_dir = './res/bad/'
ok_dir = './res/ok/'
img_dir = './img/'
result_file = './result_file'
username, name = None, None
w, m, img_l, img_t = None, None, None, None
progress = None
total_cnt = 0

def build_parser():
	parser = ArgumentParser()
	parser.add_argument('--username', metavar='INTRA ID', type=str, nargs=1,\
			help='Intra user id')
	parser.add_argument('--name', metavar='NAME', type=str, nargs='+', \
			help='Name')
	return (parser)

def updateImage():
	global cur_photo, img_list, cur_id, progress
	img_list_size = len(img_list)
	base_name = os.path.basename(img_list[cur_id])
	if (total_cnt):
		percent = int((1 - img_list_size / float(total_cnt)) * 100)
	else:
		percent = 100
	if (img_list_size):
		cur_id = random.randint(0, img_list_size - 1)
		cur_photo = ImageTk.PhotoImage(PIL.Image.open(img_list[cur_id]))
		img_l.configure(image=cur_photo, compound=CENTER, width=600) 
		img_l.image = cur_photo
		img_t.configure(text="Rate Image #" + str(photo_id[cur_id]) + " : " + base_name, compound=CENTER, width=600)
		w.configure(text="Press ['left' for Bad] ['down' for Ok] ['right' for Good] [<esc> to exit]", compound=CENTER, width=600)
		progress.configure(text="Progress: " + str(percent) + "%", width=600)
	else:
		img_l.configure(image='', borderwidth=0, highlightthickness=0, width=600)
		img_t.configure(text="", width=600)
		w.configure(text="Completed Set! Thank You\n<esc> to exit", width=600)
		m.configure(text="", width=600)
		progress.configure(text="", width=600)

def movefile(press):
	global img_list, photo_id
	if (len(img_list)):
		old_path = img_list[cur_id]
		old_id = photo_id[cur_id]
		base_name = os.path.basename(img_list[cur_id])
		del photo_id[cur_id]
		del img_list[cur_id]
		if (press == 'Left'):
			new_path = bad_dir + base_name
			message = "Image " + str(old_id) + " moved to Bad"
			m.configure(text=message)
			shutil.move(old_path, new_path)
			updateImage()
		elif (press == 'Down'):
			new_path = ok_dir + base_name
			message = "Image " + str(old_id) + " moved to Ok"
			m.configure(text=message)
			shutil.move(old_path, new_path)
			updateImage()
		elif (press == 'Right'):
			new_path = good_dir + base_name
			message = "Image " + str(old_id) + " moved to Good"
			m.configure(text=message)
			shutil.move(old_path, new_path)
			updateImage()

def keypress(event):
	if (event.keysym == 'Escape'):
		# with open(result_file, 'r') as res_file:j
		if (tkMessageBox.askokcancel("Quit", "Quit? If so, a result file will be generated. Please Slack DM @achan or @dgonchar your result file,\nresult_file.result")):
			cmd = 'echo "" > ' + result_file
			if (username):
				cmd = 'echo ' + username + ' >> ' + result_file
				os.system(cmd)
			if (name):
				cmd = 'echo ' + name + ' >> ' + result_file
				os.system(cmd)
			cmd = 'ls -lR ' + res_dir + ' >> ' + result_file
			os.system(cmd)
			root.destroy()
	else:
		pass
		press = event.keysym
		if (press in ['Left', 'Down', 'Right']):
			movefile(press)
		else:
			pass

def main():
	global cur_photo, img_list, cur_id, photo_id, root
	global m, w, img_t, img_l, progress, total_cnt, result_file
	global username, name

	parser = build_parser()
	args = parser.parse_args()

	if (len(sys.argv) > 1):

		if (args.username):
			user_app = '_'.join(args.username)
			username = user_app
		if (args.name):
			name_app = '_'.join(args.name)
			name = name_app
		result_file += '.result'

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
				if (not os.path.exists(best_dir)):
					os.mkdir(best_dir)
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
				os.mkdir(best_dir)
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
		root.geometry("600x700")
		root.configure(bg="grey")

		img_list_size = len(img_list)
		total_cnt = len(img_list)
		bad_list = glob.glob(bad_dir + '*.jpg')
		ok_list = glob.glob(ok_dir + '*.jpg')
		good_list = glob.glob(good_dir + '*.jpg')
		best_list = glob.glob(best_dir + '*.jpg')
		total_cnt += (len(bad_list) + len(good_list) + len(best_list) + len(ok_list))
		if (not img_list_size):
			w = Label(root, text="Classification of image set has been completed. Thank you for your help :)", width=600)
			w.pack()
		if (img_list_size):
			photo_id = [i for i in range(1, img_list_size + 1)]
			cur_id = random.randint(0, img_list_size - 1)
			cur_photo = ImageTk.PhotoImage(PIL.Image.open(img_list[cur_id]))
			img_l = Label(root, image=cur_photo, compound=CENTER, width=600)
			img_l.image = cur_photo
			img_l.pack()
			base_name = os.path.basename(img_list[cur_id])
			img_t = Label(root, text="Rate Image #" + str(photo_id[cur_id]) + " : " + base_name, compound=CENTER, width=600)
			img_t.pack()
			w = Label(root, text="Press ['left' for Bad] ['down' for Ok] ['right' for Good] [<esc> to exit]", compound=CENTER, width=600)
			w.pack()
			m = Label(root, text="", width=600)
			m.pack() 
			if (total_cnt):
				percent = int((1 - img_list_size / float(total_cnt)) * 100)
			else:
				percent = 100
			progress = Label(root, text="Progress: " + str(percent) + "%", width=600)
			progress.pack()

		root.bind_all('<Key>', keypress);
		root.mainloop()
	else:
		print ("Usage: ./survey.py --username <username> --name <name>")
	return (0)

if __name__ == "__main__":
	main()

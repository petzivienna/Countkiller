import os
import os.path
import PySimpleGUI as sg

startfolder = "C:/Users/User/Downloads/battle-for-wesnoth-win-stable/data/core/images"

for root, dirs, files in os.walk(startfolder): 
	for file in files:
		if file.endswith(".png"):
			answer = sg.PopupYesNo("keep this?"+"\n"+file, image=os.path.join(root, file))
			if answer == "Yes":
			    with open("output.csv", "a") as f:
				    f.write(os.path.join(root, file) + "\n")
				#print(file)

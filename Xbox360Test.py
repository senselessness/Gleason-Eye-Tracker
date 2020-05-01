from adafruit_servokit import ServoKit
import xbox
import time
import os
import glob
import colorama
from colorama import Fore, Back, Style

kit = ServoKit(channels=16)
kit.servo[0].set_pulse_width_range(500,3400)
kit.servo[1].set_pulse_width_range(500,3400)
kit.servo[2].set_pulse_width_range(500,3400)
kit.servo[3].set_pulse_width_range(500,3400)
kit.servo[4].set_pulse_width_range(500,3400)

ServoAngleVert = 45
ServoAngleHorz = 0
ServoAngleCenter = 180
kit.servo[0].angle = ServoAngleVert
kit.servo[1].angle = ServoAngleVert
kit.servo[2].angle = ServoAngleHorz
kit.servo[3].angle = ServoAngleHorz
kit.servo[4].angle = ServoAngleCenter

joy = xbox.Joystick()

Assigned = False

print(Fore.MAGENTA, '\tInstructions for use\n\tUp and Down on Dpads cotnrol vertical movement of eyes\n\tLeft and right control horizontal movement\n\tX and B control eye pitch\n\tY dicatates the document you will be writing to\n\tA saves position\n\tStart reads and moves to saved positions\n\tBack ends program', Style.RESET_ALL)

while not joy.Back():
	Up = joy.dpadUp()
	Down = joy.dpadDown()
	Left = joy.dpadLeft()
	Right = joy.dpadRight()
	XButton = joy.X()
	BButton = joy.B()
	AButton = joy.A()
	YButton = joy.Y()
	StartButton = joy.Start()

	if Up == 1 and ServoAngleVert <= 180:
		ServoAngleVert += 1
	elif Down == 1 and ServoAngleVert >= 0:
		ServoAngleVert -= 1
	if ServoAngleVert >= 0 and ServoAngleVert <= 180:
		kit.servo[0].angle = ServoAngleVert
		kit.servo[1].angle = ServoAngleVert
	if Left == 1 and ServoAngleHorz >= 0:
		ServoAngleHorz -= 1
	if Right == 1 and ServoAngleHorz <= 180:
		ServoAngleHorz += 1
	if ServoAngleHorz >= 0 and ServoAngleHorz <= 180:
		kit.servo[2].angle = ServoAngleHorz
		kit.servo[3].angle = ServoAngleHorz
	if BButton == 1 and ServoAngleCenter <= 180:
		ServoAngleCenter += 1
	if XButton == 1 and ServoAngleCenter >= 0:
		ServoAngleCenter -= 1
	if ServoAngleCenter >= 0 and ServoAngleCenter <= 180:
		kit.servo[4].angle = ServoAngleCenter

	if YButton == 1:
		Decision = "t"
		while Decision != "a" and Decision != "w":
			Assigned = True
			myFiles = glob.glob('*.txt')
			print(myFiles)
			Decision, DocName = input("\tTo Append Document type a\n\tType w to create or rewrite a document\n\tPlease type a or w followed by a space with the document name\n\tPlease do not include .txt\nResponse:   ").split()
			if Decision == "w":
				if os.path.isfile('./' + DocName + '.txt' ) == False:
					Recording = open(DocName + '.txt',"x")
				else:
					Recording = open(DocName + '.txt',"w")
				Recording.close()
			print("Will be writing to: ", DocName + "\n")

	if AButton == 1:
		if Assigned == True:
			try:
				Recording = open(DocName + '.txt', "a")
			except IOError:
				print("Issue writing to document\n")
			with Recording:
				HM = str(ServoAngleHorz)
				VM = str(ServoAngleVert)
				CM = str(ServoAngleCenter)
				Recording.write(HM + "\n")
				Recording.write(VM + "\n")
				Recording.write(CM + "\n")
				print("Current Positioned saved\n")
				time.sleep(.1)
		else:
			print("File hasn't been assigned. Please Press Y\n")

	if StartButton == 1:
		myFiles = glob.glob('*.txt')
		print(myFiles)
		FileName = input("Accepts only .txt\n.txt should not be typed\nName of the file you wish to open: ")
		try:
			Recording = open(FileName + ".txt","r")
		except IOError:
			print ("Error Opening File")
		with Recording:
			while True:
				line = Recording.readline()
				if line:
					ServoAngleHorz = int(line)
					ServoAngleVert = int(Recording.readline())
					ServoAngleCenter = int(Recording.readline())
					print("New Horizontal: %i", ServoAngleHorz, "\n" )
					print("New Vertical: %i", ServoAngleVert, "\n")
					print("New Center: %i", ServoAngleCenter, "\n")
					kit.servo[0].angle = ServoAngleVert
					kit.servo[1].angle = ServoAngleVert
					kit.servo[2].angle = ServoAngleHorz
					kit.servo[3].angle = ServoAngleHorz
					kit.servo[4].angle = ServoAngleCenter
					time.sleep(3)
				else:
					print("Done Reading Commands\n")
					Recording.close()
					break

	time.sleep(.1)
joy.close()

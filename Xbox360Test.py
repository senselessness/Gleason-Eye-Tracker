from adafruit_servokit import ServoKit
import xbox
import time
import os
import glob
import colorama
from colorama import Fore, Back, Style

#Assigns how many channels there are
kit = ServoKit(channels=16)
#Sets pulse width range of each servo
#Determines the range of how far it will rotate when assigning an angle
kit.servo[0].set_pulse_width_range(500,3400)
kit.servo[1].set_pulse_width_range(500,3400)
kit.servo[2].set_pulse_width_range(500,3400)
kit.servo[3].set_pulse_width_range(500,3400)
kit.servo[4].set_pulse_width_range(500,3400)
#Assign Angles to the servos. These are Safe angles.
#Servo 0 and 1 control the vertical eye movement
#Servo 2 and 3 controls horizontal movement
#Servo 4 controls eye pitch
ServoAngleVert = 45
ServoAngleHorz = 0
ServoAngleCenter = 180
kit.servo[0].angle = ServoAngleVert
kit.servo[1].angle = ServoAngleVert
kit.servo[2].angle = ServoAngleHorz
kit.servo[3].angle = ServoAngleHorz
kit.servo[4].angle = ServoAngleCenter
#Assigns Joy to the xbox object
joy = xbox.Joystick()

#This will ensure you don't get an error if you try and run the a saved .txt if you haven't selected one yet
Assigned = False
#Instructions on proper use
print(Fore.MAGENTA, '\tInstructions for use\n\tUp and Down on Dpads cotnrol vertical movement of eyes\n\tLeft and right control horizontal movement\n\tX and B control eye pitch\n\tY dicatates the document you will be writing to\n\tA saves position\n\tStart reads and moves to saved positions\n\tBack ends program', Style.RESET_ALL)
#Runs loop till back button is pressed
while not joy.Back():
	#Binds Keys
	Up = joy.dpadUp()
	Down = joy.dpadDown()
	Left = joy.dpadLeft()
	Right = joy.dpadRight()
	XButton = joy.X()
	BButton = joy.B()
	AButton = joy.A()
	YButton = joy.Y()
	StartButton = joy.Start()
	#As you hold the button on the dpad, the angle of the servo will change in one degree
	#Also includes checks to make sure you are not exceeding bounds
	#Includes X and B button as well
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
	#Determines the file wanting to be edited. Should be ran before start
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
	#Writes to selected file
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
	#Start button will read selected user file and execute the recorded positions
	#3 Second Delay to allow servos to reach the desired position. May want extend time period for scans
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
	#Time.sleep is important so only one press is recorded.
	time.sleep(.1)
joy.close()

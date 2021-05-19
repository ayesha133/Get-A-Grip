5## ----------------------------------------------------------------------------------------------------------
## TEMPLATE
## Please DO NOT change the naming convention within this template. Some changes may
## lead to your program not functioning as intended.

import sys
sys.path.append('../')

from Common_Libraries.p2_lib import *

import os
from Common_Libraries.repeating_timer_lib import repeating_timer

def update_sim ():
    try:
        arm.ping()
    except Exception as error_update_sim:
        print (error_update_sim)

arm = qarm()

update_thread = repeating_timer(2, update_sim)

import random

## STUDENT CODE BEGINS
## ----------------------------------------------------------------------------------------------------------
def randomContainer(): #Random container function, goes through container 1-6, and does 6 times until no random left
    container_ID = random.sample(range(1,7),6)
    return container_ID

def dropOff(ID): #Function to be called that moves qarm to correct location
    if ID == 1: 
        drop_off = [-0.6002, 0.2425, 0.4202] #Location of small red
    elif ID == 2:
        drop_off = [0.0, -0.6474, 0.4202] #Location of small green
    elif ID == 3:
        drop_off = [0.0, 0.6238, 0.4202] #Location of small blue
    elif ID == 4:
        drop_off = [-0.3900, 0.1400, 0.2900] #Location of big red
    elif ID == 5:
        drop_off = [0.0055, -0.4300, 0.3100] #Location of big green
    elif ID == 6:
        drop_off = [0.0055, 0.4300, 0.3100] #Location of big blue
    else:
        drop_off = [0.4064, 0.0, 0.4826] #Return home if all fails
    return drop_off

def gripperControl(rightArm, rightThreshold, bothThresholdNine, bothThresholdSeven): #This function controls the gripper
    if bothThresholdNine > rightArm > rightThreshold: #When right arm exceeds threshold, gripper will open, if not closes
        arm.control_gripper(40)
    elif bothThresholdSeven < rightArm < rightThreshold:
        arm.control_gripper(-40)

    return rightArm, rightThreshold
        
def moveArmLocation(bothThresholdOne, bothThresholdTwo, bothThresholdThree, bothThresholdFour, bothThresholdFive, bothThresholdEight, leftArm, rightArm, location):
    if bothThresholdEight > leftArm > bothThresholdThree and bothThresholdEight > rightArm > bothThresholdThree: #If both arms between threshold 
       arm.move_arm(location[0], location[1], location[2]) #Go to correct location
    elif leftArm > bothThresholdTwo and rightArm > bothThresholdTwo: #If both arms between threshold
        arm.move_arm(0.4064, 0.0, 0.4826) #Go home
        time.sleep(0.5)
    elif bothThresholdFive > leftArm > bothThresholdOne and bothThresholdFive > rightArm > bothThresholdOne: #If arms between threshold 
        time.sleep(0.5)
        arm.move_arm(0.5300, 0.0, 0.0211) #Move to pickup location
    return bothThresholdOne, bothThresholdTwo, bothThresholdThree, bothThresholdFour, bothThresholdFive, bothThresholdEight

def openingAutoclave(leftArm, leftThreshold, ID, bothThresholdFive, bothThresholdSix): #Function opens autoclave
    if bothThresholdSix > leftArm > leftThreshold and ID == 4:
        arm.open_red_autoclave(True) #Open autoclave if threshold is exceeded
    elif bothThresholdFive < leftArm < leftThreshold:
        arm.open_red_autoclave(False) #Close autoclave if threshold is not exceeded
        
    if bothThresholdSix > leftArm > leftThreshold and ID == 5:
        arm.open_green_autoclave(True)
    elif bothThresholdFive < leftArm < leftThreshold:
        arm.open_green_autoclave(False)
        
    if bothThresholdSix > leftArm > leftThreshold and ID == 6:
        arm.open_blue_autoclave(True)
    elif bothThresholdFive < leftArm < leftThreshold:
        arm.open_blue_autoclave(False)
    else:
        return None
    return leftArm, leftThreshold, ID, bothThresholdFive, bothThresholdSix

def terminate(leftArm, rightArm, bothThresholdFour,i): #This function counts the cages dropped. If i from the for loop is an odd number the function will return True
    if(i%2!=0):
        if leftArm > bothThresholdFour and rightArm > bothThresholdFour: #If arms below threshold
            arm.move_arm(0.4064, 0.0, 0.4826) #Reset to home location, ready to start again
            time.sleep(0.5)
            if(i==1):
                return True
            elif(i==3):
                return True
            elif(i==5):
                return True #This function counts the cages dropped. If i from the for loop is an even number the function will return False   
    else:
        if leftArm > bothThresholdFour and rightArm > bothThresholdFour: #If arms below threshold
            arm.move_arm(0.4064, 0.0, 0.4826) #Reset to home location, ready to start again
            time.sleep(0.5)
            if(i==2): 
                return False
            elif(i==4):
                return False
            elif(i==6): #This notifies the arm that this is the end of the program
                return True
                    
def main():
    location = []
    ID = randomContainer() #Call randomContainer function and store the list in ID
    count = 1
    rightThreshold = 0.9 #Thresholds for arms to exceed in order to operate properly
    leftThreshold = 0.5
    bothThresholdOne = 0.3
    bothThresholdTwo = 0.5
    bothThresholdThree = 0.7
    bothThresholdFour = 0.98
    bothThresholdFive = 0.4
    bothThresholdSix = 0.6
    bothThresholdSeven = 0.8
    bothThresholdEight = 0.85
    bothThresholdNine = 0.95
    

    for i in range(6): #This for loop runs the program 6 times to drop all containers
        if(i == 1):
            arm.spawn_cage(ID[i])
            print("containerID is: ", ID[i])
            location = dropOff(ID[i])
            while i==1: #Current position in list
                leftArm= arm.emg_left() #Variables for left and right arm emg functions
                rightArm = arm.emg_right()
                gripperControl(rightArm, rightThreshold, bothThresholdNine, bothThresholdSeven)
                moveArmLocation(bothThresholdOne, bothThresholdTwo, bothThresholdThree, bothThresholdFour, bothThresholdFive, bothThresholdEight, leftArm, rightArm, location)       
                openingAutoclave(leftArm, leftThreshold, ID[i], bothThresholdFive, bothThresholdSix)
                
                if(terminate(leftArm, rightArm, bothThresholdFour,i)==True):
                    i+=1
                    arm.spawn_cage(ID[i])
                    print("containerID is: ", ID[i])
                    location = dropOff(ID[i])
                    while i==2:
                        leftArm= arm.emg_left()
                        rightArm = arm.emg_right()
                        gripperControl(rightArm, rightThreshold, bothThresholdNine, bothThresholdSeven)
                        moveArmLocation(bothThresholdOne, bothThresholdTwo, bothThresholdThree, bothThresholdFour, bothThresholdFive, bothThresholdEight, leftArm, rightArm, location)       
                        openingAutoclave(leftArm, leftThreshold, ID[i], bothThresholdFive, bothThresholdSix)
                    
                        if(terminate(leftArm, rightArm, bothThresholdFour,i)==False):
                            i+=1
                            arm.spawn_cage(ID[i])
                            print("containerID is: ", ID[i])
                            location = dropOff(ID[i])
                            while i==3:
                                leftArm = arm.emg_left()
                                rightArm = arm.emg_right()
                                gripperControl(rightArm, rightThreshold, bothThresholdNine, bothThresholdSeven)
                                moveArmLocation(bothThresholdOne, bothThresholdTwo, bothThresholdThree, bothThresholdFour, bothThresholdFive, bothThresholdEight, leftArm, rightArm, location)       
                                openingAutoclave(leftArm, leftThreshold, ID[i], bothThresholdFive, bothThresholdSix)
                              
                                if(terminate(leftArm, rightArm, bothThresholdFour,i)==True):
                                    i+=1
                                    arm.spawn_cage(ID[i])
                                    print("containerID is: ", ID[i])
                                    location = dropOff(ID[i])
                                    
                                    while i==4:
                                        leftArm = arm.emg_left() #Variables for left and right arm emg functions
                                        rightArm = arm.emg_right()
                                        gripperControl(rightArm, rightThreshold, bothThresholdNine, bothThresholdSeven)
                                        moveArmLocation(bothThresholdOne, bothThresholdTwo, bothThresholdThree, bothThresholdFour, bothThresholdFive, bothThresholdEight, leftArm, rightArm, location)      
                                        openingAutoclave(leftArm, leftThreshold, ID[i], bothThresholdFive, bothThresholdSix)
                                    
                                        if(terminate(leftArm, rightArm, bothThresholdFour,i)==False):
                                            i+=1
                                            arm.spawn_cage(ID[i])
                                            print("containerID is: ", ID[i])
                                            location = dropOff(ID[i])
                                            while i==5:
                                                leftArm = arm.emg_left() #Variables for left and right arm emg functions
                                                rightArm = arm.emg_right()
                                                gripperControl(rightArm, rightThreshold, bothThresholdNine, bothThresholdSeven)
                                                moveArmLocation(bothThresholdOne, bothThresholdTwo, bothThresholdThree, bothThresholdFour, bothThresholdFive, bothThresholdEight, leftArm, rightArm, location)       
                                                openingAutoclave(leftArm, leftThreshold, ID[i], bothThresholdFive, bothThresholdSix)
                                    
                                                if(terminate(leftArm, rightArm, bothThresholdFour,i)==True):
                                                    i+=1
                                                    arm.spawn_cage(ID[0])
                                                    print("containerID is: ", ID[0])
                                                    location = dropOff(ID[0])
                                                    while i==6:
                                                        leftArm = arm.emg_left() #Variables for left and right arm emg functions
                                                        rightArm = arm.emg_right()
                                                        gripperControl(rightArm, rightThreshold, bothThresholdNine, bothThresholdSeven)
                                                        moveArmLocation(bothThresholdOne, bothThresholdTwo, bothThresholdThree, bothThresholdFour, bothThresholdFive, bothThresholdEight, leftArm, rightArm, location)       
                                                        openingAutoclave(leftArm, leftThreshold, ID[0], bothThresholdFive, bothThresholdSix)

                                                        if(terminate(leftArm, rightArm, bothThresholdFour,i)==True):
                                                            break
main()






import pygame
import os
import datetime
import subprocess
from gpiozero import Button
from settings import *


def onButtonPress():
    global currentGUIState
    if currentGUIState == GUIState.startScreen:
    	currentGUIState = GUIState.processing
    	os.system('sudo python ../ble_alco.py')


FPS = 60

# Initialize pygame module
pygame.init()
# Clock for assigning a certain fps (might not be necessary)
clock = pygame.time.Clock()

# Button for activating breath analysing
button = Button(21)
button.when_pressed = onButtonPress

# Create a display surface
screen = pygame.display.set_mode(RESOLUTION)
# Current state of the GUI (what picture to show)
currentGUIState = GUIState.startScreen

drunk = True  # Is the user drunk?
intoxication = 0  # The level of intoxication

timeoutStartTime = 0  # At what time moment did the result appear

# If the previous program closed unexpectedly, remove results file just in case
try:
    os.remove("results.txt")
except FileNotFoundError:
    pass

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break

    # If we are waiting for a response from the breath analyser
    if currentGUIState == GUIState.processing:
        try:
            with open("results.txt", "r") as resultsfile:
                intoxication = float(resultsfile.readline().strip("\n"))
                print("HERE!!!")
                currentGUIState = GUIState.showingResult
                timeoutStartTime = datetime.datetime.now()
                drunk = True if intoxication > drunkThreshold else False
                os.remove("results.txt")
        except FileNotFoundError:
            print("PROBLEMA 1")
            pass
        except ValueError:
            print("PROBLEMA 2")
            pass
    elif currentGUIState == GUIState.showingResult \
            and datetimeToMilliseconds(datetime.datetime.now() - timeoutStartTime) > timeout:
        currentGUIState = GUIState.startScreen

    # Display appropriate image according to GUI state
    # If user hasn't blown yet
    if currentGUIState == GUIState.startScreen:
        screen.blit(startScreenImg, (0, 0))
    # If the result is being processed
    elif currentGUIState == GUIState.processing:
        screen.blit(processingImg, (0, 0))
    # If the result is know
    elif currentGUIState == GUIState.showingResult:
        if drunk: # If the user is too drunk
            screen.blit(negativeResultImg, (0, 0))
        else:
            screen.blit(neutralResultImg, (0, 0))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()

import pygame
import os
import datetime
import subprocess
from gpiozero import Button
from settings import *


def onButtonPress():
    global currentGUIState
    if currentGUIState == GUIState.startScreen:
    	currentGUIState = GUIState.instructions
    	os.system('sudo python ../ble_alco.py')
    elif currentGUIState == GUIState.showingResult:
        imgCounter = 0
        currentGUIState = GUIState.startScreen


FPS = 60

# Initialize pygame module
pygame.init()
# Clock for assigning a certain fps (might not be necessary)
clock = pygame.time.Clock()

# Button for activating breath analysing
button = Button(21)
button.when_pressed = onButtonPress
# Wait 500ms to check if button is pressed
pressTime = 0

# Create a display surface
pygame.display.set_caption("Alcojon")
screen = pygame.display.set_mode(RESOLUTION)
font = pygame.font.SysFont("calibri", 40)
# Current state of the GUI (what picture to show)
currentGUIState = GUIState.startScreen
imgCounter = 0

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
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
            running = False
            break
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            if buttonLocation[0] <= pos[0] < buttonLocation[0] + buttonSize[0] \
            and buttonLocation[1] <= pos[1] < buttonLocation[1] + buttonSize[1]:
                running = False
                break

    # If we are waiting for a response from the breath analyser
    if currentGUIState == GUIState.processing:
        try:
            with open("results.txt", "r") as resultsfile:
                intoxication = float(resultsfile.readline().strip("\n"))
                intoxicationText = font.render("BAC: " + str(intoxication), True, (255, 255, 255))
                currentGUIState = GUIState.showingResult
                timeoutStartTime = datetime.datetime.now()
                drunk = True if intoxication > drunkThreshold else False
                os.remove("results.txt")
        except FileNotFoundError:
            pass
        except ValueError:
            pass
    elif currentGUIState == GUIState.showingResult \
            and datetimeToMilliseconds(datetime.datetime.now() - timeoutStartTime) > timeout:
        currentGUIState = GUIState.startScreen
        imgCounter = 0

    # Display appropriate image according to GUI state
    # If user hasn't blown yet
    if currentGUIState == GUIState.startScreen:
        screen.blit(startScreenImg, (0, 0))
    elif currentGUIState == GUIState.instructions:
        if imgCounter < len(instructionSequence) - 1:
            screen.blit(blankScreenImg, (0, 0))
            screen.blit(instructionSequence[imgCounter], (0, 0))

        if imgCounter <= 250:
            imgCounter += 1
        elif imgCounter > 250:
            currentGUIState = GUIState.processing
            imgCounter = 0

    # If the result is being processed
    elif currentGUIState == GUIState.processing:
        screen.blit(processingImg, (0, 0))
    # If the result is known
    elif currentGUIState == GUIState.showingResult:
        if drunk: # If the user is too drunk
            screen.blit(negativeResultImg, (0, 0))
        else:
            screen.blit(neutralResultImg, (0, 0))
        screen.blit(intoxicationText, (525, SCREEN_HEIGHT - 75))

    # Display button
    screen.blit(exitButtonImg, buttonLocation)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()

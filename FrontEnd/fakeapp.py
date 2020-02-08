import pygame
import os
import datetime
from settings import *

FPS = 60

# Initialize pygame module
pygame.init()
# Clock for assigning a certain fps (might not be necessary)
clock = pygame.time.Clock()

# Create a display surface
screen = pygame.display.set_mode(RESOLUTION)
# Current state of the GUI (what picture to show)
currentGUIState = GUIState.startScreen

drunk = True  # Is the user drunk?
intoxication = 0  # The level of intoxication

timeoutStartTime = 0  # At what time moment did the result appear

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and currentGUIState == GUIState.startScreen:
                currentGUIState = GUIState.processing

    # If we are waiting for a response from the breath analyser
    if currentGUIState == GUIState.processing:
        try:
            with open("results.txt") as resultsfile:
                intoxication = int(resultsfile.readline().strip("\n"))
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

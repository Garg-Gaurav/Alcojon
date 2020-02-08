import enum
import pygame


# Convert datetime Timedelta format to milliseconds (diff between two times)
def datetimeToMilliseconds(timedelta):
    return timedelta.days * 86400000 + timedelta.seconds * 1000 + timedelta.microseconds / 1000


# GUI states
class GUIState(enum.Enum):
    startScreen = 0
    processing = 1
    showingResult = 2


# GUI images
startScreenImg = pygame.image.load('../Design/splash_screen_1.png')
processingImg = pygame.image.load('../Design/processing.png')
negativeResultImg = pygame.image.load('../Design/result_no.png')
neutralResultImg = pygame.image.load('../Design/result_maybe.png')

# Image size
imgSize = startScreenImg.get_size()

# Screen parameters
if imgSize:
    SCREEN_WIDTH = imgSize[0]
    SCREEN_HEIGHT = imgSize[1]
else:
    SCREEN_WIDTH = 640
    SCREEN_HEIGHT = 480

# Screen resolution
RESOLUTION = (SCREEN_WIDTH, SCREEN_HEIGHT)

# Threshold for drunkenness
drunkThreshold = 0.4

# Timeout after getting the BAC input for the start screen to appear again (in milliseconds)
timeout = 30000

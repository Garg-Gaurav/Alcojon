import enum
import pygame


# Convert datetime Timedelta format to milliseconds (diff between two times)
def datetimeToMilliseconds(timedelta):
    return timedelta.days * 86400000 + timedelta.seconds * 1000 + timedelta.microseconds / 1000


# GUI states
class GUIState(enum.Enum):
    startScreen = 0
    instructions = 1
    processing = 2
    showingResult = 3


# GUI images
startScreenImg = pygame.image.load('../Design/splash_screen_3.png')
processingImg = pygame.image.load('../Design/loading.png')
negativeResultImg = pygame.image.load('../Design/result_no.png')
neutralResultImg = pygame.image.load('../Design/result_maybe.png')
blankScreenImg = pygame.image.load('../Design/blank.png')

# Exit button
exitButtonImg = pygame.image.load('../Design/xbutton.png')
exitButtonImg = pygame.transform.scale(exitButtonImg, (40, 40))

# Female head instruction animation pictures
instructionSequence = []
for i in range(90):
    fileindex = str(i) if i >= 10 else '0' + str(i)
    filename = '../Design/Female head vector/Female head vector/tra mdea_000'+fileindex+'.png'
    img = pygame.image.load(filename)
    img = pygame.transform.scale(img, (800, 480))
    instructionSequence.append(img)

imgSize = startScreenImg.get_size()
# Screen parameters
if imgSize:
    SCREEN_WIDTH = imgSize[0]
    SCREEN_HEIGHT = imgSize[1]
else:
    SCREEN_WIDTH = 640
    SCREEN_HEIGHT = 480

# Distance from button to screen edge
buttonPadding = 10
buttonSize = exitButtonImg.get_size()
buttonLocation = [SCREEN_WIDTH - buttonSize[0] - buttonPadding, buttonPadding]

# Screen resolution
RESOLUTION = (SCREEN_WIDTH, SCREEN_HEIGHT)

# Threshold for drunkenness
drunkThreshold = 0.4

# Timeout after getting the BAC input for the start screen to appear again (in milliseconds)
timeout = 300000

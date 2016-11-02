import pygame
import sys
import pytesseract
import PIL
import Image
import json
import os
import shutil

##########################################################################
# Settings
verbose = True
inputImage = "./input_data/id_f.jpg"
intermediateFolder = "./intermediate"
outputFolder = "./output"
templateFile = outputFolder + "/template.json"

##########################################################################
# Initializations
pygame.init()
running = True

##########################################################################
# Cleaning

try:  # Deleting an Existing template file
    os.remove(templateFile)
except OSError:
    if verbose:
        print "Template File not found, passing"
    pass
else:
    if verbose:
        print "Template File found, successfully deleted"


if os.path.exists(intermediateFolder):
    if verbose:
        print "intermediate folder found, Deleting"
    shutil.rmtree(intermediateFolder)

if verbose:
    print "Creating clean intermediate Folder at :", intermediateFolder
os.makedirs(intermediateFolder)


if os.path.exists(outputFolder):
    if verbose:
        print "outputFolder found, Deleting"
    shutil.rmtree(outputFolder)

if verbose:
    print "Creating clean outputFolder at :", outputFolder
os.makedirs(outputFolder)


##########################################################################
# Main Program
def setup(path):
    if verbose:
        print "Came in Setup function"
    px = pygame.image.load(path)
    if verbose:
        print "Image loaded from path :", path
    screen = pygame.display.set_mode(px.get_rect()[2:])
    screen.blit(px, px.get_rect())
    pygame.display.flip()
    return screen, px


def displayImage(screen, px, topleft, prior):
    #if verbose:
        #print "Came in displayImage function"

    # ensure that the rect always has positive width, height
    x, y = topleft
    width = pygame.mouse.get_pos()[0] - topleft[0]
    height = pygame.mouse.get_pos()[1] - topleft[1]

    if width < 0:
        x += width
        width = abs(width)
    if height < 0:
        y += height
        height = abs(height)

    # eliminate redundant drawing cycles (when mouse isn't moving)
    current = x, y, width, height
    if not (width and height):
        return current
    if current == prior:
        return current

    # draw transparent box and blit it onto canvas
    screen.blit(px, px.get_rect())
    im = pygame.Surface((width, height))
    im.fill((128, 128, 128))
    pygame.draw.rect(im, (32, 32, 32), im.get_rect(), 1)
    im.set_alpha(128)
    screen.blit(im, (x, y))
    pygame.display.flip()

    # return current box extents
    return (x, y, width, height)


def mainLoop(screen, px):
    if verbose:
        print "Came in mainLoop function"

    global running

    topleft = bottomright = prior = None
    n = 0
    while (n != 1 and running):
        try:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    if verbose:
                        print "Detected click"
                    if not topleft:
                        topleft = event.pos
                    else:
                        bottomright = event.pos
                        n = 1
                if event.type == pygame.QUIT:
                    if verbose:
                        print "Detected Exit, made running False"
                    running = False
                    pygame.quit()
                    #pygame.display.quit()
                    #pygame.quit()

            if topleft:
                prior = displayImage(screen, px, topleft, prior)
        except pygame.error as e:
            print "Found pygame error : ",e
        except e:
            print "Unknown error :",e
    if running:
        return (topleft + bottomright)

# try:
def backgroundMain():
    if verbose:
        print "Came in backgroundMain function"

    global running

    scaledImg = intermediateFolder + '/scaledDownImage.png'
    img = Image.open(inputImage)
    # TODO change the resizing formula
    img = img.resize((1200, int(
        (float(img.size[1]) * float(1200 / float(img.size[0]))))), PIL.Image.ANTIALIAS)

    img.save(scaledImg)
    if verbose:
        print "saved scaled down version of image at :" + scaledImg

    if verbose:
        print "Going to setup"
    screen, px = setup(scaledImg)

    if verbose:
        print "Going to mainLoop"

    try:
        left, upper, right, lower = mainLoop(screen, px)
    except:
        pygame.display.quit()
        return

    # ensure output rect always has positive width, height
    if right < left:
        left, right = right, left
    if lower < upper:
        lower, upper = upper, lower

    im = Image.open(scaledImg)
    if verbose:
        print "Opened Scaled image"

    if verbose:
        print "Got the selection on :"
        print left, upper, right, lower
        if(left==right and upper == lower):
            if verbose:
                print 'Double Click'
            running = False
            return

    try:
        dataFile = open(templateFile, "r")
        mainJSON = json.load(dataFile)
    except:
        mainJSON = {}
        if verbose:
            print "NO File found So creating empty object"
    else:
        if verbose:
            print "existing File found reading from that"

    im = im.crop((left, upper, right, lower))
    if verbose:
        print "Croped Image"

    readData = pytesseract.image_to_string(im)
    print "Read data is :" + readData
    fieldName = raw_input("What is this field Name ?")

    mainJSON[fieldName] = {'x1': left, 'y1': upper, 'x2': right, 'y2': lower}

    with open(templateFile, 'w') as outfile:
        json.dump(mainJSON, outfile)
        if verbose:
            print "saved to template file :",templateFile

    pygame.display.quit()
    if verbose:
        print "Closed the display"

    return

while running:
    backgroundMain()


if verbose:
    print "Exiting"

from PIL import Image
import PIL
import pytesseract
import json
import shutil
import os

##########################################################################
# Settings
verbose = True
inputFolder = "./input_data/imageset/set1"
intermediateFolder = "./intermediate/set1"
outputFolder = "./output/set1"
templateFile = "./output/template.json"

##########################################################################
# Initializations
running = True

##########################################################################
# Cleaning
#
# try:  # Deleting an Existing template file
#     os.remove(templateFile)
# except OSError:
#     if verbose:
#         print "Template File not found, passing"
#     pass
# else:
#     if verbose:
#         print "Template File found, successfully deleted"


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

with open(templateFile, 'r') as f:
    template = json.load(f)
    if verbose:
        print "Loaded Template"

    index = 0

    for filename in os.listdir(inputFolder):
        img = Image.open(os.path.join(inputFolder, filename))

        if verbose:
            print "Opened Image :", os.path.join(inputFolder, filename)

        scaledImgPath = intermediateFolder + '/scaledImage_'+str(index)+'.png'

        # TODO change the resizing formula
        scaledImg = img.resize((1200, int(
            (float(img.size[1]) * float(1200 / float(img.size[0]))))), PIL.Image.ANTIALIAS)

        scaledImg.save(scaledImgPath)

        for key, value in template.iteritems():
            croppedImage = scaledImg.crop(
                (value['left'], value['upper'], value['right'], value['lower']))
            if verbose:
                print "Cropped Image for : ", key

            croppedImage.save(outputFolder + '/crop_' +
                              str(index) + '_' + key + '.png')
            readData = pytesseract.image_to_string(croppedImage)
            print "readData : ", readData
        index+=1
        

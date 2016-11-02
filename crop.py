from PIL import Image
import pytesseract
import json
import re

with open('./output_data/data.json', 'r') as f:
    data = json.load(f)

    for key, value in data.iteritems():
        print "Key : ", key
        # print "Value: ", value
        # print "X1 :", value['x1']
        # print "Y1 :", value['y1']
        # print "X2 :", value['x2']
        # print "Y2 :", value['y2']
        img = Image.open("./output_data/sompic.png")
        img2 = img.crop(value['x1'], value['y1'], value['x2'], value['y2']))
        img2.save('./output_data/crop_' + key + '.png')

        # a=pytesseract.image_to_string(Image.open('./output_data/out.png'))
        # text_file.write(a)


# f = open("./output_data/address.json", "a")
# img = Image.open("./output_data/sompic.png")
# print j
# j = json.load(f)
# img2 = img.crop((112, 313, 319, 467))
# print img2.size
# img2.save('./output_data/crop.png')
# img3 = Image.open("./output_data/out.png")
# print img3.size

import pygame
import sys
import pytesseract
import PIL
import Image
import json
once = 1
pygame.init()


def setup(path):
    px = pygame.image.load(path)
    screen = pygame.display.set_mode(px.get_rect()[2:])
    screen.blit(px, px.get_rect())
    pygame.display.flip()
    return screen, px


def displayImage(screen, px, topleft, prior):
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
    topleft = bottomright = prior = None
    n = 0
    while n != 1:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                if not topleft:
                    topleft = event.pos
                else:
                    bottomright = event.pos
                    n = 1
            if event.type == pygame.QUIT:
                running = False
                pygame.display.quit()
                pygame.quit()

        if topleft:
            prior = displayImage(screen, px, topleft, prior)

    return (topleft + bottomright)


input_loc = './output_data/sompic.png'

try:
    def backgroundMain():
        img = Image.open('./input_data/id_f.jpg')
        img = img.resize((1200, int(
            (float(img.size[1]) * float(1200 / float(img.size[0]))))), PIL.Image.ANTIALIAS)
        img.save('./output_data/sompic.png')
        output_loc = './output_data/out.png'
        screen, px = setup(input_loc)
        left, upper, right, lower = mainLoop(screen, px)

        # ensure output rect always has positive width, height
        if right < left:
            left, right = right, left
        if lower < upper:
            lower, upper = upper, lower
        im = Image.open(input_loc)

        print left, upper, right, lower
        j = [{'x1': left, 'y1': upper, 'x2': right, 'y2': lower}]
        #itis = str(inupt)
        f = open("./output_data/data.json", "a")
        json.dump(raw_input(), f)
        json.dump(j, f)
        im = im.crop((left, upper, right, lower))
        pygame.display.quit()
        im.save(output_loc)
        print "\nThis is size of image"
        print im.size

        pass

    while 1:
        backgroundMain()
        text_file = open("./output_data/file.txt", "a")  # open text file
        #var = raw_input("Enter selection identity: ")
        # print "You entered", var
        a = pytesseract.image_to_string(Image.open('./output_data/out.png'))
        text_file.write(a)
        #text_file.write(var + "\n")


except (RuntimeError, TypeError, NameError):
    pass

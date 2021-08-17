import cairo
import random
import itertools
import numpy as np
from PIL import Image


# USER INTERFACE ##########################################################################################
# set the number of slots in the x-axis:
resX = 150  
# set the colour palette:
lightCol = np.array([238, 232, 213])
midCol = np.array([181, 137, 0])
deepCol = np.array([0, 43, 54])
# /USER INTERFACE #########################################################################################


# resizing the imported image
raw_img = Image.open('input_img.jpg')  # change the raw image name here
wPercent = (resX / float(raw_img.size[0]))
resY = int((float(raw_img.size[1]) * float(wPercent)))
img = raw_img.resize((resX, resY), Image.ANTIALIAS)
img.save('resized_img.jpg')

# turning images into arrays
image_gray = Image.open('resized_img.jpg').convert("L")
GRAY_pix_arr = np.asarray(image_gray)
con_GRAY_pix_arr = np.concatenate(GRAY_pix_arr, axis=None)

# turning images into distinct colour array
DtoM = np.quantile(con_GRAY_pix_arr, .33)
LtoM = np.quantile(con_GRAY_pix_arr, .66)
DIST_pix_arr = np.ndarray(shape=(resX, resY, 3), dtype=np.uint8)
for i, j in itertools.product(range(resX), range(resY)):
    if int(np.linalg.norm(GRAY_pix_arr[j][i])) < DtoM:  # it's the deep colour
        DIST_pix_arr[i][j] = deepCol
    # it's thelight colour
    elif int(np.linalg.norm(GRAY_pix_arr[j][i])) > LtoM:
        DIST_pix_arr[i][j] = lightCol
    else:  # it's middle the colour
        DIST_pix_arr[i][j] = midCol

im = Image.fromarray(DIST_pix_arr)
im.save("distinct_img.jpg")

# setting the drawing canvas
WIDTH = resX*11
HEIGHT = resY*11
PIXEL_SCALE = 1
surface = cairo.ImageSurface(
    cairo.FORMAT_RGB24, WIDTH * PIXEL_SCALE, HEIGHT * PIXEL_SCALE)
ctx = cairo.Context(surface)
ctx.scale(PIXEL_SCALE, PIXEL_SCALE)
ctx.rectangle(0, 0, WIDTH, HEIGHT)
ctx.set_source_rgb(255, 255, 255)
ctx.fill()


# position function used later in the code
def Give_pos(x, y, vacaArr, distArr):
    outList = []
    try:
        if vacaArr[x + 1][y] == 0 and np.array_equal(distArr[x][y], distArr[x + 1][y]):
            outList.append([x + 1, y])
    except:
        pass
    try:
        if vacaArr[x - 1][y] == 0 and np.array_equal(distArr[x][y], distArr[x - 1][y]):
            outList.append([x - 1, y])
    except:
        pass
    try:
        if vacaArr[x][y + 1] == 0 and np.array_equal(distArr[x][y], distArr[x][y + 1]):
            outList.append([x, y + 1])
    except:
        pass
    try:
        if vacaArr[x][y - 1] == 0 and np.array_equal(distArr[x][y], distArr[x][y - 1]):
            outList.append([x, y - 1])
    except:
        pass
    return outList


# Drawing code
VACA_pix_arr = np.zeros((resX, resY))
wStroke = resX//30
for i, j in itertools.product(random.sample(list(range(resX)), resX), random.sample(list(range(resY)), resY)):
    xScale = WIDTH / resX
    yScale = HEIGHT / resY
    if VACA_pix_arr[i][j] == 0:
        poss_xy = Give_pos(i, j, VACA_pix_arr, DIST_pix_arr)
        if poss_xy:
            while poss_xy:
                ctx.move_to(xScale * i, yScale * j)
                nextPos = random.choice(poss_xy)
                ctx.line_to(xScale * nextPos[0], yScale * nextPos[1])
                VACA_pix_arr[nextPos[0]][nextPos[1]] = 1
                poss_xy = Give_pos(
                    nextPos[0], nextPos[1], VACA_pix_arr, DIST_pix_arr)
                ctx.set_source_rgb(DIST_pix_arr[i][j][0] / 255, DIST_pix_arr[i][j][1] / 255,
                                   DIST_pix_arr[i][j][2] / 255)
                ctx.set_line_width(wStroke)
                ctx.stroke()
                ctx.arc(xScale * i, yScale * j, wStroke/2, 0, 2 * np.pi)
                ctx.set_source_rgb(
                    DIST_pix_arr[i][j][0] / 255, DIST_pix_arr[i][j][1] / 255, DIST_pix_arr[i][j][2] / 255)
                ctx.fill()
                i, j = nextPos[0], nextPos[1]
        else:
            ctx.arc(xScale * i, yScale * j, wStroke/1.5, 0, 2 * np.pi)
            ctx.set_source_rgb(
                DIST_pix_arr[i][j][0] / 255, DIST_pix_arr[i][j][1] / 255, DIST_pix_arr[i][j][2] / 255)
            ctx.fill()
        VACA_pix_arr[i][j] = 1

surface.write_to_png('output_img.png')

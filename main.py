import cv2
import numpy as np

COLORS = 32
FILE_PATH = 'data/website.jpg'
TILE = 'beer'
SCALE = 25

# Load image
org = cv2.imread(FILE_PATH)
tile = cv2.imread(f'data/tiles/{TILE}.png')

# Resize image
img = cv2.resize(org, (0,0), fx=1/(SCALE/2), fy=1/(SCALE/2))
tile = cv2.resize(tile, (SCALE, SCALE))
tile = tile.astype('float')

# Make less colors
def quantize_colors(img, colors):
    img = img.astype('float')
    img = np.round(img/255*colors)/colors*255
    return img.astype('uint8')

img = quantize_colors(img, COLORS)

# Output image
result = np.ones((img.shape[0]*SCALE, img.shape[1]*SCALE, 3), dtype=np.float32)*255

def make_move_color(result, tile, scale, yx, bgr):
    patt = tile.copy()
    for y in range(patt.shape[0]):
        for x in range(patt.shape[1]):
            if (patt[y][x] != np.array([255,255,255])).all():
                patt[y][x] += bgr
                if (patt[y][x] > np.array([255,255,255])).any():
                    b,g,r = patt[y][x]
                    if b > 255:
                        patt[y][x][0]=patt[y][x-1][0]
                    if g > 255:
                        patt[y][x][1]=patt[y][x-1][1]
                    if r > 255:
                        patt[y][x][2]=patt[y][x-1][2]


    y, x = yx[0]*SCALE, yx[1]*SCALE
    result[y:y+SCALE, x:x+SCALE] = patt

# Move colors
for y in range(img.shape[0]):
    for x in range(img.shape[1]):
        make_move_color(result, tile, SCALE, (y,x), img[y,x])

result = result.astype('uint8')
result = cv2.resize(result, (org.shape[1], org.shape[0]))

cv2.imshow('image', org)
cv2.waitKey(0)
cv2.imshow('image', result)
cv2.waitKey(0)
cv2.destroyAllWindows()

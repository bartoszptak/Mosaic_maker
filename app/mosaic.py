import cv2
import numpy as np
import numpy.ma as ma
import time

COLORS = 32
FILE_PATH = 'data/website.jpg'
TILE = 'circle'
SCALE = 25

### TO DELETE ###
start = time.time()
#################


def get_mosaic_list():
    from glob import glob
    files = glob('data/tiles/*.png')
    result = []
    for file in files:
        result.append(file.split('/')[-1].split('.')[0].title())
    return sorted(result)


# Load image
org = cv2.imread(FILE_PATH)
tile = cv2.imread(f'data/tiles/{TILE}.png')

# Resize image
img = cv2.resize(org, (0, 0), fx=1/(SCALE/2), fy=1/(SCALE/2))
tile = cv2.resize(tile, (SCALE, SCALE))
tile = tile.astype('float')

# Make less colors

def quantize_colors(img, colors):
    img = img.astype('float')
    return np.round(img/255*colors)/colors*255

img = quantize_colors(img, COLORS)


# Output image
result = np.ones((img.shape[0]*SCALE, img.shape[1]
                  * SCALE, 3), dtype=np.float32)*255


def make_move_color(result, tile, scale, yx, bgr):
    patt = tile.copy()
    patt += bgr
    patt[ma.masked_where(patt > 255, patt).mask] = 255.

    y, x = yx[0]*SCALE, yx[1]*SCALE
    result[y:y+SCALE, x:x+SCALE] = patt


# Move colors
for y in range(img.shape[0]):
    for x in range(img.shape[1]):
        make_move_color(result, tile, SCALE, (y, x), img[y, x])

result = result.astype('uint8')
result = cv2.resize(result, (org.shape[1], org.shape[0]))

### TO DELETE ###
print(f'{time.time()-start} s')

cv2.imshow('image', org)
cv2.waitKey(0)
cv2.imshow('image', result)
cv2.waitKey(0)
cv2.destroyAllWindows()
#################

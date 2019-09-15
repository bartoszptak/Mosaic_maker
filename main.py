import cv2
import numpy as np

COLORS = 32
FILE_PATH = 'data/website.jpg'
TILE = 'circle'
SCALE = 15

# Load image
org = cv2.imread(FILE_PATH)
tile = cv2.imread(f'data/tiles/{TILE}.png')

# Resize image
img = cv2.resize(org, (0,0), fx=1/(SCALE/2), fy=1/(SCALE/2))
tile = cv2.resize(tile, (SCALE, SCALE))

# Make less colors
def quantize_colors(img, colors):
    img = img.astype('float')
    img = np.round(img/255*colors)/colors*255
    return img.astype('uint8')

img = quantize_colors(img, COLORS)

# Output image
result = np.ones((img.shape[0]*SCALE, img.shape[1]*SCALE, 3), dtype=np.uint8)*255

def make_move_color(result, tile, yx, bgr):
    pass

# Move colors
for y in range(img.shape[0]):
    for x in range(img.shape[1]):
        make_move_color(result, tile, (y,x), img[y,x].tolist())

result = cv2.resize(result, (org.shape[1], org.shape[0]))

cv2.imshow('image', org)
cv2.waitKey(0)
cv2.imshow('image', result)
cv2.waitKey(0)
cv2.destroyAllWindows()

import cv2
import numpy as np
import numpy.ma as ma
import time

COLORS = 32

def get_mosaic_list():
    """Return the list of mosaic titles."""
    from glob import glob
    files = glob('data/tiles/*.png')
    result = []
    for file in files:
        result.append(file.split('/')[-1].split('.')[0].title())
    return sorted(result)

def read_all(file, tile):
    """Return the loaded image and tile."""
    org = cv2.imread(file)
    tile = cv2.imread(f'data/tiles/{tile}.png')
    return org, tile

def resize_all(img, tile, size):
    """Resize image elements."""
    img = cv2.resize(img, (0, 0), fx=1/(size/2), fy=1/(size/2))
    tile = cv2.resize(tile, (size, size))
    tile = tile.astype('float')
    return img, tile

def quantize_colors(img, colors):
    """Reduce the number of colors in the image."""
    img = img.astype('float')
    return np.round(img/255*colors)/colors*255

def make_move_color(result, tile, scale, yx, bgr):
    """Move a tile of the right color to the image."""
    patt = tile.copy()
    patt += bgr
    patt[ma.masked_where(patt > 255, patt).mask] = 255.

    y, x = yx[0]*scale, yx[1]*scale
    result[y:y+scale, x:x+scale] = patt

def get_mosaic(img, tile, size, shape):
    """A function that creates a mosaic."""
    result = np.ones((img.shape[0]*size, img.shape[1]
                    * size, 3), dtype=np.float32)*255

    for y in range(img.shape[0]):
        for x in range(img.shape[1]):
            make_move_color(result, tile, size, (y, x), img[y, x])

    result = result.astype('uint8')
    return cv2.resize(result, (shape[1], shape[0]))

def make_mosaic(img_file, tile_file, size):
    """The main function that loads the image, processes and saves."""
    img, tile = read_all(img_file, tile_file)
    shape = img.shape
    img, tile = resize_all(img, tile, size)

    img = quantize_colors(img, COLORS)

    mosaic = get_mosaic(img, tile, size, shape)

    cv2.imwrite(img_file, mosaic)

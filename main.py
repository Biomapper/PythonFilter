import sys
from os import scandir
from PIL import Image
import time
import math


def filterPixel(pixel, filterMin, filterMax):

    # Initialize pixel RGB values.
    red = pixel[0]
    green = pixel[1]
    blue = pixel[2]
    HALF_VAL = 127.5  # = 255 * 1/2

    # Initialize values used for filter value mapping.
    INVALID_MAP_VAL = -1
    pixelMappedVal = INVALID_MAP_VAL
    SLOPE_CONST = 200/255

    # 0 <= val < 200, blue is increasing.
    if red < HALF_VAL and green < HALF_VAL and blue < 255:
        pixelMappedVal = math.floor(blue * SLOPE_CONST)

    # 200 >= val < 400, green is increasing.
    elif red < HALF_VAL and green < 255 and blue > HALF_VAL:
        pixelMappedVal = math.floor(green * SLOPE_CONST + 200)

    # 400 <= val <  600, blue is decreasing.
    elif red < HALF_VAL and green < HALF_VAL and blue > 0:
        pixelMappedVal = math.floor(-1 * blue * SLOPE_CONST + 600)

    # 600 <= val <  800, red is increasing.
    elif red < 255 and green > HALF_VAL and blue < HALF_VAL:
        pixelMappedVal = math.floor(red * SLOPE_CONST + 600)

    # 800 <= val <  1000, green is decreasing.
    elif red > HALF_VAL and green > 0 and blue < HALF_VAL:
        pixelMappedVal = math.floor(-1 * green * SLOPE_CONST + 1000)

    # 900 <= val <= 1200, blue and green are increasing.
    elif red > HALF_VAL and green >= 0 and blue >= 0:
        pixelMappedVal = math.floor(blue * SLOPE_CONST + 1000)

    # Check if mapped pixel value is outside of specified range
    if pixelMappedVal < filterMin or pixelMappedVal > filterMax or pixelMappedVal == INVALID_MAP_VAL:
        # Clear the pixel by making it black
        return (255, 255, 255, 0)
    # Else the pixel does not need to be modified
    if red == 0 and green == 0 and blue == 0:
       pixel = (255, 255, 255, 0)

    return pixel


def main():
    # Open, loads pixel values, and gets size of image
    image = Image.open(sys.argv[1])
    image = image.convert('RGBA')
    imagePixels = image.load()

    RGB_values = []

    width, height = image.size
    # lowFilter(image, int(sys.argv[2]))
    # Loop over pixels
    for x in range(0, width):
        for y in range(0, height):
            imagePixels[x, y] = filterPixel(
                imagePixels[x, y], int(sys.argv[2]), int(sys.argv[3]))

    my_dict = {i: RGB_values.count(i) for i in RGB_values}
    imgNum = '_'.join(sys.argv[1].split('/')[-3::]).strip('.png')
    image.save('filteredTiles/' + imgNum + "filtered.png")


if __name__ == '__main__':
    main()
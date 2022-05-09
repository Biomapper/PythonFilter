
import sys
from PIL import Image



def valueFromPoint( pixel, maxValue ):
    # Initialize pixel RGB values.
    red = pixel[0]
    green = pixel[1]
    blue = pixel[2]
    alpha = pixel[3]
    HALF_VAL = 127.5  # = 255 * 1/2

    # Initialize values used for value mapping.
    SECTION_SIZE = maxValue / 6
    SLOPE_CONST = SECTION_SIZE/255

    # Transparent pixels represent no data.
    if alpha < HALF_VAL:
        return "No Data"

    # 0 <= val < 1sec, blue is increasing.
    elif red < HALF_VAL and green < HALF_VAL and blue < 255:
        return round( blue * SLOPE_CONST )

    # 1sec <= val < 2sec, green is increasing.
    elif red < HALF_VAL and green < 255 and blue > HALF_VAL:
        return round( green * SLOPE_CONST + SECTION_SIZE )

    # 2sec <= val < 3sec, blue is decreasing.
    elif red < HALF_VAL and green > HALF_VAL and blue > 0:
        return round( -1 * blue * SLOPE_CONST + 3*SECTION_SIZE )

    # 3sec <= val < 4sec, red is increasing.
    elif red < 255 and green > HALF_VAL and blue < HALF_VAL:
        return round( red * SLOPE_CONST + 3*SECTION_SIZE )

    # 4sec <= val < 5sec, green is decreasing.
    elif red > HALF_VAL and green > 0 and blue < HALF_VAL:
        return round( -1 * green * SLOPE_CONST + 5*SECTION_SIZE )

    # 5sec <= val <= maxValue, blue and green are increasing.
    elif red > HALF_VAL and green >= 0 and blue >= 0:
        return round( blue * SLOPE_CONST + 5*SECTION_SIZE )

    return "Server Error"



def main():
    # Open, loads pixel values, and gets size of image
    image = Image.open( sys.argv[1] )
    image = image.convert('RGBA')
    imagePixels = image.load()

    xCoor = int(sys.argv[2])
    yCoor = int(sys.argv[3])
    maxValue = int(sys.argv[4])
    
    width, height = image.size
    
    # Check that coordinates are valid
    if 0 <= xCoor and xCoor < width and 0 <= yCoor and yCoor < height:
        dataValue = valueFromPoint( imagePixels[xCoor, yCoor], maxValue )
        print( dataValue )
        return dataValue
         
    

if __name__ == '__main__':
    main()



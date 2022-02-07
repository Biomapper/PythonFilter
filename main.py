from PIL import Image
import time


def main(imageIn):
    # Open, loads pixel values, and gets size of image
    image = Image.open(imageIn)
    imagePixels = image.load()
    width, height = image.size

    # Loop over pixels
    for x in range(0, width):
        for y in range(0, height):
            # Assigns rgb values from image
            (r, g, b) = imagePixels[x, y]

            # can filter colors based on r, g, b values
            if g >= 239:
                imagePixels[x, y] = (0, 0, 0)

            if b >= 235:
                imagePixels[x, y] = (0, 0, 0)

    return image


if __name__ == '__main__':
    # Start time to test speed
    start_time = time.time()

    # calls main and saves the image as filtered.png (final version will not save to reduce space complexity
    main('AFRICA_DEM.png').save('filtered.png')

    # Format and end timer to print
    formattedTime = round(time.time() - start_time, 3)
    print(formattedTime)

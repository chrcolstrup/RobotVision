def obj_detect(input_img):
    print('Finding bricks by color')
    import cv2 as cv
    import numpy as np

    # InRange
    # Convert image to HSV
    input_img_hsv = cv.cvtColor(input_img, cv.COLOR_BGR2HSV)

    # Size of kernel for morphology, determined by trial-and-error
    kernel = np.ones((15, 15), np.uint8)

    # HSV: Hue (0-180), Saturation (0-255), Value (0-255)
    # NOTE: Hue is halved from 0-360 to fit in 8-bit.

    # Green
    green = 70/2
    lower_green = (green-10, 90, 90)  # Lower InRange HSV bounds
    upper_green = (green+10, 255, 255)  # Upper InRange HSV bounds
    mask_green = cv.inRange(input_img_hsv, lower_green, upper_green)  # InRange thresholding
    mask_green = cv.morphologyEx(mask_green, cv.MORPH_CLOSE, kernel)  # Morphology, closing operation
    mask_green = cv.morphologyEx(mask_green, cv.MORPH_OPEN, kernel)  # Morphology, opening operation
    cv.imwrite('mask_green.png', mask_green)

    # Yellow
    yellow = 46/2
    lower_yellow = (yellow-5, 100, 100)
    upper_yellow = (yellow+5, 255, 255)
    mask_yellow = cv.inRange(input_img_hsv, lower_yellow, upper_yellow)
    mask_yellow = cv.morphologyEx(mask_yellow, cv.MORPH_CLOSE, kernel)
    mask_yellow = cv.morphologyEx(mask_yellow, cv.MORPH_OPEN, kernel)
    cv.imwrite('mask_yellow.png', mask_yellow)

    # Orange
    lower_orange = (0, 110, 150)
    upper_orange = (15, 255, 255)
    mask_orange_1 = cv.inRange(input_img_hsv, lower_orange, upper_orange)
    lower_orange = (170, 110, 150)
    upper_orange = (180, 255, 255)
    mask_orange_2 = cv.inRange(input_img_hsv, lower_orange, upper_orange)
    mask_orange = mask_orange_1+mask_orange_2
    mask_orange = cv.morphologyEx(mask_orange, cv.MORPH_CLOSE, kernel)
    mask_orange = cv.morphologyEx(mask_orange, cv.MORPH_OPEN, kernel)
    cv.imwrite('mask_orange.png', mask_orange)

    # Blue
    blue = 190/2
    lower_blue = (blue-10, 0, 100)
    upper_blue = (blue+10, 255, 255)
    mask_blue = cv.inRange(input_img_hsv, lower_blue, upper_blue)
    mask_blue = cv.morphologyEx(mask_blue, cv.MORPH_CLOSE, kernel)
    mask_blue = cv.morphologyEx(mask_blue, cv.MORPH_OPEN, kernel)
    cv.imwrite('mask_blue.png', mask_blue)

    # White (but painted black on top)
    lower_white = (0, 0, 0)
    upper_white = (180, 255, 75)
    mask_white = cv.inRange(input_img_hsv, lower_white, upper_white)
    mask_white = cv.morphologyEx(mask_white, cv.MORPH_CLOSE, kernel)
    mask_white = cv.morphologyEx(mask_white, cv.MORPH_OPEN, kernel)
    cv.imwrite('mask_white.png', mask_white)

    # For sake of easy overview, an image of all detected objects is saved
    mask_all = mask_white + mask_blue + mask_orange + mask_green + mask_yellow
    cv.imwrite('mask_all.png', mask_all)
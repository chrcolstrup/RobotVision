def contour_detect(color, area_cutoff=0.9):
    print('Detecting contours and filtering of color:', color)
    import cv2 as cv
    import numpy as np
    img_name = 'mask_'+color+'.png'
    img = cv.imread(img_name, 0)

    # Find contours
    contours, hierarchy = cv.findContours(img, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)

    # Determine what contour area is the biggest
    contour_areas = []
    try:
        for i in range(len(contours)):
            contour_areas.append(cv.contourArea(contours[i]))
        max_area = max(contour_areas)
    except AssertionError as error:
        print(error)
        print('The linux_interaction() function was not executed')
        max_area = 0

    # Make a list of contours that are bricks, filtered by area of biggest blob
    brick_contours = []

    if max_area < 40000 or 500000 < max_area:
        print('Could not find bricks of color:', color)
    else:
        for i in range(len(contours)):
            # Only bricks that are >90% (adjustable) of the size of the largest blob is accepted
            if cv.contourArea(contours[i]) > max_area * area_cutoff:
              brick_contours.append(contours[i])
        print('Found', len(brick_contours), 'of color', color)

    # Fill the contours into an empty image and save
    mask = np.zeros(img.shape, dtype=np.uint8)
    cv.fillPoly(mask, brick_contours, 255)
    img_out_name = 'filtered_' + color + '.png'
    cv.imwrite(img_out_name, mask)

    return mask

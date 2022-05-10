def center_angle(img):
    import cv2 as cv
    from math import atan2, cos, sin, sqrt, pi
    import numpy as np

    # Find all the contours in the thresholded image
    contours, _ = cv.findContours(img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    angles = []

    for i, c in enumerate(contours):
        # cv.minAreaRect returns:
        # (center(x, y), (width, height), angle of rotation) = cv2.minAreaRect(c)
        rect = cv.minAreaRect(c)
        box = cv.boxPoints(rect)
        box = np.int0(box)

        # Retrieve the key parameters of the rotated bounding box
        center = (int(rect[0][0]), int(rect[0][1]))
        width = int(rect[1][0])
        height = int(rect[1][1])
        angle = int(rect[2])
        angles.append([center, np.deg2rad(angle)])

        # This part is for image, only used when creating the script to test.
        # if width < height:
        #     angle = 90 - angle
        # else:
        #     angle = -angle
        # label = "  Rotation Angle: " + str(np.rad2deg(angle)) + " degrees"
        # textbox = cv.rectangle(img, (center[0] - 35, center[1] - 25),
        #                        (center[0] + 295, center[1] + 10), (255, 255, 255), -1)
        # cv.putText(img, label, (center[0] - 50, center[1]),
        #            cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 1, cv.LINE_AA)
        # cv.drawContours(img, [box], 0, (0, 0, 255), 2)
        # cv.imwrite("min_area_rec_output.jpg", img)
    return angles
    #cv.imshow('Output Image', img)
    #cv.destroyAllWindows()
    #print(datapunkt)

    # Save the output image to the current directory

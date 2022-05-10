import csv
from object_detection import obj_detect  # Object detection
from contour_detect import contour_detect  # Object filtration
from image_homography import img_homography  # Image homography
from center_angle import center_angle  # Brick localization and rotation-finder

# This bit disables hardware acceleration for the webcam
# Without this, webcam takes >5 min to open
# Must be done before importing OpenCV
import os
os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"
import cv2 as cv

########### Adjustable parameters: #############
qr_irl_size = 98  # side to side, in mm
src_x = 443-qr_irl_size  # width in mm between centre of QR codes. Corner-to-corner distance minus qr size
src_y = 442-qr_irl_size  # height in mm between centre of QR codes
scale = 10  # Desired scale in warped image, in pixels per mm
colors = ['blue', 'green', 'yellow', 'orange', 'white']  # Colors of bricks present
percent_max_size = 0.8  # The filtering limit of contour areas, in relation to biggest area. Removes small objects.
img_path = ""  # File path of image
img_name = 'cam_live.jpg'  # Name of input image 'cam_live.jpg'
webcam_enable = False  # True: image is gathered from webcam, False: existing image can be used (testing)

if webcam_enable:
    # Webcam code
    vid = cv.VideoCapture(1, cv.CAP_MSMF)
    vid.set(cv.CAP_PROP_FRAME_WIDTH, 1920)
    vid.set(cv.CAP_PROP_FRAME_HEIGHT, 1080)
    while (True):
        # Capture the video frame by frame
        ret, frame = vid.read()
        # Display the video feed
        cv.imshow('frame', frame)
        #  'q' is set as image capture / quitting button
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
    cv.imwrite(img_path+'cam_live.jpg', frame)  # Saves most recent frame as image
    vid.release()  # After the loop release the cap object
    cv.destroyAllWindows()  # Destroy all the windows

# Load image and remove perspective distortion via image homography
input_img = cv.imread(img_path+img_name, cv.IMREAD_ANYCOLOR)
img_warp = img_homography(input_img, src_x, src_y, scale, qr_irl_size)  # Call custom image homography function
cv.imwrite('qr_img_warped.png', img_warp)  # Image with qr codes in corners

# Detect objects by InRange thresholding of HSV color spaces.
# Variables need adjusting depending on lighting and camera setup
# Saves an image of each color
obj_detect(img_warp)

# Filter detected objects based on size
bricks_data = []
for i in range(len(colors)):
    # Filters the images and removes noise by size of the largest object. Takes one color at a time
    filtered = contour_detect(colors[i], percent_max_size)
    # Finds brick coordinates and angles in radians
    brick_placement = center_angle(filtered)
    # For each brick, extract brick data and add color, add to final data array
    # Coordinates from top left corner, x,y, in mm
    for j in range(len(brick_placement)):
        brick_x = brick_placement[j][0][0] / scale  # x coordinate in mm
        brick_y = brick_placement[j][0][1] / scale  # y coordinate in mm
        rotation = brick_placement[j][1] # Rotation in radians
        bricks_data.append([brick_x, brick_y, rotation, colors[i], 0])  # Collects data in an array

# Print gathered data
header = ['x [mm]', 'y [mm]', 'rotation [rad]', 'color', '0']
print('Bricks detected at: ', header)
print(bricks_data)

# Write gathered data to .csv file
with open('bricks_data.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(bricks_data)
def img_homography(img, dist_x, dist_y, scale, qr_irl_size):
    import cv2 as cv
    import numpy as np

    # Detect QR codes
    det = cv.QRCodeDetector()
    retval, decoded_info, points, straight_qrcode = det.detectAndDecodeMulti(img)
    print('Detected QR codes:', decoded_info)

    # Get QR centre coordinates by taking the average x and y coordinates for corners of each QR-code
    # Store QR code info, average x-value, average y-value
    qr_point_coord = np.zeros([4, 3])
    for i in range(len(decoded_info)):
        qr_point_coord[i, 0] = int(str(decoded_info[i])[-1])  # Get QR code information, e.g. "qr_1", and extract "1"
        for j in range(2):
            qr_point_coord[i, j+1] = np.average(points[i, 0:4, j])  # Get average x- or y-value for QR-code

    # Sorts QR codes in order 1-2-3-4
    qr_point_coord = qr_point_coord[qr_point_coord[:, 0].argsort()]
    # Makes dst matrix for homography based on qr code centre coords
    dst = np.array([qr_point_coord[3, 1:3], qr_point_coord[0, 1:3], qr_point_coord[1, 1:3], qr_point_coord[2, 1:3]])

    # Initializes src matrix for resulting homographied image
    src_x = dist_x * scale
    src_y = dist_y * scale
    src = np.array([[0, src_y], [0, 0], [src_x, 0], [src_x, src_y]])

    # Increases size of output image to include qr codes
    qr_size = qr_irl_size * scale
    src = src + round(qr_size/2, 0)

    # Finds homography
    H, _ = cv.findHomography(dst, src)

    # Warps image and returns an image including QR codes '
    # and an image exclusively inside qr codes (unused)
    img_warp = cv.warpPerspective(img, H, (src_x+qr_size, src_y+qr_size))
    # img_warp_noqr = img_warp[qr_size:-qr_size, qr_size:-qr_size]
    return img_warp  #, img_warp_noqr
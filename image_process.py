import cv2
import numpy as np

import __conf__

mask = None


def init():
    # create crop mask with our transformation
    global mask
    mask = np.zeros((480, 640), dtype=np.uint8)
    mask[:] = 255
    mask = transform_image(mask)
    cv2.erode(mask, None, dst=mask, iterations=2)
    mask = crop_and_resize_image(mask)


def transform_image(img):
    w, h = 640, 480

    # transform image
    ow, oh, wi = __conf__.tx, __conf__.ty, __conf__.wi
    pts1 = np.float32(__conf__.orig_sqre)
    pts2 = np.float32([[ow, oh + wi], [ow + wi, oh + wi], [ow + wi, oh], [ow, oh]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    img = cv2.warpPerspective(img, matrix, (w, h))

    return img


def crop_and_resize_image(image):
    img = cv2.resize(image, (160, 120))
    return img[60:120, 0:160]


def grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def threshold_image(image):
    global mask
    img = cv2.medianBlur(image, 5)
    img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                cv2.THRESH_BINARY_INV, 11, 4)

    img = cv2.bitwise_and(img, mask)

    return img


def generate_preview(images):

    img = np.vstack(images)
    # img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

    cv2.line(img, (80, 120), (80, 180), (255, 0, 255), 1)

    for i in range(1, len(images)+1):
        if not i == 1:
            cv2.line(img, (0, 60*i), (160, 60*i), (255, 255, 255), 1)

    cv2.putText(img, 'original', (1, 13), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 0), 1, cv2.LINE_AA)
    cv2.putText(img, 'transformed', (1, 13+120), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 0), 1, cv2.LINE_AA)
    cv2.putText(img, 'threshold', (1, 13+120+60), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 0), 1, cv2.LINE_AA)
    cv2.putText(img, 'threshold & match', (1, 13+120+60+60), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 0), 1, cv2.LINE_AA)
    cv2.putText(img, 'best curve match', (1, 13+120+60+60+60), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 0), 1, cv2.LINE_AA)

    return img

import os
import cv2
import numpy as np
from matplotlib import pyplot as plt
from commons import *


def thinness(cnt):
    area = cv2.contourArea(cnt)
    perimeter = cv2.arcLength(cnt, True)
    return perimeter ** 2 / float(area)


def extent(cnt):
    area = cv2.contourArea(cnt)
    rect = cv2.minAreaRect(cnt)
    ((x, y), (w, h), r) = rect
    rect_area = w * h
    return area / float(rect_area)


def dist(x, y):
    return np.sqrt((x[0] - y[0]) ** 2 + (x[1] - y[1]) ** 2)


def corners(kps):
    if len(kps) == 0:
        return 0

    points = []
    for kp in kps:
        points.append(kp.pt)
    points.sort()

    eps = 30
    unique_points = [points[0]]
    for i in range(1, len(points)):
        p = points[i]
        unique_flag = True
        for j in unique_points:
            if dist(p, j) < eps:
                unique_flag = False
        if unique_flag:
            unique_points.append(p)

    return len(unique_points)


def fmt_float(x):
    return '{0:.3f}'.format(x)


def process_image(img_file, multi=False):
    features = {}

    img = cv2.imread(img_file)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # kernel = np.ones((5,5),np.float32)/25
    # img = cv2.filter2D(img, -1, kernel)

    ret, thresh = cv2.threshold(img, 127, 255, 0)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contour = contours[1]

    features['Thinness'] = fmt_float(thinness(contour))
    features['Extent'] = fmt_float(extent(contour))

    sift = cv2.SIFT()
    kps = sift.detect(img, None)
    features['Corners'] = str(corners(kps))

    # cv2.imshow('contour', cv2.drawKeypoints(img, kps))
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # img_gray = np.float32(img_gray)
    # dst = cv2.cornerHarris(img_gray,2,3,0.04)
    # # result is dilated for marking the corners, not important
    # dst = cv2.dilate(dst,None)
    # # Threshold for an optimal value, it may vary depending on the image.
    # img[dst>0.01*dst.max()]=[0,0,255]
    # cv2.imshow('dst',img)
    # if cv2.waitKey(0) & 0xff == 27:
    #     cv2.destroyAllWindows()
    # plt.imshow(img),plt.show()

    return features


def extract(input_dir, output_file):
    f_output = open(output_file, 'w')
    f_output.write(','.join(feature_list) + ',index,label\n')

    error_list = []
    for (index, input_file) in enumerate(os.listdir(input_dir)):
        if not input_file.endswith('.png'):
            continue
        print 'extracting feature from {0}'.format(input_file)
        label = input_file.split('.')[0].split('_')[1]
        try:
            features = process_image(os.path.join(input_dir, input_file))
        except:
            error_list.append(input_file)
            features = ['FAIL']
        feature_values = [features[f] for f in feature_list] + [str(index+1), label]
        f_output.write(','.join(feature_values) + '\n')

    print '\nCompleted.\nFailed:\n'
    for e in error_list:
        print e
    f_output.close()


if __name__ == '__main__':
    for shape in shape_list:
        extract(train_image_dir+'\\'+shape, os.path.join(train_feature_dir, 'train_feature_{0}.csv'.format(shape)))

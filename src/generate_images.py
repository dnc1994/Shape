import os
import random
import time
import copy
import cv2
import numpy as np
from matplotlib import pyplot as plt
from commons import *

SMALL_SIZE = 0
BIG_SIZE = 1
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


def create_img():
    img = np.ones((800, 800, 3), np.uint8)
    img[:,:] = (255, 255, 255)
    return img


def sizable_radius(size):
    if size == SMALL_SIZE:
        return random.randrange(100, 150)
    elif size == BIG_SIZE:
        return random.randrange(150, 200)
    else:
        raise Exception('Unknown size.')


def safe_rand_center(width_span, height_span, width=800, height=800):
    margin = max(int(width_span * 0.63), int(height_span * 0.63))
    center_x = random.randrange(margin + width_span, width - margin - width_span)
    center_y = random.randrange(margin + height_span, height - margin - height_span)
    return center_x, center_y


def draw_circle(img, size):
    radius = sizable_radius(size)
    center_x, center_y = safe_rand_center(radius, radius)
    cv2.circle(img, (center_x, center_y), radius, BLACK, 3)
    return img


def draw_ellipse(img, size):
    long_radius = sizable_radius(size)
    short_radius = int(long_radius * random.uniform(0.5, 0.8))
    center_x, center_y = safe_rand_center(long_radius, long_radius)
    cv2.ellipse(img, (center_x, center_y), (long_radius, short_radius), 0, 0, 360, BLACK, 3)
    return img


def draw_triangle(img, size):
    long_radius = sizable_radius(size)
    short_radius = int(long_radius * random.uniform(0.5, 0.8))
    center_x, center_y = safe_rand_center(long_radius, short_radius)
    lb_pt = [random.uniform(center_x - long_radius, center_x - long_radius + int(0.63 * long_radius)), center_y + short_radius]
    rb_pt = [random.uniform(center_x + long_radius - int(0.63 * long_radius), center_x + long_radius), center_y + short_radius]
    top_pt = [random.uniform(center_x - long_radius, center_x + long_radius), center_y - short_radius]
    pts = np.array([lb_pt, rb_pt, top_pt], np.int32)
    pts = pts.reshape((-1, 1, 2))
    cv2.polylines(img, [pts], True, BLACK, 3)
    return img


def draw_rectangle(img, size):
    long_radius = sizable_radius(size)
    short_radius = int(long_radius * random.uniform(0.5, 0.8))
    center_x, center_y = safe_rand_center(long_radius, short_radius)
    cv2.rectangle(img, (center_x - long_radius, center_y - short_radius), (center_x + long_radius, center_y + short_radius), BLACK, 3)
    return img


def draw_square(img, size):
    radius = sizable_radius(size)
    center_x, center_y = safe_rand_center(radius, radius)
    cv2.rectangle(img, (center_x - radius, center_y - radius), (center_x + radius, center_y + radius), BLACK, 3)
    return img


shape_routes = {
    'Circle': draw_circle,
    'Ellipse': draw_ellipse,
    'Triangle': draw_triangle,
    'Rectangle': draw_rectangle,
    'Square': draw_square,
}


def distort(img, factor=0.1, prob_chg_dir=0.1):
    A = img.shape[0] / 4.0
    w = 2.0 / img.shape[1]
    shift = lambda x: A * np.sin(2.0 * np.pi * x * w) / (1 / factor)
    k, dir = 0, 1
    for i in range(img.shape[0]):
        if random.random() < prob_chg_dir:
            dir = -dir
        k += dir
        img[:, i] = np.roll(img[:,i], int(shift(k)))

    A = img.shape[1] / 4.0
    w = 2.0 / img.shape[0]
    shift = lambda x: A * np.sin(2.0 * np.pi * x * w) / (1 / factor)
    k, dir = 0, 1
    for i in range(img.shape[0]):
        if random.random() < prob_chg_dir:
            dir = -dir
        k += dir
        img[i, :] = np.roll(img[i,:], int(shift(k)))
    return img


def rotate(img, degree):
    rows, cols = img.shape[:2]
    R = cv2.getRotationMatrix2D((cols / 2, rows / 2), degree, 1)
    dst = cv2.warpAffine(img, R, (cols, rows), borderValue = WHITE)
    return dst


def draw_one(shape, size, factor, degree):
    img = create_img()
    img = shape_routes[shape](img, size)
    img = distort(img, factor)
    img = rotate(img, degree)
    # cv2.imshow('test', img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    # exit(0)
    return img


def draw_many(shape, num_per_set, save_path):
    global count
    global rd
    for i in range(num_per_set):
        size = random.choice([0, 1])
        factor = random.uniform(0.1, 0.2)
        degree = rd.next()
        count += 1
        print 'Drawing #{0} {1} with size = {2}, factor = {3}, degree = {4}'.format(count, shape, size, factor, degree)
        img = draw_one(shape, size, factor, degree)
        filename = '{0:04d}_{1}.png'.format(count, shape)
        filepath = os.path.join(save_path+'\\'+shape, filename)
        cv2.imwrite(filepath, img)


def generate_data(num_per_set, split_ratio=0.9):
    global count
    delim = int(num_per_set * split_ratio)

    for shape in shape_list:
        count = 0
        draw_many(shape, delim, train_image_dir)
        draw_many(shape, num_per_set - delim, test_image_dir)


if __name__ == '__main__':
    random.seed(time.time())
    global rd
    rd = RandomDegree()
    generate_data(200)

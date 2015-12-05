import os
import random
import numpy as np
from PIL import Image, ImageDraw
from commons import *
from configs import *


def write_to_file(img, ext, filename):
    filepath = os.path.join(train_image_dir, filename)
    with open(filepath, 'wb') as f:
        img.save(f, ext)


def draw_circle(img):
    # mode must be RGBA to ensure transparency
    draw = ImageDraw.Draw(img, 'RGBA')
    limit = min(img.width, img.height)
    radius = random.randrange(50, limit // 6)
    center_x = random.randrange(0+radius, img.width-radius)
    center_y = random.randrange(0+radius, img.height-radius)
    x1, x2 = center_x - radius, center_x + radius
    y1, y2 = center_y - radius, center_y + radius
    draw.ellipse((x1, y1, x2, y2), outline='black')


def draw_ellipse():
    pass


def draw_square(img):
    draw = ImageDraw.Draw(img, 'RGBA')
    limit = min(img.width, img.height)
    side = random.randrange(50, limit // 3)
    pass


def draw_rectangle():
    pass


def draw_triangle():
    pass


def draw_trapezoid():
    pass


SHAPE_ROUTES = {
    'circle': draw_circle,
    'ellipse': draw_ellipse,
    'square': draw_square,
    'rectangle': draw_rectangle,
    'triangle': draw_triangle,
    'trapezoid': draw_trapezoid
}

# SHAPES = SHAPE_ROUTES.keys()
SHAPES = ['circle']


def pad_index(x):
    x = str(x)
    return '0' * (4 - len(x)) + x


def draw_shape(img, shape, df):
    assert shape in SHAPES
    assert df > 0 and df < 1.0
    SHAPE_ROUTES[shape](img)


def draw_one(index, res=(1000,1000), bgcolor=(255,255,255)):
    img = Image.new('RGB', res, bgcolor)
    shape = random.choice(SHAPES)
    df = random.uniform(0.1, 0.4)
    draw_shape(img, shape, df)

    filename = '{0}_{1}.png'.format(shape, pad_index(index))
    write_to_file(img, 'PNG', filename)


# def draw_many(num_drawings, max_shapes):
#
#
#     for i in range(num_drawings):
#         num_shapes = random.randrange(1, max_shapes+1)
#         draw_one(num_shapes)


def main():
    for i in range(10):
        draw_one(i)


if __name__ == '__main__':
    main()
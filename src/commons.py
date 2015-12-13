import random


shape_list = ['Circle', 'Ellipse', 'Triangle', 'Square', 'Rectangle']

feature_list = [
    'Thinness',
    'Extent',
    'Corners'
]

devel_image_dir = 'C:\\Home\\Projects\\Shape\\data\\devel_image'
train_image_dir = 'C:\\Home\\Projects\\Shape\\data\\train_image'
train_feature_dir = 'C:\\Home\\Projects\\Shape\\data\\train_feature'
test_image_dir = 'C:\\Home\\Projects\\Shape\\data\\test_image'
sketch_image_dir = 'C:\\Home\\Projects\\Shape\\data\\sketch_image'


class RandomDegree(object):
    def __init__(self):
        self.counter = 0
        self.sequence = range(360)
        random.shuffle(self.sequence)

    def next(self):
        val = self.sequence[self.counter]
        self.counter += 1
        if self.counter == len(self.sequence):
            random.shuffle(self.sequence)
            self.counter = 0
        return val

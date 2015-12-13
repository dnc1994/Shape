import sys
import os
from puzzy import fset
from puzzy.inferencer import Inferencer
from extract_features import process_image
from commons import *


class ShapeRecognizer(object):
    def __init__(self):
        fsets = {}
        rules = {}

        fsets['Circle_Like_Thinness'] = fset.Trapezoid('Circle_Like_Thinness', (13.99, 0), (15.07, 1), (15.44, 1), (16.39, 0))
        fsets['Square_Like_Thinness'] = fset.Trapezoid('Square_Like_Thinness', (15.34, 0), (17.78, 1), (18.65, 1), (21.34, 0))
        fsets['Triangle_Like_Extent'] = fset.Triangle('Triangle_Like_Extent', (0.4828, 0), (0.5170, 1), (0.5512, 0))
        fsets['Ellipse_Like_Extent'] = fset.Trapezoid('Ellipse_Like_Extent', (0.7450, 0), (0.7740, 1), (0.790, 1), (0.8180, 0))
        fsets['Rectangle_Like_Extent'] = fset.RightSkewTrapezoid('Rectangle_Like_Extent', (0.795, 0), (0.9377, 1), (1, 0))


        rules['Circle'] = 'IF Thinness IS Circle_Like_Thinness AND Extent IS Ellipse_Like_Extent THEN Shape IS Circle'
        rules['Ellipse'] = 'IF Thinness IS NOT Circle_Like_Thinness AND Extent IS Ellipse_Like_Extent THEN Shape IS Ellipse'
        rules['Triangle'] = 'IF Extent IS Triangle_Like_Extent THEN Shape IS Triangle'
        rules['Square'] = 'IF Thinness IS Square_Like_Thinness AND Extent IS Rectangle_Like_Extent THEN Shape IS Square'
        rules['Rectangle'] = 'IF Thinness IS NOT Square_Like_Thinness AND Extent IS Rectangle_Like_Extent THEN Shape IS Rectangle'

        self.inferencer = Inferencer()
        self.inferencer.add_fsets(fsets.values())
        self.inferencer.add_rules(rules.values())

    def recognize(self, img_file):
        inputs = process_image(img_file)
        result = self.inferencer.evaluate(inputs)
        return result['Shape']


def main():
    img_file = sys.argv[1]
    recognizer = ShapeRecognizer()
    result = recognizer.recognize(img_file)
    print result


def test(input_dir):
    results = []
    for img in os.listdir(input_dir):
        img_file = os.path.join(input_dir, img)
        print img
        recognizer = ShapeRecognizer()
        result = recognizer.recognize(img_file)
        print result
        print
        results.append((img, result))
    for result in results:
        print result

if __name__ == '__main__':
    # test(train_image_dir)
    main()

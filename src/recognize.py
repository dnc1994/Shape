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

        fsets['No_Corners'] = fset.LeftSkewTrapezoid('No_Corners', (0, 0), (2, 1), (4, 0))
        fsets['Circle_Like_Thinness'] = fset.Triangle('Circle_Like_Thinness', (12.5, 0), (14, 1), (15, 0))
        fsets['Square_Like_Thinness'] = fset.Triangle('Square_Like_Thinness', (15, 0), (16, 1), (20, 0))
        fsets['Triangle_Like_Extent'] = fset.Trapezoid('Triangle_Like_Extent', (0.4, 0), (0.45, 1), (0.55, 1), (0.6, 0))
        fsets['Ellipse_Like_Extent'] = fset.Triangle('Ellipse_Like_Extent', (0.7, 0), (0.8, 1), (0.85, 0))
        fsets['Rectangle_Like_Extent'] = fset.RightSkewTrapezoid('Rectangle_Like_Extent', (0.85, 0), (0.95, 1), (1, 0))


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

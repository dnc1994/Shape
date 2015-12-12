import sys
import os
from puzzy import fset
from puzzy.inferencer import Inferencer
from extract_features import process_image
from commons import *


def recognize_image(inferencer, img_file):
    inputs = process_image(img_file)
    result = inferencer.evaluate(inputs)
    return result['Shape']


def init_inferencer():
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

    inferencer = Inferencer()
    inferencer.add_fsets(fsets.values())
    inferencer.add_rules(rules.values())

    return inferencer


def main():
    img_file = sys.argv[1]

    inferencer = init_inferencer()
    result = recognize_image(inferencer, img_file)

    print result


def test():
    test_dir = train_image_dir + '\\S'
    results = []
    for img in os.listdir(test_dir):
        img_file = os.path.join(test_dir, img)
        print img
        inferencer = init_inferencer()
        result = recognize_image(inferencer, img_file)
        print result
        print
        results.append((img, result))

    for result in results:
        print result

if __name__ == '__main__':
    test()
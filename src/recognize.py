import sys
import os
from puzzy import fset
from puzzy.inferencer import Inferencer
from extract_features import process_image
from commons import *


class ShapeRecognizer(object):
    def __init__(self, rule_base='rule_base.txt'):
        fsets = {}
        rules = {}

        try:
            with open(rule_base, 'r') as f:
                while True:
                    line = f.readline()
                    if not line or not line.strip('\n'):
                        break
                    line = line.strip('\n')
                    name, shape, pts = line.split('\t')
                    pts = [pt.split(',') for pt in pts.split(' ')]
                    pts = [(float(x), float(y)) for (x, y) in pts]
                    fsets[name] = fset_routes[shape](name, *pts)

                while True:
                    line = f.readline()
                    if not line:
                        break
                    name, rule = line.strip('\n').split('\t')
                    rules[name] = rule
        except:
            raise

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
    test(sketch_image_dir)
    # main()

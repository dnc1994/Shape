import fset
import rule
from inferencer import Inferencer

__author__ = 'Linghao Zhang'
__version__ = '0.1.0'


def main():
    A1 = fset.LeftSkewTrapezoid('A1', (0, 0), (1, 1), (4, 0))
    A2 = fset.Triangle('A2', (2, 0), (5, 1), (8, 0))
    A3 = fset.RightSkewTrapezoid('A3', (6, 0), (8, 1), (10, 0))

    rule1 = 'IF x IS A1 THEN y IS B1'
    rule2 = 'IF x IS A2 THEN y IS B2'
    rule3 = 'IF x IS A3 THEN y IS B3'

    fsets = [A1, A2, A3]
    rules = [rule1, rule2, rule3]

    inferencer = Inferencer()
    inferencer.add_fsets(fsets)
    inferencer.add_rules(rules)

    input_test = {'x': 7}

    print inferencer.evaluate(input_test)


if __name__ == '__main__':
    main()

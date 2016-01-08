from commons import *
import os
import pandas

qs = [0, 0.1, 0.25, 0.5, 0.75, 0.9, 1]


def simple_stats(input_file, attr_list):
    print 'Analyzing {0}'.format(input_file)
    filepath = os.path.join(train_feature_dir, input_file)
    csv_df = pandas.DataFrame(pandas.read_csv(filepath))
    stats = {}
    for attr in attr_list:
        print 'For column {0}'.format(attr)
        vs = {}
        for q in qs:
            v = csv_df[attr].quantile(q)
            vs[q] = v
            print 'Percentile {0}: {1}'.format(q, v)
        vs[-0.05] = vs[0.1] - 2 * (vs[0.25] - vs[0.1])
        vs[1.05] = vs[0.9] + 2 * (vs[0.9] - vs[0.75])
        print 'Percentile {0}: {1}'.format(-0.05, vs[-0.05])
        print 'Percentile {0}: {1}'.format(1.05, vs[1.05])
        stats[attr] = vs
    return stats


if __name__ == '__main__':
    simple_stats('train_feature_Circle.csv', ['Thinness'])
    simple_stats('train_feature_Ellipse.csv', ['Extent'])
    simple_stats('train_feature_Rectangle.csv', ['Extent'])
    simple_stats('train_feature_Square.csv', ['Thinness'])
    simple_stats('train_feature_Triangle.csv', ['Extent'])

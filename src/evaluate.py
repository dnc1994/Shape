import os
import copy
from recognize import ShapeRecognizer
from commons import *


def eval_dataset(input_dir, output_file, need_latex=False):
    recognizer = ShapeRecognizer()

    confusion_matrix = {}
    for shape in shape_list:
        confusion_matrix[shape] = {}
        for label in shape_list:
            confusion_matrix[shape][label] = 0
    error_list = []

    for filename in os.listdir(input_dir):
        if not filename.endswith('.png'):
            continue
        index, label = filename.split('.')[0].split('_')
        input_file = os.path.join(input_dir, filename)
        recognized_label = recognizer.recognize(input_file)
        label = label.title()
        recognized_label = recognized_label.title()
        if label != recognized_label:
            error_list.append((filename, label, recognized_label))
        confusion_matrix[label][recognized_label] = 1 + confusion_matrix[label].get(recognized_label, 0)

    confusion_matrix_percent = copy.deepcopy(confusion_matrix)
    for shape in shape_list:
        count = sum(confusion_matrix_percent[shape].values())
        for key in confusion_matrix_percent[shape].keys():
            confusion_matrix_percent[shape][key] /= float(count)

    with open(output_file + '.csv', 'w') as f:
        f.write('Confusion Matrix\n')
        f.write(','.join([' '] + shape_list) + '\n')
        for shape in shape_list:
            row = [confusion_matrix_percent[shape][label] for label in shape_list]
            line = ','.join([shape] + ['{0:.2f}'.format(val) for val in row])
            f.write(line + '\n')
        f.write('\n')
        f.write('Error List\n')
        f.write(','.join(['File', 'Label', 'Recognized']) + '\n')
        for (filename, label, recognized_label) in error_list:
            line = ','.join([filename, label, recognized_label])
            f.write(line + '\n')

    if need_latex:
        with open(output_file + '_table.tex', 'w') as f:
            pass


if __name__ == '__main__':
    eval_dataset(sketch_image_dir, 'C:\\Home\\Projects\\Shape\\data\\eval_test_image')
    # eval_dataset(test_image_dir, 'C:\\Home\\Projects\\Shape\\data\\eval_test_image', True)
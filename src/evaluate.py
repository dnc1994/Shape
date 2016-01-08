import os
import copy
from recognize import ShapeRecognizer
from extract_features import process_image
from commons import *


def eval_dataset(input_dir, output_file, need_latex=True):
    recognizer = ShapeRecognizer()

    confusion_matrix = {}
    for shape in shape_list:
        confusion_matrix[shape] = {}
        for label in shape_list:
            confusion_matrix[shape][label] = 0
    error_list = []

    for (root, subdirs, filenames) in os.walk(input_dir):
        for filename in filenames:
            if not filename.endswith('.png'):
                continue
            print 'Recognizing {0}'.format(filename)
            index, label = filename.split('.')[0].split('_')
            input_file = os.path.join(root, filename)
            try:
                recognized_label = recognizer.recognize(input_file)
            except:
                recognized_label = 'FAIL'
            label = label.title()
            recognized_label = recognized_label.title()
            if label != recognized_label:
                feature_str = str(process_image(input_file))
                error_list.append((filename, label, recognized_label, feature_str))
            confusion_matrix[label][recognized_label] = 1 + confusion_matrix[label].get(recognized_label, 0)

    confusion_matrix_percent = copy.deepcopy(confusion_matrix)
    for shape in shape_list:
        count = sum(confusion_matrix_percent[shape].values())
        if count == 0:
            continue
        for key in confusion_matrix_percent[shape].keys():
            confusion_matrix_percent[shape][key] /= float(count)

    latex_lines = []

    with open(output_file + '.csv', 'w') as f:
        f.write('Confusion Matrix\n')
        f.write(','.join([' '] + shape_list) + '\n')
        latex_lines.append(' & '.join([r'\backslashbox{Label}{Recognized}'] + shape_list) + ' \\\\ \\hline\n')
        for shape in shape_list:
            row = [confusion_matrix_percent[shape][label] for label in shape_list]
            line = ','.join([shape] + ['{0:.2f}'.format(val) for val in row])
            latex_lines.append(' & '.join([shape] + ['{0:.2f}'.format(val) for val in row]) + ' \\\\ \\hline\n')
            f.write(line + '\n')
        f.write('\n')
        f.write('Error List\n')
        f.write(','.join(['File', 'Label', 'Recognized', 'Features']) + '\n')
        for (filename, label, recognized_label, feature_str) in error_list:
            line = ','.join([filename, label, recognized_label, feature_str])
            f.write(line + '\n')

    if need_latex:
        with open(output_file + '_table.tex', 'w') as f:
            f.writelines(latex_lines)


if __name__ == '__main__':
    eval_dataset(devel_image_dir, 'C:\\Home\\Projects\\Shape\\data\\eval_devel_image')
    eval_dataset(test_image_dir, 'C:\\Home\\Projects\\Shape\\data\\eval_test_image')
    # eval_dataset(sketch_image_dir, 'C:\\Home\\Projects\\Shape\\data\\eval_sketch_image')

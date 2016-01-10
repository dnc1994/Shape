# Shape

Simple geometric shape recognition based on fuzzy inference.

Final project for Introduction to Artificial Intelligence course @ Fudan University.

Read report for implementation details and experimental results.

## Author
[Linghao Zhang](https://github.com/dnc1994)

## Workflow

0. Experiment with standards shapes to derive the basic rules and framework of the system.
1. Generate random images and introduce noise by distorting and rotating.
2. Split images into training set, development set and testing set.
3. Extract features using OpenCV.
4. Use simple statistics from traning set to determine the shape and boundary of each fuzzy sets.
5. Write fuzzy sets and rules into a separate rule base file.
6. Implement a simplified Sugeno-style inferencer
7. Tune parameters using development set.
8. Evaluate performance on testing set.
9. Ask different persons to drawn sketches as additional test images

## Overview

* `src/puzzy/fset.py` Define different types of fuzzy sets (representation and membership function).
* `src/puzzy/inferencer.py` Implement inference engine.
* `src/puzzy/rule.py` Implement rule representation and parsing.
* `src/analyze_features.py` Analyze features using simple statistics.
* `src/evaluate.py` Evaluate performance on a given dataset.
* `src/extract_features.py` Extract features from a given dataset.
* `src/generate_images.py` Generate random noisy images.
* `src/recognize.py` Interface for recognition.
* `src/rule_base.txt` Rule base for the system.
* `data/sample/` Sample images used in development and evaluation.
# Imports
from matplotlib import pyplot as plt
import os
from sklearn.metrics import confusion_matrix
import itertools
import numpy as np


def acc_bar_chart(title, desc, baseline, acc_scores, labels, output_file):
    """ Graph the given accuracies against each other and baseline """
    plt.title(title)
    plt.bar(range(1, len(acc_scores) + 1), acc_scores, tick_label=labels)
    plt.axhline(baseline, color='r', label="baseline")
    plt.savefig(output_file)
    plt.clf()


def plot_confusion_matrix(gold, preds, output_file):
    """ Creates and plots a confusion matrix for the predictions

        CITATION: THIS CODE HEAVILY ADAPTED FROM SCIKITLEARN:
        http://scikit-learn.org/stable/auto_examples/model_selection/plot_confusion_matrix.html
    """
    # Create Mapping to Emojis for Display TODO
    # us_map_file = os.path.join('..', 'Data', 'mappings', 'us_mapping.txt')
    # emoji_path = os.path.join('..', 'Data', 'mappings', 'emojis')
    # us_map = {}
    # with open(us_map_file, 'r') as f:
    #     for line in f:
    #         toks = line.split()
    #         em_file = os.path.join(emoji_path, toks[2][1:-1] + '.png')
    #         us_map[int(toks[0])] = plt.imread(em_file)

    # Map the preds and gold to the emojis (for display)
    # TODO
    classes = range(10)
    n_clss = len(classes)

    # Plot the confusion matrix
    cnf_mat = confusion_matrix(gold, preds, labels=classes)

    plt.imshow(cnf_mat, interpolation='nearest', cmap=plt.cm.Blues)
    plt.colorbar()

    fmt = 'd'
    thresh = cnf_mat.max() / 2.
    for i, j in itertools.product(range(cnf_mat.shape[0]),
                                  range(cnf_mat.shape[1])):
        plt.text(j, i, format(cnf_mat[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cnf_mat[i, j] > thresh else "black")

    ticks = np.arange(n_clss)
    plt.xticks(ticks, classes)
    plt.yticks(ticks, classes)

    plt.title('Emoji Confusion Matrix')
    plt.ylabel('Gold Label')
    plt.xlabel('Predicted Label')

    plt.show()

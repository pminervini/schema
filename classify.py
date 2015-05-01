#!/usr/bin/python -uB
# -*- coding: utf-8 -*-

# ./Classify.py --experiment=~/models/aifb_d2s_010_50_20150109-164102_0.pkl --classes=data/aifb/d2s/aifb_d2s_group_affiliates.pkl

import numpy as np

import sklearn.preprocessing as preprocessing

import sklearn.datasets as datasets
import sklearn.cross_validation as cross_validation
import sklearn.grid_search as grid_search
import sklearn.metrics as metrics
import sklearn.svm as svm

import data.util as util
import persistence.layer as persistence

import cPickle as pickle

import sys
import getopt
import logging

normalize = False
iterations = 1

def main(argv):
    experiment_id, classes_pkl, use_rbf = None, None, False

    conf = util.configuration()

    # Parse arguments
    try:
        opts, args = getopt.getopt(argv, 'h', ['experiment=', 'classes=', 'rbf'])
    except getopt.GetoptError:
        logging.warn('Usage: %s [-h] [--experiment=<id>] [--classes=<classes.pkl>] [--rbf]' % (sys.argv[0]))
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            logging.info('Usage: %s [-h] [--experiment=<id>] [--classes=<classes.pkl>] [--rbf]' % (sys.argv[0]))
            logging.info('\t--experiment=<id> (default: %s)' % (experiment_id))
            logging.info('\t--classes=<classes.pkl> (default: %s)' % (classes_pkl))
            logging.info('\t--rbf (Consider using the RBF kernel during hyperparameters selection)')
            return

        if opt == '--experiment':
            experiment_id = arg
        if opt == '--classes':
            classes_pkl = arg
        if opt == '--rbf':
            use_rbf = True

    layer = persistence.PickleLayer(dir=conf.get('Persistence', 'path'))

    # Get the dict containing the details of the experiment (including the learned parameters)
    experiment = layer.get(experiment_id)

    # Get a { class: set([ elements ]) } dict
    classes_dict = pickle.load(open(classes_pkl, 'rb'))

    # If a class has less than 10 elements, remove it
    for _class in classes_dict.keys():
        if len(classes_dict[_class]) < 10:
            logging.info('Removing class %s' % _class)
            del classes_dict[_class]

    # Get the best parameters learned so far
    best = experiment['best_on_validation']

    entities, predicates = best['entities'], best['predicates']
    variables = ['Eemb']

    # Turn the { class: set([ elements ]) } dict into two arrays: [ classes ] and [ elements ]
    classes, elements = [], []
    for (_class, _elements) in classes_dict.items():
        for _element in _elements:
            classes += [_class]
            elements += [_element]

    # Turn [ classes ] (containing a class name for each element in elements) in a list of integers
    # e.g. [ 'Class1', 'Class2', 'Class1' ] becomes [ 0, 1, 0 ]
    indexes = [entities.index(element) for element in elements]
    class_idx = {_class:_idx for (_idx, _class) in enumerate(classes_dict.keys())}
    classes_numeric = [class_idx[_class] for _class in classes]

    parameter = best['parameters']['Eemb']
    Xt = np.asarray(parameter['value'])
    _X = np.transpose(Xt)
    X = _X[np.asarray(indexes), :]

    if normalize:
        preprocessing.normalize(X)

    y = np.asarray(classes_numeric)

    # Split the dataset in two equal parts
    #X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.1, random_state=0)

    for it in range(iterations):
        kf = cross_validation.KFold(len(elements), shuffle=True, n_folds=10)
        accuracies = []

        for train_index, test_index in kf:

            X_train, X_test = X[train_index], X[test_index]
            y_train, y_test = y[train_index], y[test_index]

            Cs = [1e-3, 1e-2, 1e-1, 1e0, 1e1, 1e2, 1e3]
            gammas = [1e-4, 1e-3, 1e-2, 1e-1, 1e0, 1e1, 1e2, 1e3, 1e4]

            # Tune hyper-parameters by cross-validation
            tuned_parameters = [{
                                    'kernel': ['linear'],
                                    'C': Cs
                                    }]

            if use_rbf:
                tuned_parameters += [{
                                        'kernel': ['rbf'],
                                        'gamma': gammas,
                                        'C': Cs
                                        }]

            scoring_function = 'accuracy' # ['accuracy', 'adjusted_rand_score', 'average_precision', 'f1', 'log_loss', 'mean_absolute_error', 'mean_squared_error', 'precision', 'r2', 'recall', 'roc_auc']

            logging.debug("# Tuning hyper-parameters for %s" % scoring_function)

            model = svm.SVC()
            clf = grid_search.GridSearchCV(model, tuned_parameters, cv=10, scoring=scoring_function)
            clf.fit(X_train, y_train)

            logging.debug("Best parameters set found on development set:")
            logging.debug(clf.best_estimator_)

            logging.debug("Grid scores on development set:")
            for params, mean_score, scores in clf.grid_scores_:
                logging.debug('%0.3f (+/-%0.03f) for %r' % (mean_score, scores.std() / 2, params))

            logging.debug("Detailed classification report:")

            y_true, y_pred = y_test, clf.predict(X_test)

            accuracy = metrics.accuracy_score(y_true, y_pred)
            accuracies += [accuracy]

            logging.info('Accuracy: %s' % metrics.accuracy_score(y_true, y_pred))
            #logging.debug(metrics.classification_report(y_true, y_pred))

        logging.info('Accuracy: %f +/- %f' % (np.mean(accuracies), np.var(accuracies)))

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main(sys.argv[1:])



import os
import logging
import pickle

# import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn import tree
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix;


def classifier_choice(estimators=500, algo='rf'):
    """
        Selecting the RF classifier to be used.
        -------
        Returns:
        - sklearn object
            Corresponds to the optimal RF sklearn classifier.
    """
    print(algo + " " + algo == 'rf')
    if algo == 'rf':
        print('Random Forest Classifier Selected')
        return RandomForestClassifier(n_estimators=estimators, max_depth=50, random_state=0, n_jobs=-1)
    elif algo == 'lr':
        print('Logistic Regression Classifier Selected')
        return LogisticRegression();
    elif algo == 'svm':
        print('Support vector Classifier Selected')
        return SVC(probability=True);
    # return GaussianNB();
    elif algo == 'knn':
        print('KNN Classifier Selected')
        return KNeighborsClassifier(n_neighbors=50)
    elif algo == 'dt':
        print('Decision Tree Classifier Selected')
        return tree.DecisionTreeClassifier()
    else:
        RandomForestClassifier(n_estimators=estimators, max_depth=40, random_state=0, n_jobs=-1)

def predict_labels_using_threshold(names_length, labels_predicted_proba, threshold):
    """
        Perform classification on the files 'names' using a threshold (probability of the sample
        being malicious) to predict the target values.

        -------
        Parameters:
        - names_length: int
            Number of files being analysed.
        - labels_predicted_proba: matrix
            Contains for each file in the first column the probability of the sample being benign,
            and malicious in the second one.
        - threshold: float
            Probability of a sample being malicious over which the sample will be classified
            as malicious.

        -------
        Returns:
        - list
            Contains the predicted labels of the files being analysed.
    """

    labels_predicted_test = ['nonfp' for _ in range(names_length)]
    for i, _ in enumerate(labels_predicted_test):
        if labels_predicted_proba[i, 0] >= threshold:  # If the proba of the sample being malicious
            # is over the threshold...
            labels_predicted_test[i] = 'fp'  # ... we classify the sample as malicious.

    return labels_predicted_test


def get_classification_results_verbose(names, labels, labels_predicted, labels_predicted_proba,
                                       model, attributes, threshold):
    """
        Print in stdout the classification results of the files 'names' after our analysis.
        Format: 'Name: labelPredicted (trueLabel) Probability[benign, malicious] majorityVoteTrees'

        -------
        Parameters:
        - names: list
            Contains the path of the files being analysed.
        - labels: list
            Contains the labels (real classification or '?') of the files being analysed.
        - labels_predicted: list
            Contains the predicted labels of the files being analysed.
        - labels_predicted_proba: matrix
            Contains in the first column the probability of the samples being benign,
            and malicious in the second one.
        - model
            Model to be used to classify new observations.
        - attributes: csr_matrix
            Features of the data considered.
        - threshold: float
            Probability of a sample being malicious over which the sample will be classified
            as malicious.
    """

    counts_of_same_predictions = get_nb_trees_specific_label(model, attributes,
                                                             labels, labels_predicted, threshold)
    nb_trees = len(model.estimators_)

    for i, _ in enumerate(names):
        print(str(names[i]) + ': ' + str(labels_predicted[i]) + ' ('
              + str(labels[i]) + ') ' + 'Proba: ' + str(labels_predicted_proba[i])
              + ' Majority: ' + str(counts_of_same_predictions[i]) + '/' + str(nb_trees))

    print('> Name: labelPredicted (trueLabel) Probability[fp, nonfp] majorityVoteTrees')


def get_classification_results(names, labels_predicted):
    """
        Print in stdout the classification results of the files 'names' after our analysis.
        Format: 'Name: labelPredicted (trueLabel)'

        -------
        Parameters:
        - names: list
            Contains the path of the files being analysed.
        - labels_predicted: list
            Contains the predicted labels of the files being analysed.
    """

    for i, _ in enumerate(names):
        print(str(names[i]) + ': ' + str(labels_predicted[i]))
    print('> Name: labelPredicted')


def get_score(labels, labels_predicted):
    """
        Print in stdout the accuracy results of our classification (i.e. detection accuracy,
        true positives, false positives, false negatives and true negatives).

        -------
        Parameters:
        - labels: list
            Contains the labels (real classification or '?') of the files being analysed.
        - labels_predicted: list
            Contains the predicted labels of the files being analysed.
    """

    if '?' in labels:
        logging.info("No ground truth given: unable to evaluate the accuracy of the "
                     "classifier's predictions")
    else:
        try:
            tn, fp, fn, tp = confusion_matrix(labels, labels_predicted,
                                              labels=['nonfp', 'fp']).ravel()

            # rf_roc = plot_roc_curve(model,labels, labels_predicted);
            # plt.show()
            print("Detection: " + str((tp + tn) / (tp + tn + fp + fn)))
            print("TP: " + str(tp) + ", FP: " + str(fp) + ", FN: " + str(fn) + ", TN: "
                  + str(tn))
            print("TPR: " + str(tp / (tp + fn)) + ", TNR: " + str(tn / (tn + fp)))

        except ValueError as error_message:  # In the case of a binary classification
            # (i.e. benign or malicious), if the confusion_matrix only contains one element, it
            # means that only one of the class was tested and all samples correctly classified.
            logging.exception(error_message)


def get_nb_trees_specific_label(model, attributes, labels, labels_predicted, threshold):
    """
        Get the number of trees which gave the same prediction as the one of the whole forest.

        -------
        Parameters:
        - model
            Model to be used to classify new observations.
        - attributes: csr_matrix
            Features of the data considered.
        - labels: list
            True labels (i.e. 'benign', 'malicious',or '?') of the data considered.
        - labels_predicted: list
            Labels (i.e. 'benign', 'malicious',or '?') of the data considered predicted using model.
        - threshold: float
            Probability of a sample being malicious over which the sample will be classified
            as malicious.

    """

    # Initialize a vector to hold counts of trees that gave the same class as in labels_predicted
    counts_of_same_predictions = [0 for _, _ in enumerate(labels)]
    # i = 0
    for each_tree in model.estimators_:
        single_tree_predictions_proba = each_tree.predict_proba(attributes)
        single_tree_predictions = predict_labels_using_threshold(len(labels),
                                                                 single_tree_predictions_proba,
                                                                 threshold)
        # Check if predictions are the same with the global (forest's) predictions
        for j, _ in enumerate(single_tree_predictions):
            if single_tree_predictions[j] == labels_predicted[j]:
                counts_of_same_predictions[j] += 1

    return counts_of_same_predictions


def save_analysis_results(save_dir, names, attributes, labels):
    """
        Save the results of a previous analysis, i.e. files name, attributes and label.

        -------
        Parameters:
        - save_dir: str
            Path of the directory to store the results in.
        - names: list
            Name of the data files considered.
        - labels: list
            Labels (i.e. 'benign', 'malicious',or '?') of the data considered.
        - attributes: csr_matrix
            Features of the data considered.
    """

    # Directory to store the classification related files
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    pickle.dump(names, open(os.path.join(save_dir, 'Names'), 'wb'))
    pickle.dump(attributes, open(os.path.join(save_dir, 'Attributes'), 'wb'))
    pickle.dump(labels, open(os.path.join(save_dir, 'Labels'), 'wb'))

    logging.info('The results of the analysis have been successfully stored in %s', save_dir)

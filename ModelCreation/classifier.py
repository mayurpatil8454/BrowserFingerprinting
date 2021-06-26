import os
import pickle
import argparse
import logging

import matplotlib.pyplot as plt;
import setup
from sklearn.metrics import plot_roc_curve;
import machine_learning
import utility
import static_analysis


def test_model(names, labels, attributes, model, print_res=False, print_res_verbose=True,
               print_score=True, threshold=0.50,algo ='rf'):
    """
        Use an existing model to classify new JS inputs.

    """
    print(model);
    if isinstance(model, str):
        model = pickle.load(open(model, 'rb'))
    # model_lr = pickle.load(open('../Analysis/lr','rb'))
    # model_svm = pickle.load(open('../Analysis/svm','rb'))
    # model_knn = pickle.load(open('../Analysis/knn', 'rb'))
    # model_dt = pickle.load(open('../Analysis/dt', 'rb'))


    # RocCurve
    Roc_Random = plot_roc_curve(model, attributes, labels, pos_label=model.classes_[0]);
    ax = plt.gca();
    # Roc_lr = plot_roc_curve(model_lr, attributes, labels, ax=ax, pos_label = model.classes_[0]);
    # Roc_svm = plot_roc_curve(model_svm, attributes, labels, ax=ax, pos_label = model.classes_[0]);
    # Roc_knn = plot_roc_curve(model_knn, attributes, labels, ax=ax, pos_label = model.classes_[0]);
    # Roc_dt = plot_roc_curve(model_dt, attributes, labels, ax=ax, pos_label = model.classes_[0]);

    # Roc_Random.plot(ax=ax);
    # plt.savefig("../images/Comparision_roc.png")
    # plt.savefig("../images/Base"+ algo +"_roc.png")

    labels_predicted_proba_test = model.predict_proba(attributes)
    # Probability of the samples for each class in the model.
    # First column = benign, second = malicious.
    # labels_predicted_test = model.predict(attributes_test)
    # accuracy_test = model.score(attributes_test, labels_test)  # Detection rate

    labels_predicted_test = machine_learning.\
        predict_labels_using_threshold(len(names), labels_predicted_proba_test, threshold)
    # Perform classification using a threshold (probability of the sample being malicious)
    # to predict the target values

    if print_res:
        machine_learning.get_classification_results(names, labels_predicted_test)




    # Uncomment when using the Random forest
    # if print_res_verbose:
    #     machine_learning.get_classification_results_verbose(names, labels, labels_predicted_test,
    #                                                         labels_predicted_proba_test, model,
    #                                                         attributes, threshold)

    if print_score:
        machine_learning.get_score(labels, labels_predicted_test);


    return labels_predicted_test



def main_classification():      # algo = arg_obj['algo']
    """
        Feature Extraction for classification
    """

    features2int_dict_path = os.path.join(setup.model , 'Features' +'_selected_features_99')


    if setup.ChromeAPIflag == 0:
        names, attributes, labels = static_analysis.main_analysis\
            (js_dirs=setup.TestArray, labels_dirs=['fp', 'nonfp'], js_files=None, labels_files=None,
             n=setup.ngramssize, features2int_dict_path=features2int_dict_path)
    else:
        """Get JS FIles from temp"""
        js_files =[];
        print(os.listdir(setup.ChromePath));
        for cfile in os.listdir(setup.ChromePath):  #getallfiles of dicr
            js_files.append(os.path.join(setup.ChromePath, cfile))

        print(js_files);
        names, attributes, labels = static_analysis.main_analysis\
            (js_dirs=None, labels_dirs=None, js_files=js_files, labels_files=None,
             n=setup.ngramssize, features2int_dict_path=features2int_dict_path)


    #
    # names = pickle.load(open(os.path.join(os.path.join(setup.Non_fp_samples_test_path, "Analysis-res-stored"), 'Names'), 'rb'))
    # attributes = pickle.load(open(os.path.join(os.path.join(setup.Non_fp_samples_test_path, "Analysis-res-stored"), 'Attributes'), 'rb'))
    # labels = pickle.load(open(os.path.join(os.path.join(setup.Non_fp_samples_test_path, "Analysis-res-stored"), 'Labels'), 'rb'))

    if names:
        # Uncomment to save the analysis results in pickle objects.

        # machine_learning.save_analysis_results(os.path.join(setup.Non_fp_samples_test_path, "Analysis-res-stored"),
        #                                        names, attributes, labels)

        if setup.ChromeAPIflag == 0:
            test_model(names, labels, attributes, model=os.path.join(setup.model,setup.algo), threshold=setup.threshhold,algo = setup.algo)
        else:
            result = test_model(names, labels, attributes, model=os.path.join(setup.model,setup.algo), threshold=setup.threshhold,algo = setup.algo)
            return names, result

    else:
        logging.warning('No valid JS file found for the analysis')

"""Comment if using the Chrome extension"""
# if __name__ == "__main__":  # Executed only if run as a script
#     main_classification()



import os
import pickle
import logging

import setup
import features_preselection
import features_selection
import static_analysis
import machine_learning
import utility

SRC_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


def classify(names, labels, attributes, model_dir, model_name, estimators,
             print_score=False, print_res=False , algo='rf'):  #default model random forest

    # Directory to store the classification related files
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)

    clf = machine_learning.classifier_choice(estimators=estimators, algo=algo)
    trained = clf.fit(attributes, labels)  # Model
    labels_predicted = clf.predict(attributes)  # Classification and class predictions

    if print_score:
        machine_learning.get_score(labels, labels_predicted)

    if print_res:
        machine_learning.get_classification_results(names, labels_predicted)

    model_path = os.path.join(model_dir, model_name)
    pickle.dump(trained, open(model_path, 'wb'))
    logging.info('The model has been successfully stored in %s', model_path)

    return trained



def main_learn():
    """Learning the model"""
    analysis_path = os.path.join(setup.model, 'Features') #store Calculated features here


    features2int_dict_path = os.path.join(analysis_path + '_selected_features_99')
    # print(n);

    """Getting All features from the train Set"""
    features_preselection.handle_features_all(setup.TrainArray, ['fp', 'nonfp'],
                                              analysis_path, setup.ngramssize)

    """Getting All features from the Validation set and create final features set"""
    features_selection.store_features_all(setup.ValidateArray , ['fp','nonfp'], analysis_path,  setup.ngramssize)

    """Getting the Features set and their corresponding labels"""
    names, attributes, labels = static_analysis.main_analysis\
        (js_dirs=setup.TrainArray, labels_dirs=['fp','nonfp'], js_files=None, labels_files=None,
         n=setup.ngramssize, features2int_dict_path=features2int_dict_path)

    # names = pickle.load(open(os.path.join(os.path.join(setup.model, "Analysis-n" + str(setup.ngramssize) + "-dict"), 'Names'), 'rb'))
    # attributes = pickle.load(open(os.path.join(os.path.join(setup.model, "Analysis-n" + str(setup.ngramssize) + "-dict"), 'Attributes'), 'rb'))
    # labels = pickle.load(open(os.path.join(os.path.join(setup.model, "Analysis-n" + str(setup.ngramssize) + "-dict"), 'Labels'), 'rb'))
    if names:
        #first time store all the calculated ngrams
        print("storing data");
        machine_learning.save_analysis_results(os.path.join(setup.model, "Analysis-n" + str(setup.ngramssize) + "-dict"),
                                      names, attributes, labels)


        classify(names, labels, attributes, model_dir=setup.model, model_name=setup.algo,
                 print_score=True, print_res=True, estimators=setup.rftreesize, algo=setup.algo)

    else:
        logging.warning('No valid JS file found for the analysis')


if __name__ == "__main__":  # Executed only if run as a script
    main_learn()

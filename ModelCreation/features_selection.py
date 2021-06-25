
import os
import pickle
import logging
import timeit
from multiprocessing import Process, Queue
import queue  # For the exception queue.Empty which is not in the multiprocessing package
from scipy.stats import chi2_contingency, chi2

import features_preselection
import static_analysis
import utility


SRC_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))



def store_features_all(js_dirs_validate, labels_validate,
                       analysis_path, n, analyzed_features_path=None, chi_confidence=99):
    """ store_features for the 2 validation directories; TO CALL """

    features_path = os.path.join(analysis_path + '_all_features_')

    all_features_dict_path_bad = features_path + 'fp'
    all_features_dict_path_good = features_path + 'nonfp'


    logging.debug('Currently selecting the features with chi2')
    path_info = str('')
    store_features(all_features_dict_path_good, all_features_dict_path_bad, js_dirs_validate,
                   labels_validate, path_info, analysis_path, n,
                   analyzed_features_path, chi_confidence)



def store_features(all_features_dict_path1, all_features_dict_path2, samples_dir_list,
                   labels_list, path_info, analysis_path, n=4,
                   analyzed_features_path=None, chi_confidence=99):
    """ Stores the features selected by chi2 in a dict.
        The confidence has to be given in percent. """

    pickle_path = os.path.join(analysis_path + '_selected_features_' + str(chi_confidence))
    utility.check_folder_exists(pickle_path)

    if analyzed_features_path is None:
        all_features_dict1 = pickle.load(open(all_features_dict_path1, 'rb'))
        all_features_dict2 = pickle.load(open(all_features_dict_path2, 'rb'))

        analyzed_features_dict = analyze_features_all(all_features_dict1, all_features_dict2,
                                                      samples_dir_list, labels_list,
                                                      path_info,
                                                      n, analysis_path)

    else:
        analyzed_features_dict = pickle.load(open(analyzed_features_path, 'rb'))

    selected_features_dict = select_features(analyzed_features_dict, chi_confidence)
    pickle.dump(selected_features_dict, open(pickle_path, 'wb'))

    return selected_features_dict




def analyze_features_all(all_features_dict1, all_features_dict2, samples_dir_list,
                         labels_list, path_info, n, analysis_path):
    """ Produces a dict containing the number of occurrences (or not) of each expected feature
    with a distinction between benign and malicious files. """

    if len(samples_dir_list) != len(labels_list):
        logging.error("error with the label list", str(len(samples_dir_list)), str(len(labels_list)))
        return None



    pickle_path = os.path.join(analysis_path + '_analyzed_features_' + path_info)
    utility.check_folder_exists(pickle_path)

    analyzed_features_dict = initialize_analyzed_features_dict(all_features_dict1,
                                                               all_features_dict2)

    analyses = get_features_all_files_multiproc(samples_dir_list, labels_list, n)

    for analysis in analyses:
        features_dict = analysis.features
        label = analysis.label
        if features_dict is not None:
            analyze_features(analyzed_features_dict, features_dict, label)

    pickle.dump(analyzed_features_dict, open(pickle_path, 'wb'))

    return analyzed_features_dict



def initialize_analyzed_features_dict(all_features_dict1, all_features_dict2):
    """ Create the analyzed_features_dict with all expected features (from all_features_dict_path)
    as key and [0, 0, 0, 0] as value. """

    # all_features_dict = pickle.load(open(all_features_dict_path, 'rb'))
    analyzed_features_dict = dict()
    popular_features1 = get_popular_features(all_features_dict1)
    popular_features2 = get_popular_features(all_features_dict2)

    for feature in popular_features1:
        analyzed_features_dict[feature] = [0]*4
    for feature in popular_features2:
        if feature not in analyzed_features_dict:
            analyzed_features_dict[feature] = [0]*4
    return analyzed_features_dict




def get_features_all_files_multiproc(samples_dir_list, labels_list, n):
    """
        Gets the features of all files from samples_dir_list.
    """

    my_queue = Queue()
    out_queue = Queue()
    except_queue = Queue()
    workers = list()

    for i, _ in enumerate(samples_dir_list):
        samples_dir = samples_dir_list[i]
        label = labels_list[i]
        for sample in os.listdir(samples_dir):
            sample_path = os.path.join(samples_dir, sample)
            analysis = static_analysis.Analysis(pdg_path=sample_path, label=label)
            my_queue.put([analysis, n])

    for i in range(utility.NUM_WORKERS):
        p = Process(target=features_preselection.worker_get_features, args=(my_queue, out_queue,
                                                                            except_queue))
        p.start()
        workers.append(p)

    analyses = list()

    while True:
        try:
            analysis = out_queue.get(timeout=0.01)
            analyses.append(analysis)
        except queue.Empty:
            pass
        all_exited = True
        for w in workers:  # Instead of join, as the worker cannot be joined when elements
            if w.exitcode is None:
                all_exited = False
                break
        if all_exited & out_queue.empty():
            break

    return analyses



def get_popular_features(all_features_dict):
    """ Gets the features used more than one time. """
    popular_features = dict()
    for k, v in all_features_dict.items():
        if v > 10:  # Tested with chi2, to ensure that feature and classification are dependent
            popular_features[k] = v
    return popular_features




def analyze_features(analyzed_features_dict, features_sample, label):
    """
        Features' analysis before selection process. We count the number of times a given feature:
            * appear in a nonfp sample;
            * don't appear in a nonfp sample;
            * appear in a fp sample;
            * don't appear in a fp sample.
        We do that by analyzing the features per sample.

        -------
        Parameters:
        - analyzed_features_dict: dict
            * Key: features to analyze;
            * Value: [nonfp_with_f, nonfp_wo_f, fp_with_f, fp_wo_f].
        - features_sample: dict
            Features present in the considered sample.
        - label: string
            Label of the sample: 'nonfp' or 'fp'.
    """

    # Set of features that were not found in the current sample
    features_not_sample = set(analyzed_features_dict.keys()) - set(features_sample.keys())

    if label == 'nonfp':
        i = 0
    elif label == 'fp':
        i = 2
    else:
        i = -1
        logging.error("The label should be 'fp' or 'nonfp', got %s", label)

    for feature in features_sample:
        try:
            analyzed_features_dict[feature][i] += 1  # Increase the feature is present counter
        except KeyError as err:
            logging.debug(err)
    for feature in features_not_sample:
        analyzed_features_dict[feature][i + 1] += 1  # Increase the feature not present counter



def get_chi(confidence):
    """ Gets the chi value for 1 degree of freedom and for a confidence in PERCENT. """
    return round(chi2.isf(q=1-confidence/100, df=1), 2)  # With 2 decimals


def select_features(analyzed_features_dict, confidence):
    """ chi2 test, based on the presence/absence of a given feature and depending on the sample's
    ground truth. """

    selected_features_dict = dict()
    pos = 0
    chi_critical = get_chi(confidence)

    for feature in analyzed_features_dict:
        ben_with_f, ben_wo_f, mal_with_f, mal_wo_f = analyzed_features_dict[feature]

        try:
            chi_square, _, _, _ = chi2_contingency([[ben_with_f, ben_wo_f], [mal_with_f, mal_wo_f]])

        except ValueError:
            chi_square = 0

        if chi_square >= chi_critical:  # 'confidence'% confidence
            logging.debug('Feature presence and classification are not independent, chi2 = %s',
                          str(chi_square))
            selected_features_dict[feature] = pos
            pos += 1

    return selected_features_dict



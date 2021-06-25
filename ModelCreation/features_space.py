import logging
import numpy as np
from scipy.sparse import csr_matrix

import features_counting


def get_features(file_repr, n):
    """ Returns the sort of features chosen for the analysis. """

    features_dict, total_features, pdg_size = features_counting.\
        count_ngrams(file_repr, n)
    return features_dict, total_features, pdg_size




def features2int(features2int_dict, feature):
    """ Convert a feature into an int (position in the vector space). """

    try:
        i = features2int_dict[feature]
        return i
    except KeyError as err:
        logging.debug('The key %s is not in the dictionary, %s', str(feature), str(err))
    return None


def int2features(int2features_dict, i):
    """ Convert an int (position in the vector space) into the corresponding feature. """

    try:
        feature = int2features_dict[i]
        return feature
    except KeyError as err:
        logging.debug('The key %s is not in the dictionary, %s', str(i), str(err))
    return None




def features_vector(file_repr, n, features2int_dict):
    """ Builds a vector so that the probability of occurrences of a feature is stored at the
    corresponding position in the vector space. """

    features_dict, total_features, pdg_size = get_features(file_repr, n)
    csr = None
    nb_features = len(features2int_dict)

    if features_dict is not None:
        features_vect = np.zeros(nb_features + 1)
        for feature in features_dict:
            map_feature2int = features2int(features2int_dict, feature)
            if map_feature2int is not None:
                features_vect[map_feature2int] = features_dict[feature] / total_features
                # Features appear only once in "features", so done only once per feature
        # features_vect[nb_features] = pdg_size
        csr = csr_matrix(features_vect)
        if csr.nnz == 0:  # Empty matrix, no known features
            features_vect[nb_features] = 1  # Because cannot concatenate empty CSR matrices
            csr = csr_matrix(features_vect)

    return csr

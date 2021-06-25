

import logging

import features_ngrams
import features_value

def count_ngrams(file_repr, n):
    """
        After Getting All possible N-grams of file count the no of occurances of specific Ngrams and return total
        no of Unique Ngrams
    """

    features_list, pdg_size = features_ngrams.extract_features(file_repr)
    # print(features_list)
    matrix_all_n_grams = n_grams_list(features_list, n)
    # Each row: tuple representing an n-gram.

    if matrix_all_n_grams is not None:
        dico_of_n_grams = {}
        # Nb of lines in the matrix, i.e. of sets of n-grams
        for j, _ in enumerate(matrix_all_n_grams):
            if matrix_all_n_grams[j] in dico_of_n_grams:
                dico_of_n_grams[matrix_all_n_grams[j]] += 1
            else:
                dico_of_n_grams[matrix_all_n_grams[j]] = 1

        return dico_of_n_grams, len(matrix_all_n_grams), pdg_size
    return None, None, pdg_size




def n_grams_list(numbers_list, n):
    """
        After Getting Array of nodes we will create the Ngrams from it by using the given value
    """

    if numbers_list is not None:
        len_numbers_list = len(numbers_list)
        if n > len_numbers_list:
            matrix_all_n_grams = list()
            ngram = [None for _ in range(n)]
            for i, _ in enumerate(numbers_list):
                ngram[i] = numbers_list[i]
            matrix_all_n_grams.append(tuple(ngram))
            return matrix_all_n_grams
        else:
            range_n = range(n)
            matrix_all_n_grams = list()
            range_list = range(len_numbers_list - (n - 1))
            for j in range_list:  # Loop on all the n-grams
                matrix_all_n_grams.append(tuple(numbers_list[j + i] for i in range_n))
            return matrix_all_n_grams
    return None






def count_ngram_value(file_repr, level, n):
    """ Returns (context, value) * n-gram features + the total number of features. """

    features_list, pdg_size = features_value.extract_features(file_repr, level)
    matrix_all_n_grams = n_grams_list(features_list, n)
    # Each row: tuple representing an n-gram.

    if matrix_all_n_grams is not None:
        dico_of_n_grams = {}
        # Nb of lines in the matrix, i.e. of sets of n-grams
        for j, _ in enumerate(matrix_all_n_grams):
            if matrix_all_n_grams[j] in dico_of_n_grams:
                dico_of_n_grams[matrix_all_n_grams[j]] += 1
            else:
                dico_of_n_grams[matrix_all_n_grams[j]] = 1

        return dico_of_n_grams, len(matrix_all_n_grams), pdg_size
    return None, None, pdg_size

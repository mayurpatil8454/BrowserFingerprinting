

import sys
import os
import pickle
import logging
from subprocess import run, PIPE


SRC_PATH = os.path.abspath(os.path.dirname(__file__))

sys.path.insert(0, os.path.join(SRC_PATH, 'tokens2int'))

from tokens2int import parser_esprima

sys.path.insert(0, os.path.join(SRC_PATH, '..', 'CFG_Creation'))
import node as _node


sys.setrecursionlimit(400000)  # Probably need it to unpickle BIG PDGs ;)



def extract_features(file_repr):
    """
       Map value to the nodes from the all possible nodetypes
    """

    pdg_size = None


    dico_features = parser_esprima.AST_UNITS_DICO
    # List of syntactic units linked by parents, control or data flow
    features_list, pdg_size = extract_syntactic_features(file_repr)

    # print(features_list)

    if features_list is not None and features_list != []:
        return list(map(lambda x: dico_features[x], features_list)), pdg_size
    return None, pdg_size


def extract_syntactic_features(pdg_path):
    """
       returns list of the nodes types
    """

    logging.debug('Analysis of %s', pdg_path)
    try:
        if os.stat(pdg_path).st_size < 25000000:  # Avoids handling CFGs over 25MB for perf reasons
            pdg = pickle.load(open(pdg_path, 'rb'))
            features_list = list()
            get_cfg_features(pdg, features_list=features_list, handled_set=set(), handled_features_set=set())

            return features_list, os.stat(pdg_path).st_size
        return None, os.stat(pdg_path).st_size
    except Exception as Argument:
        print(Argument)
        logging.error('The PDG of %s could not be loaded', pdg_path)
    return None, None


def get_cfg_features(cfg, features_list, handled_set, handled_features_set):
    """ TO traverse through node in depth first manner"""

    for child in cfg.children:
        if child.id not in handled_set:
            traverse_cfg(child, features_list, handled_set, handled_features_set)
        get_cfg_features(child, features_list, handled_set, handled_features_set)


def get_ast_features(cfg, features_list, handled_set):
    """
       Adding all the features which reside under control dependecy but then statements
    """
    for child in cfg.children:  # childerens which do not have the control dependancy
        if child.id not in handled_set:
            handled_set.add(child.id)
            features_list.append(child.name)
            get_ast_features(child, features_list, handled_set)






def traverse_cfg(cfg, features_list, handled_set, handled_features_set):
    """
        Traverse CFG in Depth first search PreOrder manner
    """

    if cfg.control_dep_children:  #check for control dependent node
        features_list.append(cfg.name)   #added current CFG node in feature
        handled_features_set.add(cfg.id)  # Store id from features handled
        get_ast_features(cfg, features_list, handled_features_set)  # Handled only once
    for control_dep in cfg.control_dep_children:  #Traverse all childeren which has control dependency
        control_flow = control_dep.extremity     #gets all dependecy control and statements
        # Otherwise missing CF pointing to a node already analyzed
        if not control_flow.control_dep_children or control_flow.id in handled_set:   #if not already handled add and not
            features_list.append(control_flow.name)
        # else: the node name will be added while calling traverse_cfg
        if control_flow.id not in handled_set:  #called for all other recurrently
            handled_set.add(control_flow.id)
            handled_features_set.add(control_flow.id)  # Store id from features
            get_ast_features(control_flow, features_list, handled_features_set)  # Once
            traverse_cfg(control_flow, features_list, handled_set, handled_features_set)






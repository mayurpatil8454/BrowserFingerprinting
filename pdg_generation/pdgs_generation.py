# Copyright (C) 2019 Aurore Fass
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
    Generation and storage of JavaScript PDGs. Possibility for multiprocessing (NUM_WORKERS
    defined in utility_df.py).
"""

import pickle
import psutil
from multiprocessing import Process, Queue

from utility_df import *
from handle_json import *
from build_cfg import *
from build_dfg import *
from var_list import *
from display_graph import *


GIT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))


def pickle_dump_process(dfg_nodes, store_pdg):
    """ Call to pickle.dump """

    pickle.dump(dfg_nodes, open(store_pdg, 'wb'))


def get_data_flow(input_file, benchmarks, store_pdgs=None, check_var=False,
                  save_path_ast=False, save_path_cfg=False, save_path_pdg=False):
    """
        Produces the PDG of a given file.

        -------
        Parameters:
        - input_file: str
            Path of the file to study.
        - benchmarks: dict
            Contains the different microbenchmarks. Should be empty.
        - store_pdgs: str
            Path of the folder to store the PDG in.
            Or None to pursue without storing it.
        check_var: bool
            Build PDG just to check if our malicious variables are undefined. Default: False.
        - save_path_ast / cfg / pdg:
            False --> does neither produce nor store the graphical representation;
            None --> produces + displays the graphical representation;
            Valid-path --> Produces + stores the graphical representation under the name Valid-path.


        -------
        Returns:
        - Node
            PDG of the file
        - or None.
    """

    start = timeit.default_timer()
    if input_file.endswith('.js'):
        esprima_json = input_file.replace('.js', '.json')
    else:
        esprima_json = input_file + '.json'

    extended_ast = get_extended_ast(input_file, esprima_json)
    if extended_ast is not None:
        benchmarks['got AST'] = timeit.default_timer() - start
        start = micro_benchmark('Successfully got Esprima AST in', timeit.default_timer() - start)
        ast = extended_ast.get_ast()
        # beautiful_print_ast(ast, delete_leaf=[])
        ast_nodes = ast_to_ast_nodes(ast, ast_nodes=Node('Program'))
        # ast_nodes = search_dynamic(ast_nodes)  # Tried to handle dynamically generated JS
        benchmarks['AST'] = timeit.default_timer() - start
        start = micro_benchmark('Successfully produced the AST in', timeit.default_timer() - start)
        if save_path_ast is not False:
            draw_ast(ast_nodes, attributes=True, save_path=save_path_ast)
        cfg_nodes = build_cfg(ast_nodes)
        benchmarks['CFG'] = timeit.default_timer() - start
        start = micro_benchmark('Successfully produced the CFG in', timeit.default_timer() - start)
        if save_path_cfg is not False:
            draw_cfg(cfg_nodes, attributes=True, save_path=save_path_cfg)
        unknown_var = []
        try:
            with Timeout(120):  # Tries to produce DF within 60s
                dfg_nodes = df_scoping(cfg_nodes, var_loc=VarList(), var_glob=VarList(),
                                       unknown_var=unknown_var, id_list=[], entry=1)[0]
        except Timeout.Timeout:
            logging.exception('Timed out for %s', input_file)
            return None
        if save_path_pdg is not False:
            draw_pdg(dfg_nodes, attributes=True, save_path=save_path_pdg)
        for unknown in unknown_var:
            logging.warning('The variable ' + unknown.attributes['name'] + ' is not declared')
        if check_var:
            return unknown_var
        benchmarks['PDG'] = timeit.default_timer() - start
        micro_benchmark('Successfully produced the PDG in', timeit.default_timer() - start)
        if store_pdgs is not None:
            store_pdg = os.path.join(store_pdgs, os.path.basename(input_file.replace('.js', '')))
            # pickle.dump(dfg_nodes, open(store_pdg, 'wb'))
            # I don't know why, but some PDGs lead to Segfault, this way it does not kill the
            # current process at least
            p = Process(target=pickle_dump_process, args=(dfg_nodes, store_pdg))
            p.start()
            p.join()
            if p.exitcode != 0:
                logging.error('Something wrong occurred to pickle the PDG of %s', store_pdg)
                if os.path.isfile(store_pdg) and os.stat(store_pdg).st_size == 0:
                    os.remove(store_pdg)
        features_list = list()
        get_cfg_features(dfg_nodes, features_list=features_list, handled_set=set(),
                         handled_features_set=set())
        # print(features_list);
        return dfg_nodes
    return None

counter =0;
def get_cfg_features(pdg, features_list, handled_set, handled_features_set):
    """ To provide complete code coverage while following only the CF. """

    for child in pdg.children:
        if child.id not in handled_set:
            traverse_cfg(child, features_list, handled_set, handled_features_set)
        get_cfg_features(child, features_list, handled_set, handled_features_set)


def traverse_cfg(pdg, features_list, handled_set, handled_features_set):
    """
        Given the PDG of a JavaScript file, create a list containing the esprima syntactic
        units with a Control dependency.
        The order of the units stored in the previous list resembles a tree traversal using
        the depth-first pre order.

        -------
        Parameters:
        - pdg: node
            PDG of the JS file to analyze.
        - features_list: list
            Contains the units found so far.
        - handled_list: list
            Contains the nodes id handled so far.
    """

    if pdg.control_dep_children:
        features_list.append(pdg.name)
        handled_features_set.add(pdg.id)  # Store id from features handled
        get_ast_features(pdg, features_list, handled_features_set)  # Handled only once
        # print(features_list);
    for control_dep in pdg.control_dep_children:
        control_flow = control_dep.extremity
        # Otherwise missing CF pointing to a node already analyzed
        if not control_flow.control_dep_children or control_flow.id in handled_set:
            features_list.append(control_flow.name)
        # else: the node name will be added while calling traverse_cfg
        if control_flow.id not in handled_set:
            handled_set.add(control_flow.id)
            handled_features_set.add(control_flow.id)  # Store id from features
            get_ast_features(control_flow, features_list, handled_features_set)  # Once
            traverse_cfg(control_flow, features_list, handled_set, handled_features_set)

def get_ast_features(pdg, features_list, handled_set):
    """
        Given the PDG of a JavaScript file, create a list containing the esprima syntactic
        units.
        The order of the units stored in the previous list resembles a tree traversal using
        the depth-first pre order.

        -------
        Parameters:
        - pdg: node
            PDG of the JS file to analyze.
        - features_list: list
            Contains the units found so far.
        - handled_list: list
            Contains the nodes id handled so far.
    """

    for child in pdg.children:
        if child.id not in handled_set:
            handled_set.add(child.id)
            features_list.append(child.name)
            get_ast_features(child, features_list, handled_set)
            #print(features_list);




def handle_one_pdg(root, js, store_pdgs):
    """ Stores the PDG of js located in root, in store_pdgs. """

    benchmarks = dict()
    #print(os.path.join(store_pdgs, js.replace('.js', '')))
    get_data_flow(input_file=os.path.join(root, js), benchmarks=benchmarks,
                  store_pdgs=store_pdgs)


def worker(my_queue):
    """ Worker """

    while True:
        try:
            item = my_queue.get(timeout=2)
            # print(item)
            handle_one_pdg(item[0], item[1], item[2])
        except Exception as e:
            break


def store_cfg_folder(folder_js):
    """
        Stores the PDGs of the JS files from folder_js.

        -------
        Parameters:
        - folder_js: str
            Path of the folder containing the files to get the PDG of.
    """

    start = timeit.default_timer()
    ram = psutil.virtual_memory().used
    # benchmarks = dict()

    my_queue = Queue()
    workers = list()

    if not os.path.exists(folder_js):
        logging.exception('The path %s does not exist', folder_js)
        return
    store_pdgs = os.path.join(folder_js, 'Analysis', 'CFG')
    if not os.path.exists(store_pdgs):
        os.makedirs(store_pdgs)

    for root, _, files in os.walk(folder_js):
        for js in files:
            my_queue.put([root, js, store_pdgs])
            # time.sleep(0.1)  # Just enough to let the Queue finish

    for i in range(NUM_WORKERS):
        p = Process(target=worker, args=(my_queue,))
        p.start()
        print("Starting process")
        workers.append(p)

    for w in workers:
        w.join()

    get_ram_usage(psutil.virtual_memory().used - ram)
    micro_benchmark('Total elapsed time:', timeit.default_timer() - start)




if __name__ == "__main__":  # Executed only if run as a script
    get_data_flow(os.path.abspath(os.path.join(os.path.dirname(__file__), 'CFGDummy.js')),dict());

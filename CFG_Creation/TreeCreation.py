from CreatingAST import *
from graphs import *
import pickle


SRC_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__)))
print(SRC_PATH)

def createAST(input_file,folder_js):
    print(input_file);
    if input_file.endswith('.js'):
        esprima_json = input_file.replace('.js', '.json')
    else:
        esprima_json = input_file + '.json'

    extended_ast = get_extended_ast(input_file, esprima_json)      # to create Object of AST created by the ESPRIMA
    if extended_ast is not None:

        ast = extended_ast.get_ast()    # get root node
        ast_nodes = ast_to_ast_nodes(ast, ast_nodes=Node('Program'))    ##to traaverse all to make a tree graph

        draw_ast(ast_nodes, attributes=True, save_path=os.path.join(SRC_PATH, 'AST.gv'))     #To Create the graph of AST
        cfg_nodes = build_cfg(ast_nodes)      ##to create the tree from the AST graph

        store_cfgs = os.path.join(folder_js, 'Analysis', 'CFG', input_file.replace('.js', ''))
        pickle.dump(cfg_nodes, open(store_cfgs, 'wb'))

        draw_cfg(cfg_nodes, attributes=True, save_path=os.path.join(SRC_PATH, 'CFG.gv'))     #//////To Create the graph of CFG


#
# if __name__ == "__main__":  # Executed only if run as a script
#     createAST(os.path.abspath(os.path.join(os.path.dirname(__file__), 'CFGDummy.js')),os.path.join(os.path.dirname(__file__)))  #'..','Data', 'Browser_Fingerprint_Script_0001.js')))
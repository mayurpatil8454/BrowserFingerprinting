import os
from subprocess import run, PIPE
from astattributes import *
from node import *
import json

SRC_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__)))

def get_extended_ast(input_file, json_path='1', remove_json=True):
    """Get AST from Esprima"""

    produce_ast = run(['node', os.path.join(SRC_PATH, 'js2ast.js'), input_file, json_path],stdout=PIPE)
                                    #TO create the AST for the JS file
    if produce_ast.returncode == 0:
        if json_path == '1':    #Check for AST in JSon format
            ast = produce_ast.stdout.decode('utf-8').replace('\n', '')
            return ast.split('##!!**##')
        else:
            with open(json_path) as json_data:
                esprima_ast = json.loads(json_data.read())
            if remove_json:
                os.remove(json_path)   #delete the Stored JSON format AST f

            extended_ast = ExtendedAst()    #create the object

            #set the values of the root node to the object
            extended_ast.set_type(esprima_ast['type'])
            extended_ast.set_body(esprima_ast['body'])
            extended_ast.set_source_type(esprima_ast['sourceType'])
            extended_ast.set_range(esprima_ast['range'])
            extended_ast.set_tokens(esprima_ast['tokens'])
            extended_ast.set_comments(esprima_ast['comments'])
            if 'leadingComments' in esprima_ast:
                extended_ast.set_leading_comments(esprima_ast['leadingComments'])
            # print(extended_ast)
            return extended_ast

    return None


def create_node(dico, node_body, parent_node, cond=False):
    """ Node creation. """
    if 'type' in dico:
        node = Node(name=dico['type'], parent=parent_node)
        parent_node.set_child(node)
        node.set_body(node_body)
        if cond:
            node.set_body_list(True)  # Some attributes are stored in a list
        ast_to_ast_nodes(dico, node)


def ast_to_ast_nodes(ast, ast_nodes=Node('Program')):
    """
      Create the the tree from root node
    """
    print("start")
    for k in ast:

        print(k);
        if k == 'range' or (k != 'type' and not isinstance(ast[k], list)
                            and not isinstance(ast[k], dict)) or k == 'regex':
            ast_nodes.set_attribute(k, ast[k])  # range is a list but stored as attributes
        if isinstance(ast[k], dict):
            if k == 'range':  # Case leadingComments as range: {0: begin, 1: end}
                ast_nodes.set_attribute(k, ast[k])
            else:
                create_node(dico=ast[k], node_body=k, parent_node=ast_nodes)
        elif isinstance(ast[k], list):
            if not ast[k]:  # Case with empty list, e.g. params: []
                ast_nodes.set_attribute(k, ast[k])
            for el in ast[k]:
                if isinstance(el, dict):
                    create_node(dico=el, node_body=k, parent_node=ast_nodes, cond=True)
    return ast_nodes





# Creating CFG

NonConditional = ['BlockStatement', 'DebuggerStatement', 'EmptyStatement',
           'ExpressionStatement', 'LabeledStatement', 'ReturnStatement',
           'ThrowStatement', 'WithStatement', 'CatchClause', 'VariableDeclaration',
           'FunctionDeclaration']

CONDITIONAL = ['DoWhileStatement', 'ForStatement', 'ForOfStatement', 'ForInStatement',
               'IfStatement', 'SwitchCase', 'SwitchStatement', 'TryStatement',
               'WhileStatement', 'ConditionalExpression']

UNSTRUCTURED = ['BreakStatement', 'ContinueStatement']



def build_cfg(ast_nodes):
    """
        traverse AST in BFS manner and create CFG from it
    """

    for child in ast_nodes.children:
        if child.name in NonConditional or child.name in UNSTRUCTURED:
            NonConditional_statement_cf(child)
        elif child.name in CONDITIONAL:
            conditional_statement_cf(child)
        else:
            for grandchild in child.children:
                if not grandchild.is_statement():
                    link_expression(node=grandchild, node_parent=child)
                else:
                    child.set_control_dependency(extremity=grandchild, label='e')
        build_cfg(child)
    return ast_nodes


def conditional_statement_cf(node):
    """ For the conditional nodes. """
    if node.name == 'DoWhileStatement':
        do_while_cf(node)
    elif node.name == 'ForStatement' or node.name == 'ForOfStatement'\
            or node.name == 'ForInStatement':
        for_cf(node)
    elif node.name == 'IfStatement' or node.name == 'ConditionalExpression':
        if_cf(node)
    elif node.name == 'WhileStatement':
        while_cf(node)
    elif node.name == 'TryStatement':
        try_cf(node)
    elif node.name == 'SwitchStatement':
        switch_cf(node)
    elif node.name == 'SwitchCase':
        pass  # Already handled in SwitchStatement

def for_cf(node):
    """ ForStatement. """
    # Element 0: init
    # Element 1: test (Expression)
    # Element 2: update (Expression)
    # Element 3: body (Statement)
    """ ForOfStatement. """
    # Element 0: left
    # Element 1: right
    # Element 2: body (Statement)
    i = 0
    for child in node.children:
        if child.body != 'body':
            link_expression(node=child, node_parent=node)
        elif not child.is_comment():
            node.set_control_dependency(extremity=child, label=True)
        i += 1
    extra_comment_node(node, i)


def if_cf(node):
    """ IfStatement. """
    # Element 0: test (Expression)
    # Element 1: consequent (Statement)
    # Element 2: alternate (Statement)
    link_expression(node=node.children[0], node_parent=node)
    node.set_control_dependency(extremity=node.children[1], label=True)
    if len(node.children) > 2:
        if node.children[2].is_comment():
            node.set_comment_dependency(extremity=node.children[2])
        else:
            node.set_control_dependency(extremity=node.children[2], label=False)
            extra_comment_node(node, 3)


def do_while_cf(node):
    """ DoWhileStatement. """
    # Element 0: body (Statement)
    # Element 1: test (Expression)
    node.set_control_dependency(extremity=node.children[0], label=True)
    link_expression(node=node.children[1], node_parent=node)
    extra_comment_node(node, 2)


def while_cf(node):
    """ WhileStatement. """
    # Element 0: test (Expression)
    # Element 1: body (Statement)
    link_expression(node=node.children[0], node_parent=node)
    node.set_control_dependency(extremity=node.children[1], label=True)
    extra_comment_node(node, 2)

# The comments just automatically link to a Statement node somewhere below them.
def extra_comment_node(node, max_children):
    """ If a comment has linked to a node. """
    if len(node.children) > max_children:
        if node.children[max_children].is_comment():
            node.set_comment_dependency(extremity=node.children[max_children])


def link_expression(node, node_parent):
    """ Non-statement node. """
    if node.is_comment():
        node_parent.set_comment_dependency(extremity=node)
    else:
        node_parent.set_statement_dependency(extremity=node)
    return node


def NonConditional_statement_cf(node):
    """ Non-conditional statements. """
    for child in node.children:
        if child.is_statement():
            node.set_control_dependency(extremity=child, label='e')
        else:
            link_expression(node=child, node_parent=node)


def break_statement_cf(node):
    """ BreakStatement, breaks the loop. """
    if_cond = node.control_dep_parents[0].extremity.control_dep_parents[0].extremity
    block_statmt = if_cond.control_dep_parents[0].extremity
    if_all = [elt.extremity for elt in block_statmt.control_dep_children]
    for i, _ in enumerate(if_all):
        if if_cond.id == if_all[i].id:
            break
    print(if_all)
    if_false = if_all[i+1:]
    print(if_false)
    for elt in if_false:
        print(if_cond.name)
        print(if_cond.id)
        print(elt.name)
        print(elt.id)
        if_cond.set_control_dependency(extremity=elt, label=False)
        block_statmt.remove_control_dependency(extremity=elt)





def try_cf(node):
    """ TryStatement. """
    # Element 0: block (Statement)
    # Element 1: handler (Statement) / finalizer (Statement)
    # Element 2: finalizer (Statement)
    node.set_control_dependency(extremity=node.children[0], label=True)
    if node.children[1].body == 'handler':
        node.set_control_dependency(extremity=node.children[1], label=False)
    else:  # finalizer
        node.set_control_dependency(extremity=node.children[1], label='e')
    if len(node.children) > 2:
        if node.children[2].body == 'finalizer':
            node.set_control_dependency(extremity=node.children[2], label='e')
            extra_comment_node(node, 3)
        else:
            extra_comment_node(node, 2)





def switch_cf(node):
    """ SwitchStatement. """
    # Element 0: discriminant
    # Element 1: cases (SwitchCase)

    switch_cases = node.children
    link_expression(node=switch_cases[0], node_parent=node)
    if len(switch_cases) > 1:
        # SwitchStatement -> True -> SwitchCase for first one
        node.set_control_dependency(extremity=switch_cases[1], label='e')
        switch_case_cf(switch_cases[1])
        for i in range(2, len(switch_cases)):
            if switch_cases[i].is_comment():
                node.set_comment_dependency(extremity=switch_cases[i])
            else:
                # SwitchCase -> False -> SwitchCase for the other ones
                switch_cases[i - 1].set_control_dependency(extremity=switch_cases[i], label=False)
                if i != len(switch_cases) - 1:
                    switch_case_cf(switch_cases[i])
                else:  # Because the last switch is executed per default, i.e. without condition 1st
                    switch_case_cf(switch_cases[i], last=True)
    # Otherwise, we could just have a switch(something) {}


def switch_case_cf(node, last=False):
    """ SwitchCase. """
    # Element 0: test
    # Element 1: consequent (Statement)
    nb_child = len(node.children)
    if nb_child > 1:
        if not last:  # As all switches but the last has to respect a condition to enter the branch
            link_expression(node=node.children[0], node_parent=node)
            j = 1
        else:
            j = 0
        for i in range(j, nb_child):
            if node.children[i].is_comment():
                node.set_comment_dependency(extremity=node.children[i])
            else:
                node.set_control_dependency(extremity=node.children[i], label=True)
    elif nb_child == 1:
        node.set_control_dependency(extremity=node.children[0], label=True)




def unstructured_statement_cf(node):
    """ For the unstructured nodes. """
    if node.name == 'ContinueStatement':
        continue_statement_cf(node)
    elif node.name == 'BreakStatement':
        break_statement_cf(node)

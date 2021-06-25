
class ExtendedAst:

    def __init__(self):
        self.type = None
        self.body = []
        self.source_type = None
        self.range = []
        self.comments = []
        self.tokens = []
        self.leading_comments = []

    def get_type(self):
        return self.type

    def set_type(self, root):
        self.type = root

    def get_body(self):
        return self.body

    def set_body(self, body):
        self.body = body

    def get_extended_ast(self):
        return {'type': self.get_type(), 'body': self.get_body(),
                'sourceType': self.get_source_type(), 'range': self.get_range(),
                'comments': self.get_comments(), 'tokens': self.get_tokens(),
                'leadingComments': self.get_leading_comments()}

    def get_ast(self):
        return {'type': self.get_type(), 'body': self.get_body()}

    def get_source_type(self):
        return self.source_type

    def set_source_type(self, source_type):
        self.source_type = source_type

    def get_range(self):
        return self.range

    def set_range(self, ast_range):
        self.range = ast_range

    def get_comments(self):
        return self.comments

    def set_comments(self, comments):
        self.comments = comments

    def get_tokens(self):
        return self.tokens

    def set_tokens(self, tokens):
        self.tokens = tokens

    def get_leading_comments(self):
        return self.leading_comments

    def set_leading_comments(self, leading_comments):
        self.leading_comments = leading_comments





class Dependence:

    def __init__(self, dependency_type, extremity, label, begin=None, end=None):
        self.type = dependency_type
        self.extremity = extremity
        self.id_begin = begin
        self.id_end = end
        self.label = label

    def get_type(self):
        return self.type

    def set_type(self, dependency_type):
        self.type = dependency_type

    def get_extremity(self):
        return self.extremity

    def set_extremity(self, extremity):
        self.extremity = extremity

    def get_id_begin(self):
        return self.id_begin

    def set_id_begin(self, id_begin):
        self.id_begin = id_begin

    def get_id_end(self):
        return self.id_end

    def set_id_end(self, id_end):
        self.id_end = id_end

    def get_label(self):
        return self.label

    def set_label(self, label):
        self.label = label

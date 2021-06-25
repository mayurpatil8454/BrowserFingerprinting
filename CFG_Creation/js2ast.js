var esprima = require("esprima");
var es = require("escodegen");
var fs = require("fs");


function jstoast(js, json_path) {
    var text = fs.readFileSync(js).toString('utf-8');
    var ast = esprima.parse(text,{range: true, tokens: true, comment: true}, function (node) {
        console.log(node.type);

    });
    console.log(ast)
    for (var i in ast.tokens) {
        console.log(ast.tokens[i].type)
    }

    if (json_path !== '1') {

        ast = es.attachComments(ast, ast.comments, ast.tokens);

        fs.writeFile(json_path, JSON.stringify(ast), function (err) {   ///Stroring the created AST to the file
            if (err) {
                console.error(err);
            }
            console.log("The AST has been successfully saved in " + json_path);
        });

        return ast;
    }
}

//jstoast('../Data/Browser_Fingerprint_Script_0001.js','ast.json');
jstoast(process.argv[2], process.argv[3]);

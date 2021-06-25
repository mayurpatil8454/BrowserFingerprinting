import requests
import pandas as py

RawData = py.read_csv(r"Excel.csv");
counter = 1;
Defaulter_Websites = [];
DataExcel = [];
for row in RawData.index:
    CurrentURL = RawData['URL'][row]
    if CurrentURL.find('.js') != -1 and CurrentURL.find('http') != -1:   # basic filtering
        # print(CurrentURL);
        try:   # Creating Session and Header
            s = requests.Session()
            s.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36';
            response = s.get(CurrentURL,timeout = 6.0);
        # Removing record which are not Not available
        except requests.ConnectionError as e:
            continue;
        except requests.Timeout as e:
            continue;
        except requests.TooManyRedirects as e:
            continue;

        if response.status_code == 200:
            FileName = "Data/Browser_Fingerprint_Script_" + str(counter) + ".js";   # Storing th files with names
            f = open(FileName, "w", encoding="utf-8")
            f.write(response.text + "")
            # Exdata = [CurrentURL,FileName,response.text.strip()];
            # DataExcel.append((Exdata));
            counter = counter + 1;
            # print(counter);
        else:
            Defaulter_Websites.append(CurrentURL);   # Extracting URL which found to have Not available
            # print(CurrentURL);

Defaulter_Websites_Data = py.DataFrame(Defaulter_Websites, columns=['Defaulter_URLs'])
Defaulter_Websites_Data.to_csv('Defaulter_Websites_Data.csv')

#
# DataExcelFile = py.DataFrame(DataExcel, columns=['URL','FileName','Data']);
# DataExcelFile.to_csv('DataExcel.csv');
            # print(CurrentURL);
            # print(response.content);
# CurrentURL = 'http://www.ti.com/utag/ti/main/prod/utag.200.js?utv=ut4.39.201906141355'
# if CurrentURL.find('.js') != -1:
#     try:
#         s = requests.Session()
#         s.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36';
#         response = s.get(CurrentURL,timeout = 6.0);
#         print(response.status_code);
#         if response.status_code == 200:
#             counter = 1
#             f = open("Data/malicious" + str(counter) + ".js", "w")
#             f.write(response.text + "")
#     except requests.ConnectionError as e :
#         print('a');
#     except requests.Timeout as e :
#         print("timeout")



node_types ={ 'ArrayExpression': 0,
    'ArrayPattern': 1,
    'ArrowFunctionExpression': 2,
    'AssignmentExpression': 3,
    'AssignmentPattern': 4,
    'AwaitExpression': 5,
    'BinaryExpression': 6,
    'BlockStatement': 7,
    'BreakStatement': 8,
    'CallExpression': 9,
    'CatchClause': 10,
    'ClassBody': 11,
    'ClassDeclaration': 12,
    'ClassExpression': 13,
    'ConditionalExpression': 14,
    'ContinueStatement': 15,
    'DebuggerStatement': 16,
    'DoWhileStatement': 17,
    'EmptyStatement': 18,
    'ExportAllDeclaration': 19,
    'ExportDefaultDeclaration': 20,
    'ExportNamedDeclaration': 21,
    'ExportSpecifier': 22,
    'ExpressionStatement': 23,
    'ForInStatement': 24,
    'ForOfStatement': 25,
    'ForStatement': 26,
    'FunctionDeclaration': 27,
    'FunctionExpression': 28,
    'Identifier': 29,
    'IfStatement': 30,
    'Import': 31,
    'ImportDeclaration': 32,
    'ImportDefaultSpecifier': 33,
    'ImportNamespaceSpecifier': 34,
    'ImportSpecifier': 35,
    'LabeledStatement': 36,
    'Literal': 37,
    'LogicalExpression': 38,
    'MemberExpression': 39,
    'MetaProperty': 40,
    'MethodDefinition': 41,
    'NewExpression': 42,
    'ObjectExpression': 43,
    'ObjectPattern': 44,
    'Program': 45,
    'Property': 46,
    'RestElement': 47,
    'ReturnStatement': 48,
    'SequenceExpression': 49,
    'SpreadElement': 50,
    'Super': 51,
    'SwitchCase': 52,
    'SwitchStatement': 53,
    'TaggedTemplateExpression': 54,
    'TemplateElement': 55,
    'TemplateLiteral': 56,
    'ThisExpression': 57,
    'ThrowStatement': 58,
    'TryStatement': 59,
    'UnaryExpression': 60,
    'UpdateExpression': 61,
    'VariableDeclaration': 62,
    'VariableDeclarator': 63,
    'WhileStatement': 64,
    'WithStatement': 65,
    'YieldExpression': 66,
    'Line': 67,
    'Block': 68,
    'String': 69,
    'Int': 70,
    'Numeric': 71,
    'Bool': 72,
    'Null': 73,
    'RegExp': 74
}


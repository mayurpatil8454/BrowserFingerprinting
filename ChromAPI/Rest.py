from flask import Flask,request,jsonify,Response
from flask_cors import CORS, cross_origin

import handlefiles as hf

import os;
SRC_PATH = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
cors = CORS(app);
app.config['CORS_HEADERS'] = 'Content-Type'

# gloabal variable
codesdf = {};
fpset = {};

@app.route('/',methods =['GET'])
def start():
    print("started");

@app.route('/BulkRequest', methods =['GET','POST'])
@cross_origin()
def BulkReq():
    val = request.get_json();
    srclist = val['srclist'];
    codelist = val['codelist'];
    result = hf.handlefiles(srclist, codelist);
    return jsonify(result);

@app.route('/setFPCode', methods =['GET','POST'])
@cross_origin()
def setFpCode():
    val = request.get_json();
    for key, value in val.items():
        global codesdf;
        if key not in codesdf:
            codesdf[key] = value;
    print(codesdf)
    return {}

@app.route('/getFPCode', methods =['GET','POST'])
@cross_origin()
def getFpCode():
    val = request.get_json();
    findarr = val['codesval'];

    object ={};
    global codesdf;
    for data in findarr:
        if data in codesdf:
            object[data] = codesdf[data];
    print(object);
    return jsonify(object)

@app.route("/getCSV",methods =['GET','POST'])
def getPlotCSV():
    with open(r""+os.path.join(SRC_PATH,"cachedata.csv") +"") as fp:
        csv = fp.read()
    # csv = '1,2,3\n4,5,6\n'
    return Response(
        csv,
        mimetype="text/csv",
        headers={"Content-disposition":
                 "attachment; filename=mydata.csv"})


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 8002))
    print(port);
    app.run(debug=True, host='0.0.0.0', port=port)
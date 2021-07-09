import requests;
import os;
import sys;
import shutil
from Rest import fpset;

SRC_PATH = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(SRC_PATH, '..','pdg_generation'));
import pdgs_generation as cfg;

sys.path.insert(0,os.path.join(SRC_PATH,'..','ModelCreation'))
import classifier as cl;

if not os.path.exists(os.path.join(SRC_PATH,"..","temp")):
    os.makedirs(os.path.join(SRC_PATH,"..","temp"))
import psutil

def handlefiles(srclist, codelist):

    records = dict()
    counter =0;
    results = dict();
    for val in codelist:
        if val not in fpset:
            FileName = os.path.join(SRC_PATH,"..","temp","Check" + str(counter)+".js");
            AnalyzedFileName = os.path.join(SRC_PATH,"..","temp","Analysis","CFG","Check" + str(counter)+ ".pbz2");
            records[val] = AnalyzedFileName
            f = open(FileName, "w+", encoding="utf-8")
            f.write(val + "")
            counter+=1;
        else:
            results[val] = fpset[val];
    for url in srclist:
        if url not in fpset:
            try:   # Creating Session and Header
                s = requests.Session()
                s.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36';
                response = s.get(url,timeout = 3.0);
            # Removing record which are not Not available
            except requests.ConnectionError as e:
                continue;
            except requests.Timeout as e:
                continue;
            except requests.TooManyRedirects as e:
                continue;
            if response.status_code == 200:
                FileName = os.path.join(SRC_PATH, "..", "temp", "Check" + str(counter)+".js");
                AnalyzedFileName = os.path.join(SRC_PATH, "..", "temp", "Analysis", "CFG", "Check" + str(counter) + ".pbz2");
                records[url] =AnalyzedFileName;
                f = open(FileName, "w+", encoding="utf-8")
                f.write(response.text + "");
                counter += 1;
        else:
            results[url] = fpset[url];
    #Calculate the CFG of all files
    cfg.store_cfg_folder(os.path.join(SRC_PATH,"..", "temp"));


    #Calculate the classification of files
    filename , value = cl.main_classification();

    results = reverseConnection(records,filename,value,results)
    #removefiles

    for root, dirs, files in os.walk(os.path.join(SRC_PATH,"..","temp")):
        for f in files:
            os.unlink(os.path.join(root, f))
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))

    return results;




def reverseConnection(records,filenames,value,results):
    print(filenames);
    arr =[];
    for filename in filenames:
        arr.append((filename.split(".."))[1])
    print(arr);
    for src, file in records.items():
        print(src,file);
        if (file.split(".."))[1] in arr:
            index = arr.index((file.split(".."))[1] );
            results[src] = value[index];
    print(results)
    return results;


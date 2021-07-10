import requests;
import os;
import sys;
import shutil;
import pandas as pd;
import hashlib;
import csv;

SRC_PATH = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(SRC_PATH, '..','pdg_generation'));
import pdgs_generation as cfg;

sys.path.insert(0,os.path.join(SRC_PATH,'..','ModelCreation'))
import classifier as cl;

if not os.path.exists(os.path.join(SRC_PATH,"..","temp")):
    os.makedirs(os.path.join(SRC_PATH,"..","temp"))
import psutil

def handlefiles(srclist, codelist):
    cacheData = pd.read_csv(r""+os.path.join(SRC_PATH,"cachedata.csv") +"");
    records = dict()
    counter =0;
    results = dict();
    for val in codelist:
        md5val = (hashlib.md5(val.encode('utf-8')).hexdigest())
        flag = True;
        for row in cacheData.index:
            if cacheData['data'][row] == md5val:
                results[val] = cacheData['res'][row];
                flag = False;
                break;
        if flag:
            FileName = os.path.join(SRC_PATH,"..","temp","Check" + str(counter)+".js");
            f = open(FileName, "w+", encoding="utf-8")
            f.write(val + "")

            f.close();
            sizelimit = os.path.getsize(os.path.join(SRC_PATH,"..","temp","Check" + str(counter)+".js"))
            if sizelimit < 2000000:
                AnalyzedFileName = os.path.join(SRC_PATH, "..", "temp", "Analysis", "CFG",
                                                "Check" + str(counter) + ".pbz2");
                records[val] = AnalyzedFileName;
                counter += 1;
            else:
                os.unlink(os.path.join(SRC_PATH,"..","temp","Check" + str(counter)+".js"))
        # else:
        #     results[val] = fpset[val];
    for url in srclist:
        flag = True;
        for row in cacheData.index:
            if cacheData['data'][row] == url:
                results[url] = cacheData['res'][row];
                flag = False;
                break;
        if flag:
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

                f = open(FileName, "w+", encoding="utf-8")
                f.write(response.text + "");

                f.close();
                sizelimit = os.path.getsize(os.path.join(SRC_PATH, "..", "temp", "Check" + str(counter) + ".js"))
                if sizelimit < 2000000:
                    AnalyzedFileName = os.path.join(SRC_PATH, "..", "temp", "Analysis", "CFG",
                                                    "Check" + str(counter) + ".pbz2");
                    records[url] = AnalyzedFileName;
                    counter += 1;
                else:
                    os.unlink(os.path.join(SRC_PATH, "..", "temp", "Check" + str(counter) + ".js"))
        # else:
        #     results[url] = fpset[url];
    #Calculate the CFG of all files
    if counter > 0:
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

    # for src, file in records.items():
    #     if src.startswith("https:") and src.endswith(".js"):
    #         for row in cacheData.index:


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
            index = arr.index((file.split(".."))[1]);
            results[src] = value[index];
            ## Storing in csv ##
            if src.startswith("https:") and ".js" in src:
                cacherow = [src, value[index]];
            else:
                md5val = (hashlib.md5(src.encode('utf-8')).hexdigest())
                cacherow = [md5val, value[index]];
            with open(r""+os.path.join(SRC_PATH,"cachedata.csv") +"", 'a') as f:
                writer = csv.writer(f)
                writer.writerow(cacherow)
    print(results)
    return results;


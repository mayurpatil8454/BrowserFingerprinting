import os
import hashlib
import pandas as py

HashArr =[];
Defaulter_Websites =[];
Fppath = '../Data';    # Creted Hash of the Fingerprinting Scripts
for r, d, f in os.walk(Fppath):
    for file in f:
        # print(os.path.join(r, file))
        with open(os.path.join(r, file), 'rb') as inputfile:
            data = inputfile.read()
            HashArr.append(hashlib.md5(data).hexdigest());

print(HashArr);
NonFPPath = '../Data1'    # Check for FP sccript in Normal Dataset
for r, d, f in os.walk(NonFPPath):
    for file in f:
        with open(os.path.join(r, file), 'rb') as inputfile:
            data = inputfile.read()
            dataHashed = hashlib.md5(data).hexdigest();
            if(any(word in dataHashed for word in HashArr)):
                Defaulter_Websites.append(file);

Defaulter_Websites_Data = py.DataFrame(Defaulter_Websites, columns=['Defaulter_URLs'])
Defaulter_Websites_Data.to_csv('FPScrInNonFP_Websites_Data.csv')
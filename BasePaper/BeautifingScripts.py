import jsbeautifier;
import os;
dirname =os.path.dirname(os.path.realpath(__file__))
Fppath = 'testingData'; #Beautifying fp files

for r, d, f in os.walk(Fppath):
    for file in f:
        # print(file);
        print(os.path.join(r, file))
        with open(os.path.join(r, file), 'rb') as inputfile:
            data = inputfile.read().decode('utf-8');
            try:
                res = jsbeautifier.beautify(data);
            except Exception:
                continue;
            f = open(os.path.join('testingData',file), "w")
            f.write(res);
            f.close()





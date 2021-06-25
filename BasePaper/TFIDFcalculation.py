from sklearn.feature_extraction.text import TfidfVectorizer,CountVectorizer
from sklearn.svm import OneClassSVM
from sklearn.metrics import confusion_matrix
import numpy as np
import os;


#Getting Each Line as feature
TrainSet = [];
Fppath = 'BeautifiedFPfiles'
for r, d, f in os.walk(Fppath):
    for file in f:
        with open(os.path.join(r, file), 'rb') as inputfile:
            line = inputfile.readlines();  # read all the lines in the files
            TrainSet.extend(line);
            inputfile.close()

#remove empty from lines
while("" in TrainSet) :
    TrainSet.remove("");

print(len(TrainSet));
tfidf = TfidfVectorizer(max_features=200)
TrainVectors = tfidf.fit_transform(TrainSet);


TestSet = [];
Fppath = 'testingData'
ytest = [];
for r, d, f in os.walk(Fppath):
    for file in f:
        with open(os.path.join(r, file), 'rb') as inputfile:
            if(file.startswith("B")):
                ytest.append(1);
            else:
                ytest.append(-1);
            line = inputfile.readlines();  # read all the lines in the files
            TestSet.extend(line);
            inputfile.close()
ytest = np.asarray(ytest);
# print(ytest);

#remove empty from corpus
while("" in TestSet) :
    TestSet.remove("");
TestVectors = tfidf.transform(TestSet);
print(len(TestSet))
#One Class SVM

print('modelTraining')
model = OneClassSVM(nu=0.1, kernel="rbf", gamma=0.1)
print(TrainVectors.shape)
model.fit(TrainVectors)

print('modelTesting')

test_predictions = model.predict(TestVectors)


tn, fp, fn, tp = confusion_matrix(ytest , test_predictions)

print("Accuracy" + str((tp+tn) / (tp+tn+fp+fn)))
print("tp " + str(tp) + "fp " + str(fp) + "fn "+ str(fn) + "tn " + str(tn) );




#
# ResponseStr = open(os.path.join(Fppath,'Browser_Fingerprint_Script_2.js')).readlines();
# response = tfidf.transform(ResponseStr);
# print(response);
# feature_array = tfidf.get_feature_names();
#
# n = 200
#
# print('tf_idf scores: \n', sorted(list(zip(tfidf.get_feature_names(),
#                                              response.sum(0).getA1())),
#                                  key=lambda x: x[1], reverse=True)[:n])
#
# Countidf = CountVectorizer()
# Counttfs = Countidf.fit_transform(corpus);
#
# feature_array = Countidf.get_feature_names();
# print('Frequency: \n', sorted(list(zip(Countidf.get_feature_names(),
#                                          Counttfs.sum(0).getA1())),
#                             key=lambda x: x[1], reverse=True)[:n])
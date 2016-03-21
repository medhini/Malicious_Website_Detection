import numpy as np
from sklearn import preprocessing
from sklearn import metrics
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
from sklearn.svm import SVC
from sklearn.externals import joblib

# load the CSV file as a numpy matrix
dataset = np.genfromtxt("f_vectors.csv", delimiter=',', skip_header=True)
dataset2= np.genfromtxt("f_vectors2.csv", delimiter=',', skip_header=True)
dataset=np.concatenate((dataset,dataset2))
# separate the data from the target attributes
X = dataset[:,0:8]
y = dataset[:,8]

# normalize the data attributes
nX = preprocessing.normalize(X)
# standardize the data attributes
sX = preprocessing.scale(X)

'''
model = ExtraTreesClassifier()
model.fit(X, y)
# display the relative importance of each attribute
print model.feature_importances_

print "........................."

model = LogisticRegression()
# create the RFE model and select 3 attributes
rfe = RFE(model, 3)
rfe = rfe.fit(X, y)
# summarize the selection of the attributes
print(rfe.support_)
print(rfe.ranking_)
'''
model = SVC()
model.fit(X, y)
print(model)
# make predictions
expected = y
predicted = model.predict(X)
# summarize the fit of the model
print(metrics.classification_report(expected, predicted))
print(metrics.confusion_matrix(expected, predicted))
#print X[0]
joblib.dump(model, 'trainmodel.pkl') 

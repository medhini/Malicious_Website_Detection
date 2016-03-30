import numpy as np
from sklearn import preprocessing
from sklearn import metrics
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import BernoulliNB
from sklearn.externals import joblib

# load the CSV file as a numpy matrix
dataset = np.genfromtxt("confusion.csv", delimiter=',', skip_header=True)
dataset2= np.genfromtxt("confusion2.csv", delimiter=',', skip_header=True)
dataset=np.concatenate((dataset,dataset2))
# separate the data from the target attributes
X = dataset[:,0:8]
y = dataset[:,8]

model=joblib.load("trainmodelmultinb.pkl")
expected = y
predicted = model.predict(X)
# summarize the fit of the model
print(metrics.classification_report(expected, predicted))
print(metrics.confusion_matrix(expected, predicted))
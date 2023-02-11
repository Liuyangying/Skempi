from sklearn.neural_network import MLPRegressor
import torch
import torch.nn.functional as F
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.cm as cm
import os
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import random
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import KFold
from sklearn.metrics import confusion_matrix
from sklearn import metrics
from scipy.spatial.distance import pdist,squareform
from sklearn.linear_model import LinearRegression
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.preprocessing import normalize
from sklearn import preprocessing
from torch.autograd import Variable
import torch.nn.functional as F
from scipy.stats import pearsonr, f_oneway
from scipy import stats
import statsmodels.api as sm
import scipy.stats as stats
import statsmodels.stats.multitest as smm
from linear_regression import load_data
from sklearn.neural_network import MLPClassifier
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import KFold
from joblib import dump
from sklearn.linear_model import LogisticRegression
from matplotlib import pyplot


np.random.seed(1000)

path = 'F:\\PycharmProjects\\combine_sheet\\Model\\all_features_normalized.csv'
train_percent = 0.8
xx,x,y_r,y_c=load_data(path)
#N = y_r.shape[0]
decrease = int(y_c[y_c==0].shape[0]*0.8)
increase = int(y_c[y_c==1].shape[0]*0.8)
decrease_index = np.where(y_c==0)[0]
np.random.shuffle(decrease_index)
increase_index = np.where(y_c==1)[0]
np.random.shuffle(increase_index)
#N_train = int(N*train_percent)
#index = np.arange(N)
#np.random.shuffle(index)
#train_index = index[0:N_train]
train_index = np.hstack((decrease_index[0:decrease],increase_index[0:increase]))
#test_index = index[N_train:]
test_index = np.hstack((decrease_index[decrease:],increase_index[increase:]))

train_feat = x[train_index,:]
train_target = y_r[train_index]
train_target_c = y_c[train_index]
test_feat = x[test_index,:]
test_target = y_r[test_index]
test_target_c = y_c[test_index]

mses_list = []
all_label = []
target=[]
pred_target=[]
features=[]


clf = LogisticRegression(solver='newton-cg',penalty='l2').fit(train_feat ,train_target_c)
clf.predict(test_feat)
pred_target_c_p = clf.predict_proba(test_feat)[:,1]
fpr, tpr, threshold = metrics.roc_curve(test_target_c, pred_target_c_p)
roc_auc = metrics.auc(fpr, tpr)
plt.figure(figsize=(6,6))
plt.title('ROC')
plt.plot(fpr, tpr, 'b', label = 'AUC = %0.3f' % roc_auc)
plt.legend(loc = 'lower right')
plt.plot([0, 1], [0, 1],'r--')
plt.xlim([0, 1])
plt.ylim([0, 1])
plt.ylabel('True Positive Rate')
plt.xlabel('False Positive Rate')
plt.show()


pred_target_c = clf.predict(test_feat)
print(train_target_c.shape[0], pred_target_c.shape[0])
print(metrics.classification_report(test_target_c, pred_target_c))
print(metrics.confusion_matrix(test_target_c, pred_target_c))


# get importance
plt.figure(figsize=(15,15))
importance = clf.coef_[0]
# summarize feature importance
for i,v in enumerate(importance):
	print('Feature: %0d, Score: %.5f' % (i,v))
# plot feature importance
pyplot.barh(np.array(xx.columns), importance)
pyplot.show()
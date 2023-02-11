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
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.inspection import permutation_importance
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import classification_report

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


params = {
          "n_estimators": 300,
          "max_depth": 30,
          "min_samples_split": 4,
          "learning_rate": 0.01,
          #"subsample": 0.8,
          "max_features": 'sqrt'
          }

gbdt = GradientBoostingClassifier(**params).fit(train_feat, train_target_c)
pred_target_c = gbdt.predict(test_feat)
print(train_target_c.shape[0], pred_target_c.shape[0])
print(metrics.classification_report(test_target_c, pred_target_c))
print(metrics.confusion_matrix(test_target_c, pred_target_c))

pred_target_c_p = gbdt.predict_proba(test_feat)[:,1]
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


test_score = np.zeros((params["n_estimators"],), dtype=np.float64)
for i, y_pred in enumerate(gbdt.staged_predict(test_feat)):
    test_score[i] = gbdt.loss_(test_target, y_pred)

fig = plt.figure(figsize=(6, 6))
plt.subplot(1, 1, 1)
plt.title("Loss")
plt.plot(
    np.arange(params["n_estimators"]) + 1,
    gbdt.train_score_,
    "b-",
    label="Training Set Loss",
)
plt.plot(
    np.arange(params["n_estimators"]) + 1, test_score, "r-", label="Test Set Loss"
)
plt.legend(loc="upper right")
plt.xlabel("Boosting Iterations")
plt.ylabel("Loss")
fig.tight_layout()
plt.show()


#_________________________________________________________________________________________________


feature_importance = gbdt.feature_importances_
sorted_idx = np.argsort(feature_importance)
pos = np.arange(sorted_idx.shape[0]) + 0.5
fig = plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.barh(pos, feature_importance[sorted_idx], align="center")
plt.yticks(pos, np.array(xx.columns)[sorted_idx])
plt.title("Feature Importance")

result = permutation_importance(
    gbdt, test_feat, test_target_c, n_repeats=10, random_state=42, n_jobs=2
)
sorted_idx = result.importances_mean.argsort()
plt.subplot(1, 2, 2)
plt.boxplot(
    result.importances[sorted_idx].T,
    vert=False,
    labels=np.array(xx.columns)[sorted_idx],
)
plt.title("Permutation Importance (test set)")
fig.tight_layout()
plt.show()

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

# params = {
#     "n_estimators": 500,
#     "max_depth": 8,
#     "min_samples_split": 10,
#     "learning_rate": 0.01,
#     "loss": "squared_error",
#     "subsample":0.8,
#     "max_features":'sqrt'
# }

params = {
    "n_estimators": 500,
    "max_depth": 25,
    "min_samples_split": 5,
    "learning_rate": 0.01,
    "loss": "squared_error",
    "subsample":0.8,
    "max_features":'sqrt'
}

gbdt = GradientBoostingRegressor(**params).fit(train_feat, train_target)
pred_target = gbdt.predict(test_feat)
#________________________________________________________________________________


# X = train_feat
# y = train_target
# X2 = sm.add_constant(X)
# est = sm.OLS(y, X2)
# est2 = est.fit()
# print(est2.summary())

test_target = test_target.reshape(-1)
pred_target = pred_target.reshape(-1)

corr, pval = pearsonr(test_target, pred_target)
print('Pearsons correlation: %.3f' % corr)
print('P value: ', pval)
mae = mean_absolute_error(test_target, pred_target)
print('mae: %.3f' % mae)
rmse = mean_squared_error(test_target, pred_target, squared=False)
mses_list.append(rmse)
print('test Rooted Mean squared error: %.5f' % rmse)
#The coefficient of determination: 1 is perfect prediction
print('test Coefficient of determination: %.5f'% r2_score(test_target, pred_target))


xmin_val = np.min(test_target)-1
ymin_val = np.min(pred_target)-1
xmax_val = np.max(test_target)+1#70
ymax_val = np.max(pred_target)+1
xmax_plot = xmax_val

fit_regr = LinearRegression()
fit_regr.fit(test_target.reshape((-1,1)), pred_target.reshape((-1,1)))
fit_input = np.asarray([xmin_val, xmax_plot]).reshape((-1,1))
fit_output = fit_regr.predict(fit_input)
plt.figure(figsize=(8, 8))
colors = ['red','green']
legends = ['ΔΔG<0','ΔΔG>0']
for i_class in range(0,2):
    plt.plot(test_target[test_target_c==i_class], pred_target[test_target_c==i_class],'o', label=legends[i_class])

#plt.plot(test_target,test_target, color='red')
plt.plot(fit_input,fit_output, label='Regression', color='red')
handles, labels = plt.gca().get_legend_handles_labels()
order = [1,0,2]
plt.legend([handles[idx] for idx in order],[labels[idx] for idx in order], loc='upper left', fontsize=20)
# plt.legend(legends+['Regression'], loc='upper left')
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.xlabel('Experimental ΔΔG', fontsize=25)
plt.ylabel('Predicted ΔΔG', fontsize=25)
plt.xlim([xmin_val, xmax_val])
plt.ylim([ymin_val, ymax_val])
# plt.savefig('cdr_sob.png',dpi=600,format='png')
# plt.savefig('cdr_sob.svg',dpi=600,format='svg')
plt.show()


#----------------------------------------------------------------------------------------------

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
    gbdt, test_feat, test_target, n_repeats=10, random_state=42, n_jobs=2
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

#_________________________________________________________________________________________________
test_target = test_target.reshape(-1)
pred_target = pred_target.reshape(-1)

corr, pval = pearsonr(test_target, pred_target)
print('Pearsons correlation: %.3f' % corr)
print('P value: ', pval)
mae = mean_absolute_error(test_target, pred_target)
print('mae: %.3f' % mae)
rmse = mean_squared_error(test_target, pred_target, squared=False)
mses_list.append(rmse)
print('test Mean squared error: %.5f' % rmse)
#The coefficient of determination: 1 is perfect prediction
print('test Coefficient of determination: %.5f'% r2_score(test_target, pred_target))
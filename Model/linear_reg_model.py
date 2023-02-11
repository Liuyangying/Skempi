# -*- coding: utf-8 -*-
"""
Created on Fri Sep 24 01:22:51 2021

@author: onepi
"""

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

regr = LinearRegression()
regr.fit(train_feat, train_target)
pred_target = regr.predict(test_feat)

X = train_feat
y = train_target
X2 = sm.add_constant(X)
est = sm.OLS(y, X2)
est2 = est.fit()
print(est2.summary())

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

#plt.savefig('mmse.svg',dpi=600,format='svg')

# break

# print(sum(mses_list) / len(mses_list))
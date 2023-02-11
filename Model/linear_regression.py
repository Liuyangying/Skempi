import pandas as pd #Data manipulation
import numpy as np #Data manipulation
import matplotlib.pyplot as plt # Visualization
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor

def load_data(path):

    df = pd.read_csv(path)

    xx = df.drop(['Unnamed: 0', 'WorkIndex', 'Unnamed: 1', 'Orig_G', 'Mut_G', 'Diff_G', 'Increasement'],
                      axis=1)
    x = df.drop(['Unnamed: 0', 'WorkIndex', 'Unnamed: 1', 'Orig_G', 'Mut_G', 'Diff_G', 'Increasement'],
                      axis=1).to_numpy()
    y_r = df['Diff_G'].to_numpy()
    y_c = df['Increasement'].to_numpy()

    return xx,x,y_r,y_c,




if __name__ == '__main__':

    path = 'F:\\PycharmProjects\\combine_sheet\\Model\\all_features_normalized.csv'
    x,y_r,y_c,df_x=load_data(path)

    X = df_x
    vif_info = pd.DataFrame()
    vif_info['VIF'] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
    vif_info['Column'] = X.columns
    vif_info.sort_values('VIF', ascending=False)
    print(vif_info[vif_info['VIF']>5])




    print('yes')
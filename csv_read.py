import pandas as pd
import os
import scipy as sp
import scipy.stats
from functions import *

def fitModel(model, datafile_name):
    #csv파일을 로드해 모델을 학습함
    #csv파일의 내부데이터 순서는 [['motionsensor_1', 'motionsensor_2', 'decibel_living', 'decibel_study', 'decibel_table']] 여야 함.
    data = pd.read_csv('./'+str(datafile_name)+'.csv')
    x_train = data[['motionsensor_1', 'motionsensor_2', 'decibel_living', 'decibel_study', 'decibel_table']]
    y_train = data['switch']
    model.fit(x_train, y_train,
              epochs=20,
              batch_size=10)
    return model

# 레이블에 해당하는 내용만을 CSV에서 읽어와 반환함.
def read_csv(filedir, labels):
    data = pd.read_csv(filedir)
    return data[labels]

# 파일의 모든 레이블을 반환함
def read_csv_label(filedir):
    data = pd.read_csv(filedir)
    print('return labels(columns) of the ' + str(filedir) + 'as below')
    print(data.columns.tolist())
    return data.columns.tolist()

# 중복을 제거한 배열을 반환함
def remove_duplicated(list):
    temp_list = []
    for item in list:
        if item not in temp_list:
            temp_list.append(item)
    return temp_list


# 데이터 읽어오기
filedir = "C:/Users/user/PycharmProjects/KICT_BuildingEnergyDataAnalysis/202203_buildinggraph/rawdata_mod.csv"
data = read_csv(filedir, read_csv_label(filedir))
print(data)
sort_list = remove_duplicated(data['건물용도'])
print(sort_list)

# 변환하지 않은 raw data로 플로팅팅
distribute_plot(data, '평균')

# 건축물 용도별로 데이터를 쪼갬
for purpose in sort_list:
    data_filtered = data[(data['건물용도'] == purpose)]
    print(data_filtered)

    # 변환하지 않은 raw data로 플로팅팅
    distribute_plot(data_filtered, '평균')
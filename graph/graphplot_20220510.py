import scipy as sp
import scipy.stats
import pymysql
import pandas as pd
from functions import *
import numpy as np

basedata = pd.read_csv('C:/Users/user/Downloads/대학교데이터 최종결과물_전기기준메타_v2.csv')
basedata = basedata[['mgmBldrgstPk', 'TOTAREA', 'Carbon_201401', 'Carbon_201402', 'Carbon_201403', 'Carbon_201404', 'Carbon_201405', 'Carbon_201406', 'Carbon_201407', 'Carbon_201408', 'Carbon_201409', 'Carbon_201410', 'Carbon_201411', 'Carbon_201412', 'Carbon_201501', 'Carbon_201502', 'Carbon_201503', 'Carbon_201504', 'Carbon_201505', 'Carbon_201506', 'Carbon_201507', 'Carbon_201508', 'Carbon_201509', 'Carbon_201510', 'Carbon_201511', 'Carbon_201512', 'Carbon_201601', 'Carbon_201602', 'Carbon_201603', 'Carbon_201604', 'Carbon_201605', 'Carbon_201606', 'Carbon_201607', 'Carbon_201608', 'Carbon_201609', 'Carbon_201610', 'Carbon_201611', 'Carbon_201612', 'Carbon_201701', 'Carbon_201702', 'Carbon_201703', 'Carbon_201704', 'Carbon_201705', 'Carbon_201706', 'Carbon_201707', 'Carbon_201708', 'Carbon_201709', 'Carbon_201710', 'Carbon_201711', 'Carbon_201712', 'Carbon_201801', 'Carbon_201802', 'Carbon_201803', 'Carbon_201804', 'Carbon_201805', 'Carbon_201806', 'Carbon_201807', 'Carbon_201808', 'Carbon_201809', 'Carbon_201810', 'Carbon_201811', 'Carbon_201812', 'Carbon_201901', 'Carbon_201902', 'Carbon_201903', 'Carbon_201904', 'Carbon_201905', 'Carbon_201906', 'Carbon_201907', 'Carbon_201908', 'Carbon_201909', 'Carbon_201910', 'Carbon_201911', 'Carbon_201912', 'Carbon_202001', 'Carbon_202002', 'Carbon_202003', 'Carbon_202004', 'Carbon_202005', 'Carbon_202006', 'Carbon_202007', 'Carbon_202008', 'Carbon_202009', 'Carbon_202010', 'Carbon_202011', 'Carbon_202012', 'Carbon_202101', 'Carbon_202102', 'Carbon_202103', 'Carbon_202104', 'Carbon_202105', 'Carbon_202106', 'Carbon_202107', 'Carbon_202108', 'Carbon_202109', 'Carbon_202110', 'Carbon_202111', 'Carbon_202112']]
basedata.set_index('mgmBldrgstPk', drop=True, inplace=True)
temperature_data = pd.read_csv('C:/Users/user/Downloads/ta_20220510173204.csv')
print(basedata)

data_arr = ['Carbon_201401', 'Carbon_201402', 'Carbon_201403', 'Carbon_201404', 'Carbon_201405', 'Carbon_201406', 'Carbon_201407', 'Carbon_201408', 'Carbon_201409', 'Carbon_201410', 'Carbon_201411', 'Carbon_201412', 'Carbon_201501', 'Carbon_201502', 'Carbon_201503', 'Carbon_201504', 'Carbon_201505', 'Carbon_201506', 'Carbon_201507', 'Carbon_201508', 'Carbon_201509', 'Carbon_201510', 'Carbon_201511', 'Carbon_201512', 'Carbon_201601', 'Carbon_201602', 'Carbon_201603', 'Carbon_201604', 'Carbon_201605', 'Carbon_201606', 'Carbon_201607', 'Carbon_201608', 'Carbon_201609', 'Carbon_201610', 'Carbon_201611', 'Carbon_201612', 'Carbon_201701', 'Carbon_201702', 'Carbon_201703', 'Carbon_201704', 'Carbon_201705', 'Carbon_201706', 'Carbon_201707', 'Carbon_201708', 'Carbon_201709', 'Carbon_201710', 'Carbon_201711', 'Carbon_201712', 'Carbon_201801', 'Carbon_201802', 'Carbon_201803', 'Carbon_201804', 'Carbon_201805', 'Carbon_201806', 'Carbon_201807', 'Carbon_201808', 'Carbon_201809', 'Carbon_201810', 'Carbon_201811', 'Carbon_201812', 'Carbon_201901', 'Carbon_201902', 'Carbon_201903', 'Carbon_201904', 'Carbon_201905', 'Carbon_201906', 'Carbon_201907', 'Carbon_201908', 'Carbon_201909', 'Carbon_201910', 'Carbon_201911', 'Carbon_201912', 'Carbon_202001', 'Carbon_202002', 'Carbon_202003', 'Carbon_202004', 'Carbon_202005', 'Carbon_202006', 'Carbon_202007', 'Carbon_202008', 'Carbon_202009', 'Carbon_202010', 'Carbon_202011', 'Carbon_202012', 'Carbon_202101', 'Carbon_202102', 'Carbon_202103', 'Carbon_202104', 'Carbon_202105', 'Carbon_202106', 'Carbon_202107', 'Carbon_202108', 'Carbon_202109', 'Carbon_202110', 'Carbon_202111', 'Carbon_202112']
for idx in data_arr:
    basedata[idx] = basedata[idx] / basedata['TOTAREA']

basedata = basedata.drop(labels=['TOTAREA'], axis=1)
print(basedata)

target_pk_arr = ['11620-100197744'] # 서울대
#target_pk_arr = ['11440-310']
target_pk_arr = ['11410-100186411'] # 이대
#target_pk_arr = ['11410-100185809'] # 연대

for idx in basedata.index.tolist():
    carbon_arr = basedata.loc[idx].values.tolist()
    temp_arr = [-0.7, 1.9, 7.9, 14, 18.9, 23.1, 26.1, 25.2, 22.1, 15.6, 9, -2.9, -0.9, 1, 6.3, 13.3, 18.9, 23.6, 25.8, 26.3, 22.4, 15.5, 8.9, 1.6, -3.2, 0.2, 7, 14.1, 19.6, 23.6, 26.2, 28, 23.1, 16.1, 6.8, 1.2, -1.8, -0.2, 6.3, 13.9, 19.5, 23.3, 26.9, 25.9, 22.1, 16.4, 5.6, -1.9, -4, -1.6, 8.1, 13, 18.2, 23.1, 27.8, 28.8, 21.5, 13.1, 7.8, -0.6, -0.9, 1, 7.1, 12.1, 19.4, 22.5, 25.9, 27.2, 22.6, 16.4, 7.6, 1.4, 1.6, 2.5, 7.7, 11.1, 18, 23.9, 24.1, 26.5, 21.4, 14.3, 8, -0.3, -2.4, 2.7, 9, 14.2, 17.1, 22.8, 28.1, 25.9, 22.6, 15.6, 8.2, 0.6]
    if idx in target_pk_arr:
        plt.scatter(temp_arr, carbon_arr, c='red', label=idx)
    else:
        plt.scatter(temp_arr, carbon_arr, c='blue', s=1.5)

plt.legend()
plt.show()



# plt.scatter(data)
# plt.show()


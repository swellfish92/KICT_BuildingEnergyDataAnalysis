import pandas as pd


filelist = ['result(raw_sum_divarea)_v6_20220425.xlsx', 'result(raw_sum)_v6_20220425.xlsx', 'result(toe_sum_divarea)_v6_20220425.xlsx', 'result(toe_sum)_v6_20220425.xlsx', 'result(Carbon_sum)_v6_20220425.xlsx', 'result(Carbon_sum_divarea)_v6_20220425.xlsx', 'result(EUI_sum)_v6_20220425.xlsx', 'result(EUI_sum_divarea)_v6_20220425.xlsx']


# 건축물 나이데이터를 로드해서 합침
age_data = pd.read_csv('Building_agedata.csv')
age_data.set_index('MGM_BLD_PK', drop=True, inplace=True)

print('data read')

for file in filelist:
    data = pd.read_excel('./' + file)
    data.drop(['USEAPR_DAY'], axis=1, inplace=True)
    data = data.join(age_data, how='left')
    data.to_excel('./updated_file/' + file)
    print(file + ' // finished!')
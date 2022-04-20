import pandas as pd
import seaborn as sns
#seaborn 패키지의 폰트 세팅
sns.set(font='NanumBarunGothic',
        rc={"axes.unicode_minus":False},
        style='whitegrid')

import scipy.stats as stats
from sklearn.preprocessing import StandardScaler  # 표준화 패키지 라이브러리
from sklearn.decomposition import PCA

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm


# matplotlib 패키지의 폰트 확인 및 세팅 (현재는 사용하지 않아 주석처리)
'''
# 폰트 확인부
font_list = [font.name for font in fm.fontManager.ttflist]
print(font_list)

# 폰트 세팅부
fm.get_fontconfig_fonts()
# font_location = '/usr/share/fonts/truetype/nanum/NanumGothicOTF.ttf'
font_location = 'C:/Windows/Fonts/NanumGothic.ttf'  # For Windows
font_name = fm.FontProperties(fname=font_location).get_name()
matplotlib.rc('font', family=font_name)
plt.rcParams['font.family'] = 'NanumBarunGothic'
'''

# pandas프레임워크를 사용한 상관계수 구하기
def corr_pandas(dataframe, savedir):
        result = dataframe.corr()
        result.to_excel(savedir)

import numpy as np
import time
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

def corr_total(data):

        # 최종파일에 집어넣기 위한 데이터의 키를 추출
        var = data.keys()
        # pandas 라이브러리로 상관계수를 구함. pierson_index는 나중에도 그냥 .index 메서드를 사용해 해결하므로 없앴음.(2022.04.20)
        pierson = data.corr()
        # 최종결과를 저장할 데이터프레임을 작성
        temp = pd.DataFrame(index=['X', 'Y', 'R2(SLP)', 'R2(LReg)'])

        # 데이터 키를 기준으로 이중 for문으로 각각의 아이템에 대한 상관관계를 구함
        for item in var:
                for second_item in var:
                        if item == second_item: # 동일아이템은 당연히 1(x=y)이니 무의미
                                continue
                        else:
                                try:
                                        temp2 = data[[item, second_item]]
                                        temp2 = temp2.dropna()
                                except:
                                        R2 = 'initial error'
                                        R_2 = 'initial error'

                                try:
                                        R2 = r2_score(temp2[item], temp2[second_item])
                                except:
                                        R2 = 'Scikit_learn Function Error'

                                try:
                                        # 추가분
                                        x_data = []
                                        y_data = []
                                        for element in temp2[second_item]:
                                                temp_single_list = [element]
                                                x_data.append(temp_single_list)
                                        for element in temp2[item]:
                                                temp_single_list = [element]
                                                y_data.append(temp_single_list)
                                        # print(temp2[second_item])
                                        # print(temp2[item])
                                        # print(x_data)
                                        # print(y_data)
                                        model = LinearRegression()
                                        model.fit(X=x_data, y=y_data)
                                        '''plt.title(item + '//' + second_item)
                                        plt.xlabel(second_item)
                                        plt.ylabel(item)
                                        plt.plot(x_data, y_data, 'k.')
                                        plt.grid(True)
                                        plt.plot(x_data, model.predict(x_data), color='r')
                                        #plt.show()
                                        plt.savefig('./office_energy/graphs/' + str(item) + '_' + str(second_item) + '.png')
                                        plt.clf()'''
                                        y_data_mean = np.mean(np.ravel(y_data))
                                        TSS = np.sum((np.ravel(y_data) - y_data_mean) ** 2)
                                        RSS = np.sum((np.ravel(y_data) - np.ravel(model.predict(x_data))) ** 2)
                                        R_2 = 1 - (RSS / TSS)
                                except:
                                        R_2 = 'Linear Regression error'

                                try:
                                        pierson_corr = pierson[item][pierson.index == second_item].to_list()[0]
                                        print('pierson corr = ' + str(pierson_corr))

                                except:
                                        pierson_corr = 'N/A'

                                temp = temp.append(pd.Series([item, second_item, R2, R_2, pierson_corr],
                                                             index=['X', 'Y', 'R2(SLP)', 'R2(LReg)', 'Pierson_Corr']),
                                                   ignore_index=True)

                                # temp = temp.append(pd.Series([item, second_item, "ERROR_OCCURED"], index=['X', 'Y', 'R2', 'R2(LReg)']), ignore_index=True)

# 전처리 부분에 대한 함수. 시트가 여러 개 있는 부분을 대응함
def load_excel_multisheet(filedir):
        return pd.read_excel(filedir, sheet_name=None, engine='openpyxl')

# 딕셔너리 내부 값으로 키 값을 찾음
def get_key(dict, val):
        for item in dict.keys():
                #print(id(dict[item]))
                #print(id(val))
                if id(dict[item]) == id(val):
                        return item
        raise ValueError

# ==============================================================================
# 여기부터는 개별 시트 전처리를 위한 함수. 하드코딩이므로 hardcode를 붙임!
# 하드코딩 기준 파일: 210316_energydata.xlsx
def sheetdata_trim_hardcode(sheet_data):
        # 건물명 데이터가 4번째 줄부터라는 믿음(?)을 가지고 3번째 줄까지를 잘라냄
        # 4번째 줄을 미리 잘라내서 저장해 둠 (추후 이것을 컬럼명으로 활용)
        list_old_header = sheet_data.iloc[2:3, :].values.tolist()[0]

        # 잘라낸 건물명을 편집함 (4번째 BS까지만 남기도록)
        list_new_header = []
        for item in list_old_header:
                if item == '2차분류 TAG':
                        list_new_header.append('2차분류 TAG')
                else:
                        splitted_item = item.split('-')
                        list_new_header.append(splitted_item[0] + '-' + splitted_item[1] + '-' + splitted_item[2] + '-' + splitted_item[3])

        # 5번째줄까지를(단위) 잘라냄. 단위가 kWh가 아닐 경우 여기를 손봐야 할 것.
        re_data = sheet_data.iloc[4:, :]
        # 미리 잘라 둔 건물코드로 컬럼을 재설정
        re_data.columns = list_new_header
        # 축반전으로 세로줄 인덱스를 맞춰준다
        re_data = re_data.transpose()
        # 컬럼 값을 날자 값으로 새로 지정
        list_new_header = re_data.iloc[0:1,:].values.tolist()[0]
        re_data.columns = list_new_header
        return re_data.iloc[1:,:]

# trim이 끝난 파일을 받아서 날짜별로 값을 더해 월별로 합쳐 준다.
def sheetdata_monthly_sum_hardcode(sheet_data, col_name):
        # 숫자 값이 아닌 것이 들어갔을 때 여기서 NaN값으로 자동 변경한다
        sheet_data.replace('.',np.nan, regex=True, inplace=True)
        # 일별사용량을 체크하기 위한 날자배열을 만듬
        date_arr = sheet_data.columns.values.tolist()
        #print(date_arr)
        building_arr = sheet_data.index.values.tolist()
        #print(building_arr)
        temp_res = []
        for iter in range(len(building_arr)):
                # 길이가 12인 0배열을 만듬 (각 월별 총사용량)
                res_month_arr = [0 for i in range(12)]
                # 날자배열별로 컬럼 값을 모두 더한 뒤, -으로 스플릿한 2번째 값 (즉, 월 값)의 넘버링에 해당하는 배열에 더한다
                for date in date_arr:
                        temp_addvalue = sheet_data[date][iter]
                        month_index = int(date.split('-')[1])-1
                        res_month_arr[month_index] = res_month_arr[month_index] + temp_addvalue
                #print(res_month_arr)
                temp_res.append(res_month_arr)
        # 결과로 데이터프레임을 만들고 컬럼, 인덱스 설정
        result = pd.DataFrame(temp_res, index=None)
        month_list = []
        for i in range(12):
                month_list.append(col_name + '_' + str(i+1))
        result.columns = month_list
        result.index = building_arr
        return result

multisheet_data = load_excel_multisheet('C:/Users/user/PycharmProjects/KICT_BuildingEnergyDataAnalysis/Pierson_analysis/210316_energydata.xlsx')
# 멀티시트 데이터 딕셔너리에서 전력이 아닌 것들을 드롭함
temp_list_for_del = []
for item in multisheet_data.keys():
        if '전력' not in item:
                temp_list_for_del.append(item)
for item in temp_list_for_del:
        del multisheet_data[item]

print(multisheet_data.keys())

# proc_res = sheetdata_trim_hardcode(multisheet_data)
# sheetdata_monthly_sum_hardcode(proc_res)

temp_arr_for_df = []
for sheet_data_keys in multisheet_data:
        sheet_data = multisheet_data[sheet_data_keys]
        proc_res = sheetdata_trim_hardcode(sheet_data)
        print(proc_res)
        final_res = sheetdata_monthly_sum_hardcode(proc_res, get_key(multisheet_data, sheet_data))
        print(final_res)
        temp_arr_for_df.append(final_res)

# 데이터프레임을 조인시킴
result = temp_arr_for_df[0]
for i in range(len(temp_arr_for_df) - 1):
        # 혹시 중첩이 있다면, 우항의 값에 dup을 붙인다.
        result = result.join(temp_arr_for_df[i + 1], how='outer', rsuffix='_dup')
print(result)
result.to_excel('C:/Users/user/PycharmProjects/KICT_BuildingEnergyDataAnalysis/Pierson_analysis/210316_energydata_result.xlsx')
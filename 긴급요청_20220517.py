import scipy as sp
import scipy.stats
import pymysql
import pandas as pd
from functions import *
import numpy as np

energy_db = pymysql.connect(
    user = 'swellfish_remote',
    passwd = 'atdt01410',
    host = '222.236.133.141',
    db = 'energy_data',
    charset = 'utf8'
)


# Cursor 세팅 및 Sql 쿼리 사전정의
cursor = energy_db.cursor(pymysql.cursors.DictCursor)

def load_sql(cursor, load_query):
    cursor.execute(load_query)
    result = cursor.fetchall()
    return pd.DataFrame(result)

# 공통부를 채우기 위한 함수(사용승인일 및 사용용도)
# df_1에 null이 있을 경우 df_2에서 가져와서 채움. null이 없으면 기본적으로 앞의 것을 신뢰함.
def fill_null(df_1, df_2, col_arr):
    fill_null_condition = lambda s1, s2: s2 if pd.isna(s1) is True else s1
    # print(col_arr)
    # print(df_1)
    # print(df_1.columns.tolist())
    # print(df_2)
    # print(df_2.columns.tolist())
    for index in col_arr:
        df_1[index] = df_1[index].combine(df_2[index], fill_null_condition)
    return df_1


def get_energy_column_string(energy_sort, year):
    months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
    temp_result = ''
    for month in months:
        temp_result = temp_result + '+' + energy_sort + '_' + str(year) + str(month)
    temp_result = temp_result[1:len(temp_result)]
    return temp_result

def get_coefficient_string(energy_sort, calc_type):
    # 계수계산값을 이곳에 저장토록 함. (추후 확장성을 위해)

    # 지역난방의 경우 단위가 여러 개임... 불러올 때 체크해야! (1MJ = 0.277778 kWh, 1 Gcal = 1162.22 kWh)

    coeff_dict = {
        'EUI':{                     # EUI단위는 kWh/m^2으로 통일했음.
            'ELEC':'*2.75',         # 원래 kWh라서 추가작업 필요 없음.
            'GAS':'*0.30558',    # 1 MJ/m^2 = 0.2778 kWh/m2\^2, *1.1*0.2778 = *0.30558
            'HEAT': '*0.2022384' # 1 MJ/m^2 = 0.2778 kWh/m2\^2, *0.728*0.2778 = *0.2022384
        },
        'Carbon':{              # 탄소배출량 단위는 Kg으로 통일했음.
            'ELEC': '*0.4598',  #0.4594 t*CO2eq/MWh = 0.4594 kg*CO2eq/kWh    **for reference: https://tips.energy.or.kr/diagnosis/qna_view.do?no=1796
            'GAS': '*0.056236', #56,100 kg*CO2eq/TJ = 0.056100 Kg*CO2eq/MJ  (1MJ = 10^-6 TJ)
            'HEAT': '*0.02928' #34,771 kg*CO2eq/TJ = 0.034771 Kg*CO2eq/MJ  (1MJ = 10^-6 TJ)
        },
        'raw': {
            'ELEC': '*1',
            'GAS': '*1',
            'HEAT': '*1'
        },
        'toe': {
            # 한국부동산원 기준계수로 데이터를 수정했음. '환산계수.xlsx'을 참조.
            'ELEC': '*0.000086',
            'GAS': '*0.00002388459',    #에너지원별로 toe의 환산계수가 다른데, 이를 맨 마지막에 곱하는 것 같음. 기타가 1.000이니 일단은 단위환산만 해 둔다.
            'HEAT': '*0.00002388459'    #(1toe = 10Gcal) 1MJ = 0.2778 kWh = 0.2778/1162.22 Gcal = 0.000239 Gcal = 0.0000239 toe
        }
    }
    return coeff_dict[calc_type][energy_sort]

def get_energy_data_col(dataframe):
    # 에너지사용량에 해당하는 칼럼값을 뽑아내는 메서드
    col_list = dataframe.columns.to_list()
    res_list = []
    # 맨 뒤 4자리가 숫자일 경우(데이터 형식이 'ELEC_CONVERGED_2014'같은 구조이므로) 목록에 넣어서 반환
    for item in col_list:
        if item[len(item)-4:len(item)].isdigit() == True:
            res_list.append(item)
    return res_list

def get_year_data_monthly_by_pk(pk_code, energy_sort, year_arr, calc_type, data_type, include_attr = True):
    # 속성정보 데이터를 로드
    query_for_attr = "SELECT * FROM " + str(energy_sort) + "_attribute WHERE MGM_BLD_PK = '" + str(pk_code) + "';"
    #print(query_for_attr)
    attr_data = load_sql(cursor, query_for_attr)
    #print(attr_data)
    attr_data.set_index('MGM_BLD_PK', drop=True, inplace=True)
    attr_column = attr_data.columns.to_list()

    for year in year_arr:
        # 쿼리설정: 에너지종류별, 계산타입(EUI, 탄소배출)별, 연도별 1월부터 12월까지
        query = "SELECT * FROM " + str(energy_sort) + '_' + str(year)  + " WHERE MGM_BLD_PK = '" + str(pk_code) + "';"
        data = load_sql(cursor, query)
        # MGM_BLD_PK를 인덱스로 설정
        data.set_index('MGM_BLD_PK', drop=True, inplace=True)
        # 그러고 나면 남는 것이 데이터 컬럼뿐인데, 여기에 계수를 곱해서 값을 연산한다.
        for col_name in data.columns:
            data[col_name] = data[col_name] * float(get_coefficient_string(energy_sort, calc_type).split('*')[1])
        # 속성정보 데이터와 병합
        attr_data = attr_data.join(data, how='outer')
    result = attr_data
    # # 속성정보 데이터와 묶음. MGM_BLD_PK외에 다른 데이터는 중복되는 것이 없도록 저장했으므로, 저장할 column은 따로 정하지 않는다.
    # result = attr_data.merge(data, how='outer', left_index=True, right_index=True)

    # data_type을 따라서 데이터 값을 처리함
    # sum: 12개월치의 총합 (면적고려X)
    # sum_divarea: 12개월치의 단위면적당 총합
    # average: 1년간의 월평균값 (면적고려X)
    # average_divarea: 1년간의 단위면적당 월평균값

    # 이상한 값을 적을 경우 강제로 sum_divarea로 변경
    if data_type not in ['raw', 'divarea']:
        print('ERROR: data_type is not correct. should be one of [raw|divarea]')
        print('ERROR: data_type is forced_set as raw to prevent further error')
        data_type = 'raw'

    if data_type == 'divarea':
        # 모든 값을 면적으로 나누는 메서드
        for data_col in get_energy_data_col(result):
            result[data_col] = result[data_col]/result['TOTAREA']


    # 속성정보 포함여부가 False일 경우 해당 데이터를 drop후 내보냄 (면적 등 정보가 과정상 필요하므로 마지막에 다시 지우는 방식을 채택)
    if include_attr != True:
        result = result.drop(attr_column, axis=1)

    return result

energy_type_arr = ['elec', 'gas', 'heat']
year_arr = ['2014', '2015', '2016', '2017', '2018', '2019', '2020']

for energy_type in energy_type_arr:
    for year in year_arr:
        table_name = energy_type + '_' + year
        query_str = "select * from " + table_name + " where MGM_BLD_PK in ('11110-647', '11215-23070', '11230-632', '11530-5576', '11680-74', '11110-100183537', '11680-410', '11410-100185809', '11470-100186127', '11710-228', '11590-14698', '11290-518', '11650-323', '11200-1225', '11560-1390', '11380-100290794', '11740-544', '11710-485', '11530-7681', '11140-176', '11350-14660', '11260-11032', '11560-33312', '11560-100251089', '11500-6410', '11500-100214588', '11230-100185458', '11230-29344', '11110-462', '11230-34287', '11590-100194692', '11470-100191796', '11740-4945', '11560-59', '11110-12058', '11170-171', '11560-100194494', '11620-20883', '11380-14367', '11410-21340', '11305-19037', '11260-25373', '11320-280', '11500-100318672', '11350-9982', '11140-14986', '11680-88', '11740-435', '11350-503', '11560-507', '11560-6251', '11215-18377', '11470-7821', '11545-12486', '11230-388', '11590-100191091');"
        temp_data = load_sql(cursor, query_str)
        temp_data.set_index('MGM_BLD_PK', drop=True, inplace=True)
        if year == '2014':
            energy_data = temp_data
        else:
            energy_data = energy_data.join(temp_data, how='outer')

    if energy_type == 'elec':
        final_data = energy_data
    else:
        final_data = final_data.join(energy_data, how='outer')

final_data.to_csv('병원데이터시트_20220517.csv')

raise IOError


base_data = pd.read_excel('C:/Users/user/Downloads/basedata_컨설팅.xlsx', engine='openpyxl', sheet_name='Sheet1')
print(base_data)
base_data.set_index('final_pk', drop=True, inplace=True)
energy_data = pd.read_csv('KICT_BuildingEnergyDataAnalysis/result(Carbon_sum)_v7_20220425.csv')
energy_data.set_index('MGM_BLD_PK', drop=True, inplace=True)
res = base_data.join(energy_data, how='left')

res.to_csv('컨설팅건물결과.csv', encoding='utf-8 sig')
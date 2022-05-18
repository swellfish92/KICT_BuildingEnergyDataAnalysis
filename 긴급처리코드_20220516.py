import scipy as sp
import scipy.stats
import pymysql
import pandas as pd
from functions import *
import numpy as np
import sqlalchemy

from functions import *

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

def get_year_data_monthly_by_pk(pk_code_arr, energy_sort, year_arr, calc_type, data_type, include_attr = True):
    # # 속성정보 데이터를 로드
    # query_for_attr = "SELECT * FROM " + str(energy_sort) + "_attribute WHERE MGM_BLD_PK = '" + str(pk_code_arr) + "';"
    # print(query_for_attr)
    # attr_data = load_sql(cursor, query_for_attr)
    # print(attr_data)
    # attr_data.set_index('MGM_BLD_PK', drop=True, inplace=True)
    # attr_column = attr_data.columns.to_list()

    for year in year_arr:
        # 쿼리설정: 에너지종류별, 계산타입(EUI, 탄소배출)별, 연도별 1월부터 12월까지
        query = "SELECT * FROM " + str(energy_sort) + '_' + str(year)  + " WHERE MGM_BLD_PK = '" + str(pk_code_arr) + "';"
        data = load_sql(cursor, query)
        print(data)
        # MGM_BLD_PK를 인덱스로 설정
        data.set_index('MGM_BLD_PK', drop=True, inplace=True)
        # 그러고 나면 남는 것이 데이터 컬럼뿐인데, 여기에 계수를 곱해서 값을 연산한다.
        for col_name in data.columns:
            data[col_name] = data[col_name] * float(get_coefficient_string(energy_sort, calc_type).split('*')[1])
        # # 속성정보 데이터와 병합
        # attr_data = attr_data.join(data, how='outer')
    result = data
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


    # # 속성정보 포함여부가 False일 경우 해당 데이터를 drop후 내보냄 (면적 등 정보가 과정상 필요하므로 마지막에 다시 지우는 방식을 채택)
    # if include_attr != True:
    #     result = result.drop(attr_column, axis=1)

    return result


base_data = pd.read_csv('basedata_서울시400.csv')
base_data.set_index('MGM_BLD_PK', drop=True, inplace=True)
carbon_data = pd.read_csv('./updated_file/result(Carbon_sum)_v7_20220425.csv')
carbon_data.set_index('MGM_BLD_PK', drop=True, inplace=True)
base_data = base_data.join(carbon_data, how='left')

base_data['Avg_2017'] = base_data['HEAT_converged_Carbon_sum_2017'].fillna(0)+base_data['ELEC_converged_Carbon_sum_2017'].fillna(0)+base_data['GAS_converged_Carbon_sum_2017'].fillna(0)
base_data['Avg_2018'] = base_data['HEAT_converged_Carbon_sum_2018'].fillna(0)+base_data['ELEC_converged_Carbon_sum_2018'].fillna(0)+base_data['GAS_converged_Carbon_sum_2018'].fillna(0)
base_data['Avg_2019'] = base_data['HEAT_converged_Carbon_sum_2019'].fillna(0)+base_data['ELEC_converged_Carbon_sum_2019'].fillna(0)+base_data['GAS_converged_Carbon_sum_2019'].fillna(0)
base_data['total_Avg'] = (base_data['Avg_2017']+base_data['Avg_2018']+base_data['Avg_2019'])/3

base_data.to_csv('서울시400개_2017_2019_3년평균.csv', encoding='utf-8 sig')

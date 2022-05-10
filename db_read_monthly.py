import scipy as sp
import scipy.stats
import pymysql
import pandas as pd
from functions import *
import numpy as np

energy_db = pymysql.connect(
    user = 'root',
    passwd = 'atdt01410',
    host = '127.0.0.1',
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
            'GAS':'*1.1*0.2778',    # 1 MJ/m^2 = 0.2778 kWh/m2\^2
            'HEAT': '*0.728*0.2778' # 1 MJ/m^2 = 0.2778 kWh/m2\^2
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


def get_year_data_monthly_by_pk(pk_code, energy_sort, year_arr, calc_type, include_attr = True):
    # 속성정보 데이터를 로드
    query_for_attr = "SELECT * FROM " + str(energy_sort) + "_attribute WHERE MGM_BLD_PK = '" + pk_code + "';"
    attr_data = load_sql(cursor, query_for_attr)
    attr_data.set_index('MGM_BLD_PK', drop=True, inplace=True)
    attr_column = attr_data.columns.to_list()

    # 쿼리설정: 에너지종류별, 계산타입(EUI, 탄소배출)별, 연도별 1월부터 12월까지
    query = "SELECT MGM_BLD_PK, (" + get_energy_column_string(energy_sort, year) + ")" + get_coefficient_string(energy_sort, calc_type) + " AS " + energy_sort + "_converged_" + calc_type + "_" + data_type + "_" + year + " FROM " + str(energy_sort) + '_' + str(year)
    data = load_sql(cursor, query)
    # MGM_BLD_PK를 인덱스로 설정
    data.set_index('MGM_BLD_PK', drop=True, inplace=True)

    # 속성정보 데이터와 묶음. MGM_BLD_PK외에 다른 데이터는 중복되는 것이 없도록 저장했으므로, 저장할 column은 따로 정하지 않는다.
    result = attr_data.merge(data, how='outer', left_index=True, right_index=True)

    # data_type을 따라서 데이터 값을 처리함
    # sum: 12개월치의 총합 (면적고려X)
    # sum_divarea: 12개월치의 단위면적당 총합
    # average: 1년간의 월평균값 (면적고려X)
    # average_divarea: 1년간의 단위면적당 월평균값

    # 이상한 값을 적을 경우 강제로 sum_divarea로 변경
    if data_type not in ['sum', 'sum_divarea', 'average', 'average_divarea']:
        print('ERROR: data_type is not correct. should be one of [sum|sum_divarea|average|average_divarea]')
        print('ERROR: data_type is forced_set as sum_divarea to prevent further error')
        data_type = 'sum_divarea'

    if data_type == 'sum_divarea' or data_type == 'average_divarea':
        # 모든 값을 면적으로 나누는 메서드
        for data_col in get_energy_data_col(result):
            result[data_col] = result[data_col]/result['TOTAREA']

    if data_type == 'average' or data_type == 'average_divarea':
        # 모든 값을 12로 나누는 메서드
        for data_col in get_energy_data_col(result):
            result[data_col] = result[data_col]/12

    # 속성정보 포함여부가 False일 경우 해당 데이터를 drop후 내보냄 (면적 등 정보가 과정상 필요하므로 마지막에 다시 지우는 방식을 채택)
    if include_attr != True:
        result = result.drop(attr_column, axis=1)

    return result

def get_attr_data_only(energy_sort):
    # 속성정보 데이터를 로드
    query_for_attr = "SELECT * FROM " + str(energy_sort) + '_attribute'
    attr_data = load_sql(cursor, query_for_attr)
    attr_data.set_index('MGM_BLD_PK', drop=True, inplace=True)
    return attr_data

def get_year_data_multi(energy_sort, year_arr, calc_type, data_type = 'sum', include_attr = True):
    # 속성정보 데이터를 로드
    query_for_attr = "SELECT * FROM " + str(energy_sort) + '_attribute'
    attr_data = load_sql(cursor, query_for_attr)
    attr_data.set_index('MGM_BLD_PK', drop=True, inplace=True)
    attr_column = attr_data.columns.to_list()

    # 연도별 데이터를 로드하고, 배열에 저장
    temp_result = []
    for year in year_arr:
        query = "SELECT MGM_BLD_PK, (" + get_energy_column_string(energy_sort, year) + ")" + get_coefficient_string(energy_sort, calc_type) + " AS  " + energy_sort + "_converged_" + calc_type + "_" + data_type + "_"  + year + " FROM " + str(energy_sort) + '_' + str(year)
        temp_data = load_sql(cursor, query)

        # MGM_BLD_PK를 인덱스로 설정
        temp_data.set_index('MGM_BLD_PK', drop=True, inplace=True)

        temp_result.append(temp_data)

    # 배열의 데이터프레임을 MGM_BLD_PK 기준으로 병합. MGM_BLD_PK외에 다른 데이터는 중복되는 것이 없도록 저장했으므로, 저장할 column은 따로 정하지 않는다.
    for item in temp_result:
        attr_data = attr_data.merge(item, how='outer', left_index=True, right_index=True)
        #print(attr_data.columns.tolist())
    result = attr_data
    print(result.columns.tolist())
    # data_type을 따라서 데이터 값을 처리함
    # sum: 12개월치의 총합 (면적고려X)
    # sum_divarea: 12개월치의 단위면적당 총합
    # average: 1년간의 월평균값 (면적고려X)
    # average_divarea: 1년간의 단위면적당 월평균값

    # 이상한 값을 적을 경우 강제로 sum_divarea로 변경
    if data_type not in ['sum', 'sum_divarea', 'average', 'average_divarea']:
        print('ERROR: data_type is not correct. should be one of [sum|sum_divarea|average|average_divarea]')
        print('ERROR: data_type is forced_set as sum_divarea to prevent further error')
        data_type = 'sum_divarea'

    if data_type == 'sum_divarea' or data_type == 'average_divarea':
        # 모든 값을 면적으로 나누는 메서드
        for data_col in get_energy_data_col(result):
            result[data_col] = result[data_col]/result['TOTAREA']

    if data_type == 'average' or data_type == 'average_divarea':
        # 모든 값을 12로 나누는 메서드
        for data_col in get_energy_data_col(result):
            result[data_col] = result[data_col]/12

    # 속성정보 포함여부가 False일 경우 해당 데이터를 drop후 내보냄 (면적 등 정보가 과정상 필요하므로 마지막에 다시 지우는 방식을 채택)
    if include_attr != True:
        result = result.drop(attr_column, axis=1)

    return result

def read_and_export_excel(calc_type, data_type):
    # 통합파일 출력을 위한 구문 개선버전
    heat_data = get_year_data_multi('HEAT', ['2014', '2015', '2016', '2017', '2018', '2019', '2020'], calc_type, data_type=data_type)
    elec_data = get_year_data_multi('ELEC', ['2014', '2015', '2016', '2017', '2018', '2019', '2020'], calc_type, data_type=data_type, include_attr=False)
    gas_data = get_year_data_multi('GAS', ['2014', '2015', '2016', '2017', '2018', '2019', '2020'], calc_type, data_type=data_type, include_attr=False)
    elec_attr = get_attr_data_only("ELEC")
    gas_attr = get_attr_data_only("GAS")

    result = heat_data
    result = result.join(elec_data, how='outer')
    result = result.join(gas_data, how='outer')
    print(elec_attr)
    print(elec_attr.columns.tolist())
    print(result.columns.tolist())
    result = fill_null(result, elec_attr, elec_attr.columns.tolist())
    result = fill_null(result, gas_attr, gas_attr.columns.tolist())

    # inf(TOTAREA가 0인 경우)를 제거함.
    result[get_energy_data_col(result)].replace(np.inf,0)
    result[get_energy_data_col(result)].replace(-1*np.inf, 0)
    # 이게 작동을 안 해서 일단 수동으로 때웠음...... (엑셀 Ctrl+R)

    print(result)

    # 대충 이게 4분쯤 걸림.
    result.to_excel('result(' + str(calc_type) + '_' + str(data_type) + ')_v6_20220425.xlsx')

    print('Finished!')
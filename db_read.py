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

sql_gas = "SELECT MGM_BLD_PK, USEAPR_DAY, MAIN_PURPS_NM, (GAS_202004 + GAS_202005 + GAS_202006 + GAS_202007 + GAS_202008 + GAS_202009 + GAS_202010 + GAS_202011 + GAS_202012 + GAS_202101 + GAS_202102 + GAS_202103)*1.1/TOTAREA AS GAS_converged_EUI FROM gas"
sql_elec = "SELECT MGM_BLD_PK, USEAPR_DAY, MAIN_PURPS_NM, (ELEC_202004 + ELEC_202005 + ELEC_202006 + ELEC_202007 + ELEC_202008 + ELEC_202009 + ELEC_202010 + ELEC_202011 + ELEC_202012 + ELEC_202101 + ELEC_202102 + ELEC_202103)*2.75/TOTAREA AS ELEC_converged_EUI FROM elec"
sql_heat = "SELECT MGM_BLD_PK, USEAPR_DAY, MAIN_PURPS_NM, (HEAT_202004 + HEAT_202005 + HEAT_202006 + HEAT_202007 + HEAT_202008 + HEAT_202009 + HEAT_202010 + HEAT_202011 + HEAT_202012 + HEAT_202101 + HEAT_202102 + HEAT_202103)*0.728/TOTAREA AS HEAT_converged_EUI FROM heat"

def load_sql(cursor, load_query):
    cursor.execute(load_query)
    result = cursor.fetchall()
    return pd.DataFrame(result)

# 공통부를 채우기 위한 함수(사용승인일 및 사용용도)
# df_1에 null이 있을 경우 df_2에서 가져와서 채움. null이 없으면 기본적으로 앞의 것을 신뢰함.
def fill_null(df_1, df_2, col_arr):
    fill_null_condition = lambda s1, s2: s2 if pd.isna(s1) is True else s1
    print(col_arr)
    print(df_1.columns.tolist())
    print(df_2.columns.tolist())
    for index in col_arr:
        df_1[index] = df_1[index].combine(df_2[index], fill_null_condition)
    return df_1

def get_fulldata():
    gas_data = load_sql(cursor, sql_gas)
    elec_data = load_sql(cursor, sql_elec)
    heat_data = load_sql(cursor, sql_heat)
    gas_data.set_index('MGM_BLD_PK', drop=True, inplace=True)
    elec_data.set_index('MGM_BLD_PK', drop=True, inplace=True)
    heat_data.set_index('MGM_BLD_PK', drop=True, inplace=True)
    # print(gas_data)
    # print(elec_data)
    # print(heat_data)

    # 코드 가독성을 위해 gas_data를 복사한 다음 elec_data, heat_data와 각각 머징
    result = gas_data

    result = result.merge(elec_data['ELEC_converged_EUI'], how='outer', left_index=True, right_index=True)
    result = fill_null(result, elec_data, ['USEAPR_DAY', 'MAIN_PURPS_NM'])

    result = result.merge(heat_data['HEAT_converged_EUI'], how='outer', left_index=True, right_index=True)
    result = fill_null(result, heat_data, ['USEAPR_DAY', 'MAIN_PURPS_NM'])

    # EUI의 총합을 계산해서 합산
    # fillna로 NaN 데이터값을 0으로 치환(합만 구해서 사용하므로)
    result['GAS_converged_EUI'] = result['GAS_converged_EUI'].fillna(0)
    result['ELEC_converged_EUI'] = result['ELEC_converged_EUI'].fillna(0)
    result['HEAT_converged_EUI'] = result['HEAT_converged_EUI'].fillna(0)
    result['total_converged_EUI'] = result['GAS_converged_EUI'] + result['ELEC_converged_EUI'] + result['HEAT_converged_EUI']

    print('full data loaded')
    print(result.head())
    return result

#get_fulldata()


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
            'ELEC': '*0.4594',  #0.4594 t*CO2eq/MWh = 0.4594 kg*CO2eq/kWh    **for reference: https://tips.energy.or.kr/diagnosis/qna_view.do?no=1796
            'GAS': '*0.056100', #56,100 kg*CO2eq/TJ = 0.056100 Kg*CO2eq/MJ  (1MJ = 10^-6 TJ)
            'HEAT': '*0.034771' #34,771 kg*CO2eq/TJ = 0.034771 Kg*CO2eq/MJ  (1MJ = 10^-6 TJ)
        },
        'raw': {
            'ELEC': '*1',
            'GAS': '*1',
            'HEAT': '*1'
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


def get_year_data(energy_sort, year, calc_type, data_type = 'sum', include_attr = True):
    # 속성정보 데이터를 로드
    query_for_attr = "SELECT * FROM " + str(energy_sort) + '_attribute'
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
        print(attr_data.columns.tolist())
    result = attr_data

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
    result = fill_null(result, elec_attr, elec_attr.columns.tolist())
    result = fill_null(result, gas_attr, gas_attr.columns.tolist())

    # inf(TOTAREA가 0인 경우)를 제거함.
    result[get_energy_data_col(result)].replace(np.inf,0)
    result[get_energy_data_col(result)].replace(-1*np.inf, 0)
    # 이게 작동을 안 해서 일단 수동으로 때웠음...... (엑셀 Ctrl+R)

    print(result)

    # 대충 이게 4분쯤 걸림.
    result.to_excel('result(' + str(calc_type) + '_' + str(data_type) + ')_v3.xlsx')

    print('Finished!')



read_and_export_excel('EUI', 'sum_divarea')
#read_and_export_excel('EUI', 'sum')
read_and_export_excel('Carbon', 'sum_divarea')
#read_and_export_excel('Carbon', 'sum')



def get_certain_data(year_arr, calc_type, data_type):
    # 데이터를 뽑아서 그래프플로팅용으로 건네주는 메서드. 편집은 이곳에서~
    heat_data = get_year_data_multi('HEAT', year_arr, calc_type, data_type=data_type)
    elec_data = get_year_data_multi('ELEC', year_arr, calc_type, data_type=data_type, include_attr=False)
    gas_data = get_year_data_multi('GAS', year_arr, calc_type, data_type=data_type, include_attr=False)
    elec_attr = get_attr_data_only("ELEC")
    gas_attr = get_attr_data_only("GAS")
    result = heat_data
    result = result.join(elec_data, how='outer')
    result = result.join(gas_data, how='outer')
    result = fill_null(result, elec_attr, elec_attr.columns.tolist())
    result = fill_null(result, gas_attr, gas_attr.columns.tolist())
    # get_energy_data_col 로 에너지 칼럼을 뽑음
    energy_data_col = get_energy_data_col(result)

    # energy_data_col의 길이는 연도배열의 3배 (1년당 전기/가스/난방의 3개씩이므로) 여야 함. 아닐 경우 에러 처리
    if len(energy_data_col) != len(year_arr)*3:
        print("ERROR: length of energy_data_col selected is not matching with the number of data cols :")
        print(energy_data_col)
        import sys
        sys.exit()

    # NaN값은 0으로 바꾸고 싹 더해서 최종결과를 뽑아줌
    result['total_converged_EUI'] = 0
    for column in energy_data_col:
        result['total_converged_EUI'] = result['total_converged_EUI'] + result[column].fillna(0)

    # 기존 플로팅 코드 호환을 위해 걍 0으로 통일한 UseAprDay값 삽입
    result['USEAPR_DAY'] = 0
    print(result.head())

    # result_r = result['total_converged_EUI']
    # result_r = result_r[(result['total_converged_EUI']>0) & (result['total_converged_EUI']<999999999999999999999999999999999)]
    return result

# 평균 구하는 코드
# data_2020 = get_certain_data(['2020'], 'Carbon', 'sum_divarea')
# data_2019 = get_certain_data(['2019'], 'Carbon', 'sum_divarea')
# data_2018 = get_certain_data(['2018'], 'Carbon', 'sum_divarea')
# data_2017 = get_certain_data(['2017'], 'Carbon', 'sum_divarea')
# print('yearly mean from 2017 to 2020')
# print(data_2017.mean())
# print(data_2018.mean())
# print(data_2019.mean())
# print(data_2020.mean())
#
# temp_list = []
# print('yearly mean from 2017 to 2020_222222')
# for item in data_2017.values.tolist():
#     temp_list.append(item)
#
# print(sum(temp_list) / len(temp_list))
# temp_list = []
#
# for item in data_2018.values.tolist():
#     temp_list.append(item)
#
# print(sum(temp_list) / len(temp_list))
# temp_list = []
#
# for item in data_2019.values.tolist():
#     temp_list.append(item)
#
# print(sum(temp_list) / len(temp_list))
# temp_list = []
#
# for item in data_2020.values.tolist():
#     temp_list.append(item)
#
# print(sum(temp_list) / len(temp_list))
#
# temp_list = []
# for item in data_2017.values.tolist():
#     temp_list.append(item)
# for item in data_2018.values.tolist():
#     temp_list.append(item)
# for item in data_2019.values.tolist():
#     temp_list.append(item)
# print('mean for 2017-2019')
# print(sum(temp_list)/len(temp_list))
#
# # k.to_excel('RESULT_FOR_TEST2.xlsx')

# 통합파일 출력구문의 legacy code(혹시 몰라 남겨둠)
'''def merge_dataframe(df_left, df_right):
    fill_null_condition = lambda s1, s2: s2 if pd.isna(s1) is True else s1
    df_left = df_left.combine(df_right, fill_null_condition)
    print(df_left)
    df_left = fill_null(df_left, df_right, df_right.columns.tolist())
    print(df_left)
    return df_left


elec_data = get_year_data_multi('ELEC', ['2014', '2015', '2016', '2017', '2018', '2019', '2020'], 'Carbon', data_type='sum_divarea')
gas_data = get_year_data_multi('GAS', ['2014', '2015', '2016', '2017', '2018', '2019', '2020'], 'Carbon', data_type='sum_divarea')
heat_data = get_year_data_multi('HEAT', ['2020', '2021'], 'Carbon', data_type='sum_divarea')


print(elec_data)
print(gas_data)
print(heat_data)


# fill_null 을 위한 채울 기본속성 배열을 작성
fill_arr = ['BLD_TYPE_GB_CD', 'REGSTR_GB_CD', 'REGSTR_KIND_CD', 'SIGUNGU_NM', 'BJDONG_NM', 'PLAT_GB_CD', 'BUN', 'JI', 'JUSO', 'ROAD_JUSO', 'TOTAREA', 'HHLD_CNT', 'MAIN_PURPS_NM', 'UNIT_CD']

# 코드 가독성을 위해 heat_data를 복사한 다음 elec_data, gas_data와 각각 머징
result = heat_data
print('==============================================================================')
print(elec_data.columns.tolist())
print('==============================================================================')
result = merge_dataframe(result, elec_data)
print(result)
result = merge_dataframe(result, gas_data)
print(result)

result.to_excel('final_result_of_all_data.xlsx')'''





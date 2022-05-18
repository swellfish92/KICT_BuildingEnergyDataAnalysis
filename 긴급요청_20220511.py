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

result_col_arr = ['BLD_TYPE_GB_CD', 'REGSTR_GB_CD', 'REGSTR_KIND_CD', 'SIGUNGU_NM', 'BJDONG_NM', 'PLAT_GB_CD', 'BUN', 'JI', 'JUSO', 'ROAD_JUSO', 'TOTAREA', 'HHLD_CNT', 'MAIN_PURPS_NM', 'UNIT_CD', 'USEAPR_DAY', 'ELEC_201401', 'ELEC_201402', 'ELEC_201403', 'ELEC_201404', 'ELEC_201405', 'ELEC_201406', 'ELEC_201407', 'ELEC_201408', 'ELEC_201409', 'ELEC_201410', 'ELEC_201411', 'ELEC_201412', 'ELEC_201501', 'ELEC_201502', 'ELEC_201503', 'ELEC_201504', 'ELEC_201505', 'ELEC_201506', 'ELEC_201507', 'ELEC_201508', 'ELEC_201509', 'ELEC_201510', 'ELEC_201511', 'ELEC_201512', 'ELEC_201601', 'ELEC_201602', 'ELEC_201603', 'ELEC_201604', 'ELEC_201605', 'ELEC_201606', 'ELEC_201607', 'ELEC_201608', 'ELEC_201609', 'ELEC_201610', 'ELEC_201611', 'ELEC_201612', 'ELEC_201701', 'ELEC_201702', 'ELEC_201703', 'ELEC_201704', 'ELEC_201705', 'ELEC_201706', 'ELEC_201707', 'ELEC_201708', 'ELEC_201709', 'ELEC_201710', 'ELEC_201711', 'ELEC_201712', 'ELEC_201801', 'ELEC_201802', 'ELEC_201803', 'ELEC_201804', 'ELEC_201805', 'ELEC_201806', 'ELEC_201807', 'ELEC_201808', 'ELEC_201809', 'ELEC_201810', 'ELEC_201811', 'ELEC_201812', 'ELEC_201901', 'ELEC_201902', 'ELEC_201903', 'ELEC_201904', 'ELEC_201905', 'ELEC_201906', 'ELEC_201907', 'ELEC_201908', 'ELEC_201909', 'ELEC_201910', 'ELEC_201911', 'ELEC_201912', 'ELEC_202001', 'ELEC_202002', 'ELEC_202003', 'ELEC_202004', 'ELEC_202005', 'ELEC_202006', 'ELEC_202007', 'ELEC_202008', 'ELEC_202009', 'ELEC_202010', 'ELEC_202011', 'ELEC_202012', 'index', 'ELE_202101', 'ELE_202102', 'ELE_202103', 'ELE_202104', 'ELE_202105', 'ELE_202106', 'ELE_202107', 'ELE_202108', 'ELE_202109', 'ELE_202110', 'ELE_202111', 'ELE_202112']


basedata = pd.read_excel('C:/Users/user/PycharmProjects/Areasum_20220517_병원_V2_0.xlsx', engine='openpyxl')

energy_sort = 'ELEC'
calc_type = 'Carbon'
data_type = 'raw'

month_arr = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
year_arr = ['2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021']

result_df_arr = []
for i in range(len(basedata)):
    row = basedata.loc[i]
    print('legister is : ' + str(row['총괄표제부']) + '/' + str(row['일반건축물']) + '/' + str(row['표제부']))
    try:
        # 해당 배열값이 없으면 셀 값이 np.nan인데, 이 경우 if문에서 typeerror가 나니까, try에서 Except로 빠진다는 것은 값이 없다는 것임.
        if len(row['총괄표제부']) != 0:
            recap_pk_arr = row['총괄표제부'].split('|')
            # 괄호 제거 ( (앞의 것만을 사용)
            for k in range(len(recap_pk_arr)):
                recap_pk_arr[k] = recap_pk_arr[k].split('(')[0]
            # PK코드로 DB를 조회
            for pk_code in recap_pk_arr:
                k =get_year_data_monthly_by_pk(pk_code, energy_sort, year_arr, calc_type, data_type, include_attr=True)
                result_df_arr.append(k)
    except:
        # 총괄표제부 값이 없으면, 일반-표제부 값을 배열로 반환함.
        try:
            if len(row['일반건축물']) != 0:
                recap_pk_arr = row['일반건축물'].split('|')
                # 괄호 제거 ( (앞의 것만을 사용)
                for k in range(len(recap_pk_arr)):
                    recap_pk_arr[k] = recap_pk_arr[k].split('(')[0]
                # PK코드로 DB를 조회
                for pk_code in recap_pk_arr:
                    k = get_year_data_monthly_by_pk(pk_code, energy_sort, year_arr, calc_type, data_type, include_attr=True)
                    result_df_arr.append(k)
        except:
            try:
                if len(row['표제부']) != 0:
                    recap_pk_arr = row['표제부'].split('|')
                    # 괄호 제거 ( (앞의 것만을 사용)
                    for k in range(len(recap_pk_arr)):
                        recap_pk_arr[k] = recap_pk_arr[k].split('(')[0]
                    # PK코드로 DB를 조회
                    for pk_code in recap_pk_arr:
                        k = get_year_data_monthly_by_pk(pk_code, energy_sort, year_arr, calc_type, data_type, include_attr=True)
                        result_df_arr.append(k)
            except:
                print('에너지DB 값이 없음.')

for i in range(len(result_df_arr)):
    if i == 0:
        # 맨 첫번째 것은 그대로 사용함
        result_df = result_df_arr[i]
    else:
        # 그 다음 것은 이어붙임
        result_df = pd.concat([result_df, result_df_arr[i]])

elec_result = result_df

result_col_arr = ['BLD_TYPE_GB_CD', 'REGSTR_GB_CD', 'REGSTR_KIND_CD', 'SIGUNGU_NM', 'BJDONG_NM', 'PLAT_GB_CD', 'BUN', 'JI', 'JUSO', 'ROAD_JUSO', 'TOTAREA', 'HHLD_CNT', 'MAIN_PURPS_NM', 'UNIT_CD', 'USEAPR_DAY', 'ELEC_201401', 'ELEC_201402', 'ELEC_201403', 'ELEC_201404', 'ELEC_201405', 'ELEC_201406', 'ELEC_201407', 'ELEC_201408', 'ELEC_201409', 'ELEC_201410', 'ELEC_201411', 'ELEC_201412', 'ELEC_201501', 'ELEC_201502', 'ELEC_201503', 'ELEC_201504', 'ELEC_201505', 'ELEC_201506', 'ELEC_201507', 'ELEC_201508', 'ELEC_201509', 'ELEC_201510', 'ELEC_201511', 'ELEC_201512', 'ELEC_201601', 'ELEC_201602', 'ELEC_201603', 'ELEC_201604', 'ELEC_201605', 'ELEC_201606', 'ELEC_201607', 'ELEC_201608', 'ELEC_201609', 'ELEC_201610', 'ELEC_201611', 'ELEC_201612', 'ELEC_201701', 'ELEC_201702', 'ELEC_201703', 'ELEC_201704', 'ELEC_201705', 'ELEC_201706', 'ELEC_201707', 'ELEC_201708', 'ELEC_201709', 'ELEC_201710', 'ELEC_201711', 'ELEC_201712', 'ELEC_201801', 'ELEC_201802', 'ELEC_201803', 'ELEC_201804', 'ELEC_201805', 'ELEC_201806', 'ELEC_201807', 'ELEC_201808', 'ELEC_201809', 'ELEC_201810', 'ELEC_201811', 'ELEC_201812', 'ELEC_201901', 'ELEC_201902', 'ELEC_201903', 'ELEC_201904', 'ELEC_201905', 'ELEC_201906', 'ELEC_201907', 'ELEC_201908', 'ELEC_201909', 'ELEC_201910', 'ELEC_201911', 'ELEC_201912', 'ELEC_202001', 'ELEC_202002', 'ELEC_202003', 'ELEC_202004', 'ELEC_202005', 'ELEC_202006', 'ELEC_202007', 'ELEC_202008', 'ELEC_202009', 'ELEC_202010', 'ELEC_202011', 'ELEC_202012', 'index', 'ELE_202101', 'ELE_202102', 'ELE_202103', 'ELE_202104', 'ELE_202105', 'ELE_202106', 'ELE_202107', 'ELE_202108', 'ELE_202109', 'ELE_202110', 'ELE_202111', 'ELE_202112']


basedata = pd.read_excel('C:/Users/user/PycharmProjects/Areasum_20220517_병원_V2_0.xlsx', engine='openpyxl')

energy_sort = 'GAS'
calc_type = 'Carbon'
data_type = 'raw'

month_arr = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
year_arr = ['2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021']

result_df_arr = []
for i in range(len(basedata)):
    row = basedata.loc[i]
    print('legister is : ' + str(row['총괄표제부']) + '/' + str(row['일반건축물']) + '/' + str(row['표제부']))
    try:
        # 해당 배열값이 없으면 셀 값이 np.nan인데, 이 경우 if문에서 typeerror가 나니까, try에서 Except로 빠진다는 것은 값이 없다는 것임.
        if len(row['총괄표제부']) != 0:
            recap_pk_arr = row['총괄표제부'].split('|')
            # 괄호 제거 ( (앞의 것만을 사용)
            for k in range(len(recap_pk_arr)):
                recap_pk_arr[k] = recap_pk_arr[k].split('(')[0]
            # PK코드로 DB를 조회
            for pk_code in recap_pk_arr:
                k =get_year_data_monthly_by_pk(pk_code, energy_sort, year_arr, calc_type, data_type, include_attr=True)
                result_df_arr.append(k)
    except:
        # 총괄표제부 값이 없으면, 일반-표제부 값을 배열로 반환함.
        try:
            if len(row['일반건축물']) != 0:
                recap_pk_arr = row['일반건축물'].split('|')
                # 괄호 제거 ( (앞의 것만을 사용)
                for k in range(len(recap_pk_arr)):
                    recap_pk_arr[k] = recap_pk_arr[k].split('(')[0]
                # PK코드로 DB를 조회
                for pk_code in recap_pk_arr:
                    k = get_year_data_monthly_by_pk(pk_code, energy_sort, year_arr, calc_type, data_type, include_attr=True)
                    result_df_arr.append(k)
        except:
            try:
                if len(row['표제부']) != 0:
                    recap_pk_arr = row['표제부'].split('|')
                    # 괄호 제거 ( (앞의 것만을 사용)
                    for k in range(len(recap_pk_arr)):
                        recap_pk_arr[k] = recap_pk_arr[k].split('(')[0]
                    # PK코드로 DB를 조회
                    for pk_code in recap_pk_arr:
                        k = get_year_data_monthly_by_pk(pk_code, energy_sort, year_arr, calc_type, data_type, include_attr=True)
                        result_df_arr.append(k)
            except:
                print('에너지DB 값이 없음.')

for i in range(len(result_df_arr)):
    if i == 0:
        # 맨 첫번째 것은 그대로 사용함
        result_df = result_df_arr[i]
    else:
        # 그 다음 것은 이어붙임
        result_df = pd.concat([result_df, result_df_arr[i]])

gas_result = result_df


basedata = pd.read_excel('C:/Users/user/PycharmProjects/Areasum_20220517_병원_V2_0.xlsx', engine='openpyxl')

energy_sort = 'HEAT'
calc_type = 'Carbon'
data_type = 'raw'

month_arr = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
year_arr = ['2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021']

result_df_arr = []
for i in range(len(basedata)):
    row = basedata.loc[i]
    print('legister is : ' + str(row['총괄표제부']) + '/' + str(row['일반건축물']) + '/' + str(row['표제부']))
    try:
        # 해당 배열값이 없으면 셀 값이 np.nan인데, 이 경우 if문에서 typeerror가 나니까, try에서 Except로 빠진다는 것은 값이 없다는 것임.
        if len(row['총괄표제부']) != 0:
            recap_pk_arr = row['총괄표제부'].split('|')
            # 괄호 제거 ( (앞의 것만을 사용)
            for k in range(len(recap_pk_arr)):
                recap_pk_arr[k] = recap_pk_arr[k].split('(')[0]
            # PK코드로 DB를 조회
            for pk_code in recap_pk_arr:
                k =get_year_data_monthly_by_pk(pk_code, energy_sort, year_arr, calc_type, data_type, include_attr=True)
                result_df_arr.append(k)
    except:
        # 총괄표제부 값이 없으면, 일반-표제부 값을 배열로 반환함.
        try:
            if len(row['일반건축물']) != 0:
                recap_pk_arr = row['일반건축물'].split('|')
                # 괄호 제거 ( (앞의 것만을 사용)
                for k in range(len(recap_pk_arr)):
                    recap_pk_arr[k] = recap_pk_arr[k].split('(')[0]
                # PK코드로 DB를 조회
                for pk_code in recap_pk_arr:
                    k = get_year_data_monthly_by_pk(pk_code, energy_sort, year_arr, calc_type, data_type, include_attr=True)
                    result_df_arr.append(k)
        except:
            try:
                if len(row['표제부']) != 0:
                    recap_pk_arr = row['표제부'].split('|')
                    # 괄호 제거 ( (앞의 것만을 사용)
                    for k in range(len(recap_pk_arr)):
                        recap_pk_arr[k] = recap_pk_arr[k].split('(')[0]
                    # PK코드로 DB를 조회
                    for pk_code in recap_pk_arr:
                        k = get_year_data_monthly_by_pk(pk_code, energy_sort, year_arr, calc_type, data_type, include_attr=True)
                        result_df_arr.append(k)
            except:
                print('에너지DB 값이 없음.')

for i in range(len(result_df_arr)):
    if i == 0:
        # 맨 첫번째 것은 그대로 사용함
        result_df = result_df_arr[i]
    else:
        # 그 다음 것은 이어붙임
        result_df = pd.concat([result_df, result_df_arr[i]])

heat_result = result_df

result_df = elec_result.join(gas_result, how='left', rsuffix='_gas')
result_df = result_df.join(heat_result, how='left', rsuffix='_heat')

print(result_df)
result_df.to_csv('에너지뭔가갖다붙인_병원건물결과.csv', encoding='utf-8 sig')


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

# sql_gas = "SELECT MGM_BLD_PK, USEAPR_DAY, MAIN_PURPS_NM, (GAS_202004 + GAS_202005 + GAS_202006 + GAS_202007 + GAS_202008 + GAS_202009 + GAS_202010 + GAS_202011 + GAS_202012 + GAS_202101 + GAS_202102 + GAS_202103)*1.1/TOTAREA AS GAS_converged_EUI FROM gas"
# sql_elec = "SELECT MGM_BLD_PK, USEAPR_DAY, MAIN_PURPS_NM, (ELEC_202004 + ELEC_202005 + ELEC_202006 + ELEC_202007 + ELEC_202008 + ELEC_202009 + ELEC_202010 + ELEC_202011 + ELEC_202012 + ELEC_202101 + ELEC_202102 + ELEC_202103)*2.75/TOTAREA AS ELEC_converged_EUI FROM elec"
# sql_heat = "SELECT MGM_BLD_PK, USEAPR_DAY, MAIN_PURPS_NM, (HEAT_202004 + HEAT_202005 + HEAT_202006 + HEAT_202007 + HEAT_202008 + HEAT_202009 + HEAT_202010 + HEAT_202011 + HEAT_202012 + HEAT_202101 + HEAT_202102 + HEAT_202103)*0.728/TOTAREA AS HEAT_converged_EUI FROM heat"

def load_sql(cursor, load_query):
    cursor.execute(load_query)
    result = cursor.fetchall()
    return pd.DataFrame(result)

def get_rawdata_all(energy_type_arr, year_arr):

    # 1. 데이터 불러오기
    for energy_type in energy_type_arr:
        for year in year_arr:

            query_string = 'SELECT * FROM ' + energy_type + '_' + year + ';'

            if year_arr.index(year) == 0:
                result_df = load_sql(cursor, query_string)
                result_df.set_index('MGM_BLD_PK', drop=True, inplace=True)
            else:
                temp_df = load_sql(cursor, query_string)
                temp_df.set_index('MGM_BLD_PK', drop=True, inplace=True)
                result_df = result_df.join(temp_df, how='outer')

        if energy_type_arr.index(energy_type) == 0:
            final_result_df = result_df
        else:
            final_result_df.join(result_df, how='outer')

    # 2. 계산타입 (Raw/Carbon/TOE/EUI) 별로 데이터 연산



# def get_fulldata():
#     gas_data = load_sql(cursor, sql_gas)
#     elec_data = load_sql(cursor, sql_elec)
#     heat_data = load_sql(cursor, sql_heat)
#     gas_data.set_index('MGM_BLD_PK', drop=True, inplace=True)
#     elec_data.set_index('MGM_BLD_PK', drop=True, inplace=True)
#     heat_data.set_index('MGM_BLD_PK', drop=True, inplace=True)
#     # print(gas_data)
#     # print(elec_data)
#     # print(heat_data)
#
#     # 코드 가독성을 위해 gas_data를 복사한 다음 elec_data, heat_data와 각각 머징
#     result = gas_data
#
#     result = result.merge(elec_data['ELEC_converged_EUI'], how='outer', left_index=True, right_index=True)
#     result = fill_null(result, elec_data, ['USEAPR_DAY', 'MAIN_PURPS_NM'])
#
#     result = result.merge(heat_data['HEAT_converged_EUI'], how='outer', left_index=True, right_index=True)
#     result = fill_null(result, heat_data, ['USEAPR_DAY', 'MAIN_PURPS_NM'])
#
#     # EUI의 총합을 계산해서 합산
#     # fillna로 NaN 데이터값을 0으로 치환(합만 구해서 사용하므로)
#     result['GAS_converged_EUI'] = result['GAS_converged_EUI'].fillna(0)
#     result['ELEC_converged_EUI'] = result['ELEC_converged_EUI'].fillna(0)
#     result['HEAT_converged_EUI'] = result['HEAT_converged_EUI'].fillna(0)
#     result['total_converged_EUI'] = result['GAS_converged_EUI'] + result['ELEC_converged_EUI'] + result['HEAT_converged_EUI']
#
#     print('full data loaded')
#     print(result.head())
#     return result
#
# #get_fulldata()


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

def read_dbdata_dataframe(calc_type, data_type):
    # 통합파일 출력과 같으나, 파일로 저장하는게 아니고 데이터프레임을 반환함.
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

    return result

def distribute_plot_mod(data, label, label_word):#, figure, type='both'):
    k = 20000000
    print(k)
    x_range = []
    for i in range(0, 200):
        x_range.append(i*k/200)
    temp_data = data[(data['BLDG_AGE'] < 12) & (data['BLDG_AGE'] >= 0)]
    plt.hist(temp_data[label], alpha = 0.5, bins = x_range, histtype='step', label = '2010~')
    temp_data = data[(data['BLDG_AGE'] < 22) & (data['BLDG_AGE'] >= 12)]
    plt.hist(temp_data[label], alpha = 0.5, bins = x_range, histtype='step', label = '2000~2009')
    temp_data = data[(data['BLDG_AGE'] < 32) & (data['BLDG_AGE'] >= 22)]
    plt.hist(temp_data[label], alpha = 0.5, bins = x_range, histtype='step', label = '1990~1999')
    temp_data = data[(data['BLDG_AGE'] < 42) & (data['BLDG_AGE'] >= 32)]
    plt.hist(temp_data[label], alpha = 0.5, bins = x_range, histtype='step', label = '1980~1989')
    temp_data = data[(data['BLDG_AGE'] < 52) & (data['BLDG_AGE'] >= 42)]
    plt.hist(temp_data[label], alpha = 0.5, bins = x_range, histtype='step', label = '1970~1979')
    temp_data = data[(data['BLDG_AGE'] < 62) & (data['BLDG_AGE'] >= 52)]
    plt.hist(temp_data[label], alpha = 0.5, bins = x_range, histtype='step', label = '1960~1969')
    temp_data = data[(data['BLDG_AGE'] < 72) & (data['BLDG_AGE'] >= 62)]
    plt.hist(temp_data[label], alpha = 0.5, bins = x_range, histtype='step', label = '1950~1959')
    temp_data = data[(data['BLDG_AGE'] < 82)]
    plt.hist(temp_data[label], alpha = 0.5, bins = x_range, histtype='step', label = '~1949')

    plt.xlim([0, 20000000])
    plt.ylim([0, 5000])
    plt.title(label_word)
    plt.legend()
    plt.show()
    plt.clf()

    # data[label].plot(kind='kde')

    # # 범위 설정. 데이터의 최소-최대 값 기준에 resolution은 10000.
    # resolution = 1000
    # data_for_fit = data[label].values
    # #x_range = np.linspace(min(data_for_fit), max(data_for_fit), resolution)
    # x_range = []
    # print(x_range)
    # #div = 0.01
    # k = max(data_for_fit)
    # print(k)
    # for i in range(0, resolution):
    #     x_range.append(i*k/resolution)
    # print(x_range)
    # plt.xlim(0, max(data_for_fit))
    # temp = figure.add_subplot(1, 1, 1)
    # if type == 'both':
    #     temp = sns.distplot(data[label], bins=x_range)
    #     # plt.show()
    # elif type == 'hist':
    #     temp = sns.displot(data[label], kde=False, bins=x_range)
    #     # plt.show()
    # elif type == 'kde':
    #     temp = sns.displot(data[label], kind='kde')
    #     # plt.show()
    # else:
    #     print('invalid type. please use one of |both|hist|kde|')

def remove_percentile(percentile, dataframe, label):
    modded_dataframe = dataframe[(dataframe[label] <= dataframe[label].quantile(q=1-percentile, interpolation='nearest')) & (dataframe[label] > dataframe[label].quantile(q=percentile, interpolation='nearest'))]
    return modded_dataframe

def drop_extreme(data, label):
    # 아웃소스: 나중에 체크할 것
    # s_ol_data = pd.Series(ol_data)
    level_1q = data[label].quantile(0.25)
    level_3q = data[label].quantile(0.75)
    IQR = level_3q - level_1q
    rev_range = 3  # 제거 범위 조절 변수
    return data[(data[label] <= level_3q + (rev_range * IQR)) & (data[label] >= data[label] - (rev_range * IQR))]

def draw_histogram(data, label, resolution, hist_type, label_name):
    # 극단값을 쳐내고 그것을 기반으로 배열을 작성
    # histtype 백업: 'bar', 'barstacked', 'step', 'stepfilled'
    dropped_data = drop_extreme(data, label)
    data_for_fit = dropped_data[label].values
    x_range = []
    for i in range(0, resolution):
        x_range.append(i*max(data_for_fit)/resolution)
    plt.hist(data[label], alpha=0.5, bins=x_range, histtype=hist_type, label=label_name)

#
# read_and_export_excel('EUI', 'sum_divarea')
# read_and_export_excel('EUI', 'sum')
# read_and_export_excel('Carbon', 'sum_divarea')
# read_and_export_excel('Carbon', 'sum')
# read_and_export_excel('toe', 'sum')
# read_and_export_excel('toe', 'sum_divarea')
# read_and_export_excel('raw', 'sum')
# read_and_export_excel('raw', 'sum_divarea')
# print('파일저장 완료')
# import time
# time.sleep(1000)
# #read_and_export_excel('Carbon', 'sum')
#
# # 2022.04.22 탄소로 뽑고 toe계산해서 붙이기
# #data = read_dbdata_dataframe('Carbon', 'sum')
#
# # data['toe_heat_2020'] = data['HEAT_converged_Carbon_sum_2020']*498.4762734
# # data['toe_elec_2020'] = data['ELEC_converged_Carbon_sum_2020']*0.000426025
# # data['toe_gas_2020'] = data['GAS_converged_Carbon_sum_2020']*0.000687354
# # data['toe_total_2020'] = data['toe_heat_2020'] + data['toe_elec_2020'] + data['toe_gas_2020']
# # data.to_excel('result(Carbon_sum)_2020toe_added.xlsx')
#
#
#
#
# # data = pd.read_excel('result(Carbon_sum)_2020toe_added.xlsx')
#
# '''# 긴급. DB에 넣을 시간이 없어 때워야 한다.
# # xlsx 3개를 읽어와서 사용승인일과 PK코드만 분리
# heat_pk_data = pd.read_excel('DB_INPUT/HEAT_2004_2109.xlsx')
# elec_pk_data = pd.read_excel('DB_INPUT/ELEC_2004_2109.xlsx')
# gas_pk_data = pd.read_excel('DB_INPUT/GAS_2004_2109.xlsx')
#
# # PK코드와 사용승인일만 남김
# heat_pk_data = heat_pk_data[['MGM_BLD_PK', 'USEAPR_DAY']]
# elec_pk_data = elec_pk_data[['MGM_BLD_PK', 'USEAPR_DAY']]
# gas_pk_data = gas_pk_data[['MGM_BLD_PK', 'USEAPR_DAY']]
#
# # 합쳐서 PK코드 데이터를 만듬
# heat_pk_data.set_index('MGM_BLD_PK', drop=True, inplace=True)
# elec_pk_data.set_index('MGM_BLD_PK', drop=True, inplace=True)
# gas_pk_data.set_index('MGM_BLD_PK', drop=True, inplace=True)
#
# # 병합을 위한 코드를 추가 작성해야 할 것임.
# heat_pk_data.join(elec_pk_data, how='outer', rsuffix='_elec')
# heat_pk_data.join(gas_pk_data, how='outer', rsuffix='_gas')
#
# import math
# bldg_age_data = heat_pk_data.dropna()    #NaN값 (사용승인일 데이터가 없는 것)을 날림
# #bldg_age_data['BLDG_AGE'] = 2022 - math.floor(bldg_age_data['USEAPR_DAY']/10000)    #맨앞 4자리(연도)만 뺀 뒤 이걸로 나이를 구함
# bldg_age_data.to_excel('building_agedata.xlsx')'''
#
# # bldg_age_data = pd.read_excel('building_agedata.xlsx')
# #
# # bldg_age_data.set_index('MGM_BLD_PK', drop=True, inplace=True)
# #
# # data.set_index('MGM_BLD_PK', drop=True, inplace=True)
# # print(bldg_age_data)
# # data.join(bldg_age_data, how='left')
#
# # 여기부터는 그래프를 그리는 부분
# # data.to_excel('건물연령 합한 데이터.xlsx')
# data = pd.read_excel('building_data_including_age.xlsx')
# data.set_index('MGM_BLD_PK', drop=True, inplace=True)
# print(data)
#
#
# # 필터-toe 2천 이상.
# #filtered_data = data[data['toe_total_2020'] >= 2000]
# #filtered_data.set_index('MGM_BLD_PK', drop=True, inplace=True)
# #filtered_data.join(bldg_age_data, how='left')
# #filtered_data.to_excel('toe2000cut.xlsx')
# #fig = plt.figure()
# filtered_data = data
# # filtered_data_mod = filtered_data[(filtered_data['TOTAREA'] < 100) & (filtered_data['TOTAREA'] >= 0)]
# # distribute_plot_mod(filtered_data_mod, 'energy_total_2020', '0~100')
# # filtered_data_mod = filtered_data[(filtered_data['TOTAREA'] < 500) & (filtered_data['TOTAREA'] >= 100)]
# # distribute_plot_mod(filtered_data_mod, 'energy_total_2020', '100~500')
# # filtered_data_mod = filtered_data[(filtered_data['TOTAREA'] < 1000) & (filtered_data['TOTAREA'] >= 500)]
# # distribute_plot_mod(filtered_data_mod, 'energy_total_2020', '500~1000')
# # filtered_data_mod = filtered_data[(filtered_data['TOTAREA'] < 3000) & (filtered_data['TOTAREA'] >= 1000)]
# # distribute_plot_mod(filtered_data_mod, 'energy_total_2020', '1000~3000')
# # filtered_data_mod = filtered_data[(filtered_data['TOTAREA'] < 5000) & (filtered_data['TOTAREA'] >= 3000)]
# # distribute_plot_mod(filtered_data_mod, 'energy_total_2020', '3000~5000')
# # filtered_data_mod = filtered_data[(filtered_data['TOTAREA'] < 10000) & (filtered_data['TOTAREA'] >= 5000)]
# # distribute_plot_mod(filtered_data_mod, 'energy_total_2020', '5000~10000')
# # filtered_data_mod = filtered_data[(filtered_data['TOTAREA'] < 30000) & (filtered_data['TOTAREA'] >= 10000)]
# # distribute_plot_mod(filtered_data_mod, 'energy_total_2020', '10000~30000')
#
# # plt.xlim([0, 1000000])
# # plt.ylim([0, 100000])
# # plt.legend()
# # plt.show()
# # plt.clf()
#
# filtered_data_mod = filtered_data[(filtered_data['BLDG_AGE'] < 10) & (filtered_data['BLDG_AGE'] >= 5)]
# filtered_data_mod = remove_percentile(0.05, filtered_data_mod, 'HEAT_converged_Carbon_sum_2020')
# distribute_plot_mod(filtered_data_mod, 'HEAT_converged_Carbon_sum_2020')
#
# filtered_data_mod = filtered_data[(filtered_data['BLDG_AGE'] < 15) & (filtered_data['BLDG_AGE'] >= 10)]
# filtered_data_mod = remove_percentile(0.05, filtered_data_mod, 'HEAT_converged_Carbon_sum_2020')
# distribute_plot_mod(filtered_data_mod, 'HEAT_converged_Carbon_sum_2020')
#
# filtered_data_mod = filtered_data[(filtered_data['BLDG_AGE'] < 20) & (filtered_data['BLDG_AGE'] >= 15)]
# filtered_data_mod = remove_percentile(0.05, filtered_data_mod, 'HEAT_converged_Carbon_sum_2020')
# distribute_plot_mod(filtered_data_mod, 'HEAT_converged_Carbon_sum_2020')
#
# filtered_data_mod = filtered_data[(filtered_data['BLDG_AGE'] < 25) & (filtered_data['BLDG_AGE'] >= 20)]
# filtered_data_mod = remove_percentile(0.05, filtered_data_mod, 'HEAT_converged_Carbon_sum_2020')
# distribute_plot_mod(filtered_data_mod, 'HEAT_converged_Carbon_sum_2020')
#
#
# '''filtered_data_mod = remove_percentile(0.05, filtered_data, 'HEAT_converged_Carbon_sum_2014')
# distribute_plot_mod(filtered_data_mod, 'HEAT_converged_Carbon_sum_2014')
# filtered_data_mod = remove_percentile(0.05, filtered_data, 'HEAT_converged_Carbon_sum_2015')
# distribute_plot_mod(filtered_data_mod, 'HEAT_converged_Carbon_sum_2015')
# filtered_data_mod = remove_percentile(0.05, filtered_data, 'HEAT_converged_Carbon_sum_2016')
# distribute_plot_mod(filtered_data_mod, 'HEAT_converged_Carbon_sum_2016')
# filtered_data_mod = remove_percentile(0.05, filtered_data, 'HEAT_converged_Carbon_sum_2017')
# distribute_plot_mod(filtered_data_mod, 'HEAT_converged_Carbon_sum_2017')
# filtered_data_mod = remove_percentile(0.05, filtered_data, 'HEAT_converged_Carbon_sum_2018')
# distribute_plot_mod(filtered_data_mod, 'HEAT_converged_Carbon_sum_2018')
# filtered_data_mod = remove_percentile(0.05, filtered_data, 'HEAT_converged_Carbon_sum_2019')
# distribute_plot_mod(filtered_data_mod, 'HEAT_converged_Carbon_sum_2019')
# filtered_data_mod = remove_percentile(0.05, filtered_data, 'HEAT_converged_Carbon_sum_2020')
# distribute_plot_mod(filtered_data_mod, 'HEAT_converged_Carbon_sum_2020')'''
# plt.show()
#
# plt.clf()
# distribute_plot_mod(filtered_data_mod, 'ELEC_converged_Carbon_sum_2014', 'kde')
# distribute_plot_mod(filtered_data_mod, 'ELEC_converged_Carbon_sum_2015', 'kde')
# distribute_plot_mod(filtered_data_mod, 'ELEC_converged_Carbon_sum_2016', 'kde')
# distribute_plot_mod(filtered_data_mod, 'ELEC_converged_Carbon_sum_2017', 'kde')
# distribute_plot_mod(filtered_data_mod, 'ELEC_converged_Carbon_sum_2018', 'kde')
# distribute_plot_mod(filtered_data_mod, 'ELEC_converged_Carbon_sum_2019', 'kde')
# distribute_plot_mod(filtered_data_mod, 'ELEC_converged_Carbon_sum_2020', 'kde')
# plt.show()
# plt.clf()
# distribute_plot_mod(filtered_data_mod, 'GAS_converged_Carbon_sum_2014', 'kde')
# distribute_plot_mod(filtered_data_mod, 'GAS_converged_Carbon_sum_2015', 'kde')
# distribute_plot_mod(filtered_data_mod, 'GAS_converged_Carbon_sum_2016', 'kde')
# distribute_plot_mod(filtered_data_mod, 'GAS_converged_Carbon_sum_2017', 'kde')
# distribute_plot_mod(filtered_data_mod, 'GAS_converged_Carbon_sum_2018', 'kde')
# distribute_plot_mod(filtered_data_mod, 'GAS_converged_Carbon_sum_2019', 'kde')
# distribute_plot_mod(filtered_data_mod, 'GAS_converged_Carbon_sum_2020', 'kde')
# plt.show()
# plt.clf()




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





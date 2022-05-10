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


def get_year_data_monthly_by_pk(pk_code_arr, energy_sort, year_arr, calc_type, data_type, include_attr = True):
    # 속성정보 데이터를 로드
    query_for_attr = "SELECT * FROM " + str(energy_sort) + "_attribute WHERE MGM_BLD_PK IN " + str(tuple(pk_code_arr)) + ";"
    print(query_for_attr)
    attr_data = load_sql(cursor, query_for_attr)
    print(attr_data)
    attr_data.set_index('MGM_BLD_PK', drop=True, inplace=True)
    attr_column = attr_data.columns.to_list()

    for year in year_arr:
        # 쿼리설정: 에너지종류별, 계산타입(EUI, 탄소배출)별, 연도별 1월부터 12월까지
        query = "SELECT * FROM " + str(energy_sort) + '_' + str(year)  + " WHERE MGM_BLD_PK IN " + str(tuple(pk_code_arr)) + ";"
        data = load_sql(cursor, query)
        print(data)
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

def get_attr_data_only(energy_sort):
    # 속성정보 데이터를 로드
    query_for_attr = "SELECT * FROM " + str(energy_sort) + '_attribute'
    attr_data = load_sql(cursor, query_for_attr)
    attr_data.set_index('MGM_BLD_PK', drop=True, inplace=True)
    return attr_data


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

# 전기랑 가스 파일을 불러옴
elec_data_recap = pd.read_csv('C:/Users/user/Downloads/대학목록_총괄표제부/대학목록_Carbon_ELEC.csv')
gas_data_recap = pd.read_csv('C:/Users/user/Downloads/대학목록_총괄표제부/대학목록_Carbon_GAS.csv')
elec_data_recap.set_index('mgmBldrgstPk', drop=True, inplace=True)
gas_data_recap.set_index('mgmBldrgstPk', drop=True, inplace=True)

# 표제부 파일도 불러옴
elec_data_title = pd.read_csv('C:/Users/user/Downloads/대학목록_표제부/대학목록_Carbon_ELEC.csv')
gas_data_title = pd.read_csv('C:/Users/user/Downloads/대학목록_표제부/대학목록_Carbon_GAS.csv')
# 총괄표제부에 있으면 드롭
for i in range(len(elec_data_title)):
    row = elec_data_title.loc[i]
    if row['PNU'] in elec_data_recap['PNU']:
        elec_data_title.drop(labels=row.index, inplace=True)
elec_data_title.set_index('mgmBldrgstPk', drop=True, inplace=True)
elec_data_recap = elec_data_recap.join(elec_data_title, how='outer', rsuffix='_title')

for i in range(len(gas_data_title)):
    row = gas_data_title.loc[i]
    if row['PNU'] in elec_data_recap['PNU']:
        gas_data_title.drop(labels=row.index, inplace=True)
gas_data_title.set_index('mgmBldrgstPk', drop=True, inplace=True)
gas_data_recap = gas_data_recap.join(gas_data_title, how='outer', rsuffix='_title')

# PK코드 기준으로 두 개를 합침
# elec_data_recap.set_index('mgmBldrgstPk', drop=True, inplace=True)
# gas_data_recap.set_index('mgmBldrgstPk', drop=True, inplace=True)

final_data = elec_data_recap.j
join(gas_data_recap, how='outer', rsuffix='_gas')

month_arr = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
year_arr = ['2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021']

print(final_data)

for year in year_arr:
    for month in month_arr:
        final_data['Carbon_' + year + month] = final_data['ELEC_' + year + month] + final_data['GAS_' + year + month]


final_data.to_csv('대학교데이터 최종결과물.csv', encoding='utf-8 sig')

raise IOError



energy_sort = 'GAS'
year_arr = [2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021]
calc_type = 'Carbon'
data_type = 'raw'


pk_code_df = pd.read_excel('C:/Users/user/Downloads/대학목록.xlsx', engine='openpyxl')
pkcode_df = pk_code_df.dropna(subset=['mgmBldrgstPk'])
# recap_df = pd.read_csv('C:/Users/user/PycharmProjects/bind_result_recaptitle.csv')
# pk_code_df = pk_code_df[['mgmBldrgstPk', 'PNU']]
# pk_code_df.set_index('PNU', drop=True, inplace=True)
# recap_df_second = recap_df[['mgmBldrgstPk', 'PNU']]
# recap_df_second.set_index('PNU', drop=True, inplace=True)
# pk_code_df = pk_code_df.join(recap_df_second, how='left', lsuffix='_title')
print(pk_code_df)

# 여기가 검색부분임 (바꾸지 말 것)
pk_code_arr = pk_code_df['mgmBldrgstPk'].dropna().values.tolist()
print(len(pk_code_arr))
#pk_code_arr.append('11170-16053')
data = get_year_data_monthly_by_pk(tuple(pk_code_arr), energy_sort, year_arr, calc_type, data_type, include_attr = True)
print(data)

# recap_df = pd.read_csv('C:/Users/user/Downloads/최종에너지합산결과_2020_20220507_v3.csv')
# recap_df_third = recap_df[['mgmBldrgstPk', 'count', 'atch_count', 'totArea', 'PNU']]
# recap_df_third = recap_df_third.rename(columns={'totArea':'totArea_title'})
# recap_df_third.set_index('mgmBldrgstPk', drop=True, inplace=True)


# recap_df_third = recap_df[['mgmBldrgstPk', 'mainBldCnt', 'atchBldCnt', 'totArea', 'PNU']]
# recap_df_third = recap_df_third.rename(columns={'totArea':'totArea_recap'})
# recap_df_third.set_index('mgmBldrgstPk', drop=True, inplace=True)

univ_df = pd.read_excel('C:/Users/user/Downloads/대학목록.xlsx', engine='openpyxl')
# univ_df = univ_df[['mgmBldrgstPk', '학교명', '주소', 'count', 'atch_count', 'etc_count', 'USEAPR_DAY', 'BLDG_AGE']]
univ_df = univ_df.rename(columns={'USEAPR_DAY':'USEAPR_DAY_title'})
univ_df.set_index('mgmBldrgstPk', drop=True, inplace=True)

#data = data.join(recap_df_third, how='left')
data = data.join(univ_df, how='left')

data.to_csv('C:/Users/user/Downloads/대학목록_' + calc_type + '_' + energy_sort + '.csv', encoding='utf-8 sig')

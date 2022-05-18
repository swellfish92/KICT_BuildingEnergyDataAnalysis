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

energy_db_another = pymysql.connect(
    user = 'swellfish_remote',
    passwd = 'atdt01410',
    host = '222.236.133.141',
    db = 'energy_data_another',
    charset = 'utf8'
)

cursor = energy_db.cursor(pymysql.cursors.DictCursor)



# 이 변수값은 read_data_from_excel의 인덱스 (칼럼 명) 변경을 위한 것임.
attrdata_db_matrix = {
    '건축물_유형':'BLD_TYPE_GB_CD',
    '관리건축물_PK':'MGM_BLD_PK',
    '건축물_구분':'REGSTR_GB_CD',
    '건축물_종류':'REGSTR_KIND_CD',
    '시군구_명':'SIGUNGU_NM',
    '법정동_명':'BJDONG_NM',
    '대지_구분':'PLAT_GB_CD',
    '주번지':'BUN',
    '부번지':'JI',
    '주소':'JUSO',
    '도로명_주소':'ROAD_JUSO',
    '연면적':'TOTAREA',
    '세대_개수':'HHLD_CNT',
    '사용승인일':'USEAPR_DAY',
    '용동_명':'MAIN_PURPS_NM',
    '단위_명':'UNIT_CD'
 }

attrdata_db_matrix_another = {
    'MGM_BLD_PK':'PK',
    'REGSTR_GB_CD':'group_label',
    'REGSTR_KIND_CD':'regi_label',
    'SIGUNGU_NM':'gu',
    'BJDONG_NM':'dong',
    'PLAT_GB_CD':'land_label',
    'BUN':'main',
    'JI':'sub',
    'TOTAREA':'tot_area',
    'HHLD_CNT':'no_house',
    'MAIN_PURPS_NM':'usage',
    'UNIT_CD':'unit',
 }
namematrix_elec = {'ELEC_201701':'e1701','ELEC_201702':'e1702','ELEC_201703':'e1703','ELEC_201704':'e1704','ELEC_201705':'e1705','ELEC_201706':'e1706','ELEC_201707':'e1707','ELEC_201708':'e1708','ELEC_201709':'e1709','ELEC_201710':'e1710','ELEC_201711':'e1711','ELEC_201712':'e1712','ELEC_201801':'e1801','ELEC_201802':'e1802','ELEC_201803':'e1803','ELEC_201804':'e1804','ELEC_201805':'e1805','ELEC_201806':'e1806','ELEC_201807':'e1807','ELEC_201808':'e1808','ELEC_201809':'e1809','ELEC_201810':'e1810','ELEC_201811':'e1811','ELEC_201812':'e1812','ELEC_201901':'e1901','ELEC_201902':'e1902','ELEC_201903':'e1903','ELEC_201904':'e1904','ELEC_201905':'e1905','ELEC_201906':'e1906','ELEC_201907':'e1907','ELEC_201908':'e1908','ELEC_201909':'e1909','ELEC_201910':'e1910','ELEC_201911':'e1911','ELEC_201912':'e1912','ELEC_202001':'e2001','ELEC_202002':'e2002','ELEC_202003':'e2003','ELEC_202004':'e2004','ELEC_202005':'e2005','ELEC_202006':'e2006','ELEC_202007':'e2007','ELEC_202008':'e2008','ELEC_202009':'e2009','ELEC_202010':'e2010','ELEC_202011':'e2011','ELEC_202012':'e2012','ELEC_202101':'e2101','ELEC_202102':'e2102','ELEC_202103':'e2103','ELEC_202104':'e2104','ELEC_202105':'e2105','ELEC_202106':'e2106','ELEC_202107':'e2107','ELEC_202108':'e2108','ELEC_202109':'e2109'}
namematrix_heat = {'HEAT_201701':'h1701','HEAT_201702':'h1702','HEAT_201703':'h1703','HEAT_201704':'h1704','HEAT_201705':'h1705','HEAT_201706':'h1706','HEAT_201707':'h1707','HEAT_201708':'h1708','HEAT_201709':'h1709','HEAT_201710':'h1710','HEAT_201711':'h1711','HEAT_201712':'h1712','HEAT_201801':'h1801','HEAT_201802':'h1802','HEAT_201803':'h1803','HEAT_201804':'h1804','HEAT_201805':'h1805','HEAT_201806':'h1806','HEAT_201807':'h1807','HEAT_201808':'h1808','HEAT_201809':'h1809','HEAT_201810':'h1810','HEAT_201811':'h1811','HEAT_201812':'h1812','HEAT_201901':'h1901','HEAT_201902':'h1902','HEAT_201903':'h1903','HEAT_201904':'h1904','HEAT_201905':'h1905','HEAT_201906':'h1906','HEAT_201907':'h1907','HEAT_201908':'h1908','HEAT_201909':'h1909','HEAT_201910':'h1910','HEAT_201911':'h1911','HEAT_201912':'h1912','HEAT_202001':'h2001','HEAT_202002':'h2002','HEAT_202003':'h2003','HEAT_202004':'h2004','HEAT_202005':'h2005','HEAT_202006':'h2006','HEAT_202007':'h2007','HEAT_202008':'h2008','HEAT_202009':'h2009','HEAT_202010':'h2010','HEAT_202011':'h2011','HEAT_202012':'h2012','HEAT_202101':'h2101','HEAT_202102':'h2102','HEAT_202103':'h2103','HEAT_202104':'h2104','HEAT_202105':'h2105','HEAT_202106':'h2106','HEAT_202107':'h2107','HEAT_202108':'h2108','HEAT_202109':'h2109'}
namematrix_gas = {'GAS_201701':'g1701','GAS_201702':'g1702','GAS_201703':'g1703','GAS_201704':'g1704','GAS_201705':'g1705','GAS_201706':'g1706','GAS_201707':'g1707','GAS_201708':'g1708','GAS_201709':'g1709','GAS_201710':'g1710','GAS_201711':'g1711','GAS_201712':'g1712','GAS_201801':'g1801','GAS_201802':'g1802','GAS_201803':'g1803','GAS_201804':'g1804','GAS_201805':'g1805','GAS_201806':'g1806','GAS_201807':'g1807','GAS_201808':'g1808','GAS_201809':'g1809','GAS_201810':'g1810','GAS_201811':'g1811','GAS_201812':'g1812','GAS_201901':'g1901','GAS_201902':'g1902','GAS_201903':'g1903','GAS_201904':'g1904','GAS_201905':'g1905','GAS_201906':'g1906','GAS_201907':'g1907','GAS_201908':'g1908','GAS_201909':'g1909','GAS_201910':'g1910','GAS_201911':'g1911','GAS_201912':'g1912','GAS_202001':'g2001','GAS_202002':'g2002','GAS_202003':'g2003','GAS_202004':'g2004','GAS_202005':'g2005','GAS_202006':'g2006','GAS_202007':'g2007','GAS_202008':'g2008','GAS_202009':'g2009','GAS_202010':'g2010','GAS_202011':'g2011','GAS_202012':'g2012','GAS_202101':'g2101','GAS_202102':'g2102','GAS_202103':'g2103','GAS_202104':'g2104','GAS_202105':'g2105','GAS_202106':'g2106','GAS_202107':'g2107','GAS_202108':'g2108','GAS_202109':'g2109'}



# HEAT에서 유닛 단위를 MJ로 통일시킴
def unify_energy_unit(dataframe,  unit_col, data_col_arr):
    print(dataframe)
    for idx, row in dataframe.iterrows():
        # 여기서 조건문으로 단위변환을 걸어 준다. 현재는 Gcal, MWh, MJ의 3개만을 사용할 것.
        if dataframe.loc[idx,:][unit_col] == 'Gcal':
            for col_index in data_col_arr:
                # 1Gcal = 4184MJ (ref:http://www.conversion-website.com/energy/gigacalorie-to-megajoule.html)
                pk_index = dataframe.loc[idx,:]['MGM_BLD_PK']
                dataframe[col_index][idx] = float(dataframe.loc[idx,:][col_index]) * 4184
                dataframe[unit_col][idx] = 'MJ'

        elif dataframe.loc[idx,:][unit_col] == 'Mcal':
            for col_index in data_col_arr:
                # 1Mcal = 4.184MJ (ref:http://www.conversion-website.com/energy/gigacalorie-to-megajoule.html)
                dataframe[col_index][idx] = float(dataframe.loc[idx,:][col_index]) * 4.184
                dataframe[unit_col][idx] = 'MJ'

        elif dataframe.loc[idx, :][unit_col] == 'MWh' or dataframe.loc[idx, :][unit_col] == 'Mwh' :
            for col_index in data_col_arr:
                # 1MWh = 3600MJ
                dataframe[col_index][idx] = float(dataframe.loc[idx, :][col_index]) * 3600
                dataframe[unit_col][idx] = 'MJ'

        elif dataframe.loc[idx, :][unit_col] != 'MJ':
            # 맨 마지막까지 왔지만 단위가 메가줄도 아닐 경우, 오류를 출력
            print('Unidentified Unit Detected : Please add transform data in unify_energy_unit')
    return dataframe

def unify_energy_unit_for_file(filedir, data_col, unit_col = 'UNIT_CD'):
    # CSV 혹은 엑셀 파일을 불러와서 유닛을 통일시켜서 파일명 뒤에 _MJ_unified을 붙여서 저장
    if filedir.split('.')[1] == 'xlsx':
        df = pd.read_excel(filedir)
    elif filedir.split('.')[1] == 'csv':
        df = pd.read_csv(filedir)
    else:
        print('unknown filetype! please insert CSV or XLSX files.')

    result = unify_energy_unit(df, 'UNIT_CD', data_col)
    # 메가줄로 통일했으니 UNIT_CD가 필요없는 것 아닌지? drop하는 코드 나중에 따로 작성할 것.
    # 그리고 index행이 나오는 부분도 없애야 한다!
    result.to_excel(filedir.split('.')[0] + '_MJ_unified.' + filedir.split('.')[1])
    print('file saved!')


def read_data_from_excel(filedir):
    # xlsx와 csv에 맞춰서 읽어오도록 설정
    if filedir.split('.')[1] == 'xlsx':
        data = pd.read_excel(filedir)
    elif filedir.split('.')[1] == 'csv':
        data = pd.read_csv(filedir)
    else:
        print('unknown filetype! please insert CSV or XLSX files.')
    return data

def join_dataframes(index_colname, df_list):
    # index_colname행을 인덱스로 바꾸고, 데이터프레임들을 인덱스 기준으로 outer join시킴. 기존 인덱스는 사라진다!
    temp_df_list = []
    for df in df_list:
        # DB구조를 목적으로 하므로, 인덱스의 중복 또한 여기서 제거한다.
        temp_res = df.drop_duplicates([index_colname], keep='first')
        temp_res.set_index(index_colname, drop=True, inplace=True)
        temp_df_list.append(temp_res)
    # 합병을 위한 초기 데이터프레임을 0번을 복사해 생성
    result = temp_df_list[0]

    for i in range(len(temp_df_list)-1):
        print(result)
        print(temp_df_list[i+1])
        # 혹시 중첩이 있다면, 우항의 값에 dup을 붙인다.
        result = result.join(temp_df_list[i+1], how='outer', rsuffix='_dup')

    return result

import time

def txt_read_to_df(filedir):
    f = open(filedir, 'r')
    txt_arr = f.readlines()
    f.close()
    test_line = txt_arr[0].split('\n')[0]
    if '\t' in test_line:
        splitter = '\t'
    elif '|' in test_line:
        splitter = '|'
    header = txt_arr[0].split('\n')[0].split(splitter)
    txt_arr.pop()
    temp_arr = []
    for line in txt_arr:
        line_a = line.split('\n')[0]
        temp_arr.append(line_a.split(splitter))
    data = pd.DataFrame(temp_arr[1:], columns=header)
    return data

def txt_read_to_df_spc(filedir, header):
    f = open(filedir, 'r')
    txt_arr = f.readlines()
    f.close()
    temp_arr = []
    for line in txt_arr:
        line_a = line.split('\n')[0]
        line_a = line_a.split('|')
        res_line = line_a[16:]
        res_line.append(line_a[1])
        res_line.append(line_a[15])
        temp_arr.append(res_line)
    data = pd.DataFrame(temp_arr, columns=header)
    return data

def load_sql(cursor, load_query):
    cursor.execute(load_query)
    result = cursor.fetchall()
    return pd.DataFrame(result)


# 면적입력 코드
# 건축물대장, 에너지데이터(부동산원) 데이터를 끌어와서 Area DB를 만든다.
# DB구조는 PK단에서 이루어지며, 이 내용은 건축물대장 및 부동산원 업데이트시 초기화시킬 수 있도록 한다.
def build_area_database(cursor):
    # 1. 에너지데이터(부동산원) 정보를 취득
    query_string = 'select MGM_BLD_PK, TOTAREA from elec_attribute'
    elec_attr_res = load_sql(cursor, query_string)
    query_string = 'select MGM_BLD_PK, TOTAREA from gas_attribute'
    gas_attr_res = load_sql(cursor, query_string)
    query_string = 'select MGM_BLD_PK, TOTAREA from heat_attribute'
    heat_attr_res = load_sql(cursor, query_string)
    elec_attr_res.set_index('MGM_BLD_PK', drop=True, inplace=True)
    gas_attr_res.set_index('MGM_BLD_PK', drop=True, inplace=True)
    heat_attr_res.set_index('MGM_BLD_PK', drop=True, inplace=True)
    print(elec_attr_res)
    print(gas_attr_res)
    energy_db_res = fill_null(elec_attr_res, gas_attr_res, ['MGM_BLD_PK', 'totArea'])
    energy_db_res = fill_null(energy_db_res, heat_attr_res, ['MGM_BLD_PK', 'totArea'])
    energy_db_res.rename(columns={'TOTAREA':'TOTAREA_energydb', 'MGM_BLD_PK':'mgmBldrgstPk'}, inplace=True)

    # 2. 건축물대장 정보를 취득
    # 2-1. 총괄표제부 면적 취득
    query_string = 'select mgmBldrgstPk, totArea from building_legister_recaptitle_seoul'
    recaptitle_res = load_sql(cursor, query_string)
    recaptitle_res.rename(columns={'totArea':'TOTAREA_recaptitle'}, inplace=True)
    recaptitle_res.set_index('mgmBldrgstPk', drop=True, inplace=True)

    # 2-2. 표제부 면적 취득
    query_string = 'select mgmBldrgstPk, totArea from building_legister_title_seoul'
    title_res = load_sql(cursor, query_string)
    title_res.rename(columns={'totArea': 'TOTAREA_title'}, inplace=True)
    title_res.set_index('mgmBldrgstPk', drop=True, inplace=True)

    # 2-3. 층별면적 취득
    # PK가 같은 것들의 층별면적을 합함
    query_string = 'select mgmBldrgstPk, sum(area) from building_legister_floordata_seoul group by mgmBldrgstPk;'
    floor_res = load_sql(cursor, query_string)
    floor_res.rename(columns={'sum(area)':'TOTAREA_floorsum'}, inplace=True)
    floor_res.set_index('mgmBldrgstPk', drop=True, inplace=True)

    # 3. 병합
    merged_res = energy_db_res.join(recaptitle_res, how='outer')
    merged_res = merged_res.join(title_res, how='outer')
    merged_res = merged_res.join(floor_res, how='outer')

    # 4. 조정면적(TOTAREA_custom)과 선택 컬럼 만들기
    merged_res['TOTAREA_custom'] = ''
    merged_res['TOTAREA_selector'] = ''

    # 결과 데이터프레임을 db에 저장한다.
    # 저장에 앞선 기본값 설정
    db_connection_str = 'mysql+pymysql://root:atdt01410@127.0.0.1/energy_data'
    db_connection = sqlalchemy.create_engine(db_connection_str)
    data_type_matrix = {
        'mgmBldrgstPk':sqlalchemy.types.VARCHAR(33),
        'TOTAREA_energydb':sqlalchemy.types.VARCHAR(80),
        'TOTAREA_recaptitle':sqlalchemy.types.FLOAT,
        'TOTAREA_title':sqlalchemy.types.FLOAT,
        'TOTAREA_floorsum':sqlalchemy.types.FLOAT,
        'TOTAREA_custom':sqlalchemy.types.FLOAT,
        'TOTAREA_selector':sqlalchemy.types.VARCHAR(24),
    }

    print('connected')

    def input_db(dataframe, connection, table_name):
        dataframe.to_sql(name=table_name, con=connection, if_exists='replace', index=True, dtype=data_type_matrix, method='multi')
        print('Data saved to DB with table name: ' + str(table_name))

    input_db(result, db_connection, 'area_data')     # 수정해야 하는 주석

build_area_database(cursor)
raise IOError


data = pd.read_csv('C:/Users/Swellfish/Downloads/2021_res/gas_res.csv')

# 결과 데이터프레임을 db에 저장한다.
# 저장에 앞선 기본값 설정
db_connection_str = 'mysql+pymysql://root:atdt01410@127.0.0.1/energy_data'
db_connection = sqlalchemy.create_engine(db_connection_str)
data_type_matrix = {
    'MGM_BLD_PK':sqlalchemy.types.VARCHAR(33)
}

print('connected')

def input_db(dataframe, connection, table_name):
    dataframe.to_sql(name=table_name, con=connection, if_exists='replace', index=True, dtype=data_type_matrix)
    print('Data saved to DB with table name: ' + str(table_name))

input_db(data, db_connection, 'gas_2021')     # 수정해야 하는 주석

raise IOError




heat_data_01 = txt_read_to_df('C:/Users/user/Downloads/BDT_BLDRGST_HEAT_2004_2101.txt')
heat_data_01 = heat_data_01[['MGM_BLD_PK', 'HEAT_202101', 'UNIT_CD']]
elec_data_01 = txt_read_to_df('C:/Users/user/Downloads/BDT_BLDRGST_ELE_2004_2101.txt')
elec_data_01 = elec_data_01[['MGM_BLD_PK', 'ELE_202101']]
gas_data_01 = txt_read_to_df('C:/Users/user/Downloads/BDT_BLDRGST_GAS_2004_2101.txt')
gas_data_01 = gas_data_01[['MGM_BLD_PK', 'GAS_202101']]

heat_data_01 = unify_energy_unit(heat_data_01, 'UNIT_CD', ['HEAT_202101'])
heat_data_01.set_index('MGM_BLD_PK', inplace=True, drop=True)
elec_data_01.set_index('MGM_BLD_PK', inplace=True, drop=True)
gas_data_01.set_index('MGM_BLD_PK', inplace=True, drop=True)


heat_data_02 = txt_read_to_df('C:/Users/user/Downloads/HEAT_2102_2106.txt')
heat_data_02 = heat_data_02[['MGM_BLD_PK', 'HEAT_202102', 'HEAT_202103', 'HEAT_202104', 'HEAT_202105', 'HEAT_202106', 'UNIT_CD']]
elec_data_02 = txt_read_to_df('C:/Users/user/Downloads/ELE_2102_2106.txt')
elec_data_02 = elec_data_02[['MGM_BLD_PK', 'ELE_202102', 'ELE_202103', 'ELE_202104', 'ELE_202105', 'ELE_202106']]
gas_data_02 = txt_read_to_df('C:/Users/user/Downloads/GAS_2102_2106.txt')
print(gas_data_02.columns)
gas_data_02 = gas_data_02[['MGM_BLD_PK', 'GAS_202102', 'GAS_202103', 'GAS_202104', 'GAS_202105', 'GAS_202106']]

heat_data_02 = unify_energy_unit(heat_data_02, 'UNIT_CD', ['HEAT_202102', 'HEAT_202103', 'HEAT_202104', 'HEAT_202105', 'HEAT_202106'])
heat_data_02.set_index('MGM_BLD_PK', inplace=True, drop=True)
elec_data_02.set_index('MGM_BLD_PK', inplace=True, drop=True)
gas_data_02.set_index('MGM_BLD_PK', inplace=True, drop=True)

heat_data_03 = pd.read_excel('C:/Users/user/Downloads/서울_난방.xlsx', engine='openpyxl')
print(heat_data_03)
heat_data_03 = heat_data_03[['MGM_BLD_PK', 'HEAT_202107', 'HEAT_202108', 'HEAT_202109', 'UNIT_CD']]
elec_data_03 = pd.read_excel('C:/Users/user/Downloads/서울_전기_2107_2109.xlsx', engine='openpyxl')
elec_data_03 = elec_data_03[['MGM_BLD_PK', 'ELE_202107', 'ELE_202108', 'ELE_202109']]
gas_data_03 = pd.read_excel('C:/Users/user/Downloads/서울_도시가스.xlsx', engine='openpyxl')
gas_data_03 = gas_data_03[['MGM_BLD_PK', 'GAS_202107', 'GAS_202108', 'GAS_202109']]

heat_data_03 = unify_energy_unit(heat_data_03, 'UNIT_CD', ['HEAT_202107', 'HEAT_202108', 'HEAT_202109'])
heat_data_03.set_index('MGM_BLD_PK', inplace=True, drop=True)
elec_data_03.set_index('MGM_BLD_PK', inplace=True, drop=True)
gas_data_03.set_index('MGM_BLD_PK', inplace=True, drop=True)


heat_data_04 = txt_read_to_df_spc('C:/Users/user/Downloads/난방_2104_2112.txt', ['HEAT_202104', 'HEAT_202105', 'HEAT_202106', 'HEAT_202107', 'HEAT_202108', 'HEAT_202109', 'HEAT_202110', 'HEAT_202111', 'HEAT_202112', 'MGM_BLD_PK', 'UNIT_CD'])
print(heat_data_04.head())
heat_data_04 = unify_energy_unit(heat_data_04, 'UNIT_CD', ['HEAT_202104', 'HEAT_202105', 'HEAT_202106', 'HEAT_202107', 'HEAT_202108', 'HEAT_202109', 'HEAT_202110', 'HEAT_202111', 'HEAT_202112'])
elec_data_04 = txt_read_to_df_spc('C:/Users/user/Downloads/전기_2104_2112.txt', ['ELE_202104', 'ELE_202105', 'ELE_202106', 'ELE_202107', 'ELE_202108', 'ELE_202109', 'ELE_202110', 'ELE_202111', 'ELE_202112', 'MGM_BLD_PK', 'UNIT_CD'])
elec_data_04 = elec_data_04[['MGM_BLD_PK', 'ELE_202104', 'ELE_202105', 'ELE_202106', 'ELE_202107', 'ELE_202108', 'ELE_202109', 'ELE_202110', 'ELE_202111', 'ELE_202112']]
gas_data_04 = txt_read_to_df_spc('C:/Users/user/Downloads/도시가스_2104_2112.txt', ['GAS_202104', 'GAS_202105', 'GAS_202106', 'GAS_202107', 'GAS_202108', 'GAS_202109', 'GAS_202110', 'GAS_202111', 'GAS_202112', 'MGM_BLD_PK', 'UNIT_CD'])
gas_data_04 = gas_data_04[['MGM_BLD_PK', 'GAS_202104', 'GAS_202105', 'GAS_202106', 'GAS_202107', 'GAS_202108', 'GAS_202109', 'GAS_202110', 'GAS_202111', 'GAS_202112']]

heat_data_04 = heat_data_04[['MGM_BLD_PK', 'HEAT_202110', 'HEAT_202111', 'HEAT_202112']]
elec_data_04 = elec_data_04[['MGM_BLD_PK', 'ELE_202110', 'ELE_202111', 'ELE_202112']]
gas_data_04 = gas_data_04[['MGM_BLD_PK', 'GAS_202110', 'GAS_202111', 'GAS_202112']]

heat_data_04.set_index('MGM_BLD_PK', inplace=True, drop=True)
elec_data_04.set_index('MGM_BLD_PK', inplace=True, drop=True)
gas_data_04.set_index('MGM_BLD_PK', inplace=True, drop=True)

heat_res = heat_data_01.join(heat_data_02, how='outer', rsuffix='_02')
heat_res = heat_res.join(heat_data_03, how='outer', rsuffix='_03')
heat_res = heat_res.join(heat_data_04, how='outer', rsuffix='_04')

elec_res = elec_data_01.join(elec_data_02, how='outer', rsuffix='_02')
elec_res = elec_res.join(elec_data_03, how='outer', rsuffix='_03')
elec_res = elec_res.join(elec_data_04, how='outer', rsuffix='_04')

gas_res = gas_data_01.join(gas_data_02, how='outer', rsuffix='_02')
gas_res = gas_res.join(gas_data_03, how='outer', rsuffix='_03')
gas_res = gas_res.join(gas_data_04, how='outer', rsuffix='_04')

print(heat_res)

heat_res.to_csv('C:/Users/user/Downloads/heat_res.csv')
elec_res.to_csv('C:/Users/user/Downloads/elec_res.csv')
gas_res.to_csv('C:/Users/user/Downloads/gas_res.csv')

raise IOError

# unit_col의 단위를 기준으로 data_col에 해당하는 값들의 단위를 통일시킴

'''unit_col = 'UNIT_CD'
data_col_202004_202109 = ['HEAT_202004', 'HEAT_202005', 'HEAT_202006', 'HEAT_202007', 'HEAT_202008', 'HEAT_202009',
                          'HEAT_202010', 'HEAT_202011', 'HEAT_202012', 'HEAT_202101', 'HEAT_202102', 'HEAT_202103',
                          'HEAT_202104', 'HEAT_202105', 'HEAT_202106', 'HEAT_202107', 'HEAT_202108', 'HEAT_202109']
data_col_201701_202003 = ['HEAT_201701', 'HEAT_201702', 'HEAT_201703', 'HEAT_201704', 'HEAT_201705', 'HEAT_201706',
                          'HEAT_201707', 'HEAT_201708', 'HEAT_201709', 'HEAT_201710', 'HEAT_201711', 'HEAT_201712',
                          'HEAT_201801', 'HEAT_201802', 'HEAT_201803', 'HEAT_201804', 'HEAT_201805', 'HEAT_201806',
                          'HEAT_201807', 'HEAT_201808', 'HEAT_201809', 'HEAT_201810', 'HEAT_201811', 'HEAT_201812',
                          'HEAT_201901', 'HEAT_201902', 'HEAT_201903', 'HEAT_201904', 'HEAT_201905', 'HEAT_201906',
                          'HEAT_201907', 'HEAT_201908', 'HEAT_201909', 'HEAT_201910', 'HEAT_201911', 'HEAT_201912',
                          'HEAT_202001', 'HEAT_202002', 'HEAT_202003']



#unify_energy_unit_for_file('HEAT_1701_2003.xlsx', data_col_201701_202003)
unify_energy_unit_for_file('HEAT_2004_2109.xlsx', data_col_202004_202109, unit_col)'''


# 파일에서 데이터프레임을 읽어옴
data_1 = read_data_from_excel('GAS_1701_2003.xlsx')
data_2 = read_data_from_excel('GAS_2004_2109.xlsx')

# PK만 이름을 먼저 바꿔 준다...
data_1.rename(columns={'MGM_BLD_PK':'PK'}, inplace=True)
data_2.rename(columns={'MGM_BLD_PK':'PK'}, inplace=True)

pk_name = 'PK'

result = join_dataframes(pk_name, [data_1, data_2])

# [주석 컨트롤] column의 이름을 목적 DB에 맞도록 조정함. 이 경우는 메뉴얼로 바꿔 두었으니 두 번째만 쓴다.
result.rename(columns=attrdata_db_matrix_another, inplace=True)
result.rename(columns=namematrix_gas, inplace=True)        # 수정해야 하는 주석

# 결과 데이터프레임을 db에 저장한다.
# 저장에 앞선 기본값 설정
db_connection_str = 'mysql+pymysql://root:atdt01410@127.0.0.1/energy_data'
db_connection = sqlalchemy.create_engine(db_connection_str)
data_type_matrix = {
    'PK':sqlalchemy.types.VARCHAR(33),
    'group_label':sqlalchemy.types.VARCHAR(80),
    'regi_label':sqlalchemy.types.VARCHAR(10),
    'gu':sqlalchemy.types.VARCHAR(50),
    'dong':sqlalchemy.types.VARCHAR(50),
    'land_label':sqlalchemy.types.VARCHAR(4),
    'main':sqlalchemy.types.VARCHAR(4),
    'sub':sqlalchemy.types.VARCHAR(4),
    'JUSO':sqlalchemy.types.VARCHAR(236),
    'ROAD_JUSO':sqlalchemy.types.VARCHAR(289),
    'tot_area':sqlalchemy.types.FLOAT,
    'USEAPR_DAY':sqlalchemy.types.VARCHAR(8),
    'no_house':sqlalchemy.types.INT,
    'usage':sqlalchemy.types.VARCHAR(500)
}

print('connected')

def input_db(dataframe, connection, table_name):
    dataframe.to_sql(name=table_name, con=connection, if_exists='replace', index=True, dtype=data_type_matrix, method='multi')
    print('Data saved to DB with table name: ' + str(table_name))

input_db(result, db_connection, 'gas')     # 수정해야 하는 주석


# cursor = energy_db_another.cursor(pymysql.cursors.DictCursor)
#
# table_list = ['heat']
# for table_name in table_list:
#     query_for_PK = 'ALTER TABLE ' + table_name + ' MODIFY ' + pk_name + ' VARCHAR(33) not null Primary Key'
#     cursor.execute(query_for_PK)


# 메모용 덤프커맨드 (CMD - sql서버 bin디렉터리 내에서 실행)
# mysqldump -u[username] -p[password] [database name] > [dumpfile name (.sql extension)]
# 덤프로 복원시에는 < 로 반대방향 입력.




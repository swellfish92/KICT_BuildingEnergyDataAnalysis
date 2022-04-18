import scipy as sp
import scipy.stats
import pymysql
import pandas as pd
from functions import *
import numpy as np
import sqlalchemy
import sys
# from db_read import *

# 텍스트파일로 받아오는 서울시 데이터를 읽어들이는 함수
# 예외적으로 이 파일을 run해서 DB에 집어넣도록 한다 (main과의 분리를 위함)

# ======================================================================================================================
# APPENDIX
# 참조를 위해 받은 sample data와 DB에 넣기 위한 변수명의 테이블을 이곳에 작성함. Dict형태로 저장
# ['건축물_유형','관리건축물_PK','건축물_구분','건축물_종류','시군구_명','법정동_명','대지_구분','주번지','부번지','주소','도로명_주소','연면적','세대_개수','용동_명','단위_명']
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

# dtype지정을 위한 딕셔너리
data_type_matrix = {
'BLD_TYPE_GB_CD':sqlalchemy.types.VARCHAR(80),
'MGM_BLD_PK':sqlalchemy.types.VARCHAR(33),
'REGSTR_GB_CD':sqlalchemy.types.VARCHAR(80),
'REGSTR_KIND_CD':sqlalchemy.types.VARCHAR(10),
'SIGUNGU_NM':sqlalchemy.types.VARCHAR(50),
'BJDONG_NM':sqlalchemy.types.VARCHAR(50),
'PLAT_GB_CD':sqlalchemy.types.VARCHAR(4),
'BUN':sqlalchemy.types.VARCHAR(4),
'JI':sqlalchemy.types.VARCHAR(4),
'JUSO':sqlalchemy.types.VARCHAR(236),
'ROAD_JUSO':sqlalchemy.types.VARCHAR(289),
'TOTAREA':sqlalchemy.types.FLOAT,
'USEAPR_DAY':sqlalchemy.types.VARCHAR(8),
'HHLD_CNT':sqlalchemy.types.INT,
'MAIN_PURPS_NM':sqlalchemy.types.VARCHAR(500),
'UNIT_CD':sqlalchemy.types.VARCHAR(8)
}
# ======================================================================================================================

'''energy_db = pymysql.connect(
    user = 'root',
    passwd = 'atdt01410',
    host = '127.0.0.1',
    db = 'energy_data',
    charset = 'utf8'
)

# Cursor 세팅 및 Sql 쿼리 사전정의
cursor = energy_db.cursor(pymysql.cursors.DictCursor)'''

# sqlalchemy 용으로 따로 만듬
db_connection_str = 'mysql+pymysql://root:atdt01410@127.0.0.1/energy_data'
db_connection = sqlalchemy.create_engine(db_connection_str)

def get_dtype(arr):
    temp_dict = {}
    for item in arr:
        if item in data_type_matrix.keys():
            temp_dict[item] = data_type_matrix[item]
    return temp_dict

def get_year_month_arr(string, year):
    # 식별을 위한 PK코드는 무조건 들어가야 함!
    temp_arr = ['MGM_BLD_PK']
    for i in range(1, 13):
        temp_arr.append(string+'_'+str(year)+str(i).zfill(2))
    return temp_arr

def read_df_from_text(dir, energy_type, year_arr, seperator=',', encoding='ANSI'):
    read_data = pd.read_csv(dir, sep=seperator, engine='python', encoding='cp949')
    read_data.rename(columns=attrdata_db_matrix, inplace=True)
    # 읽어오자마자 가장 먼저 PK인 MGM_BLD_PK의 중복을 제거한다. 맨 위에 있는 것을 유지시킴.
    read_data = read_data.drop_duplicates(['MGM_BLD_PK'], keep='first')

    # 기본 데이터(속성데이터)를 따로 떼놓음 (연도별 테이블 작성을 위해서임. 근데 이것도 따로 떼놓아도 될 듯?
    attr_label = ['BLD_TYPE_GB_CD','MGM_BLD_PK','REGSTR_GB_CD','REGSTR_KIND_CD','SIGUNGU_NM','BJDONG_NM','PLAT_GB_CD','BUN','JI','JUSO','ROAD_JUSO','TOTAREA','HHLD_CNT','MAIN_PURPS_NM','UNIT_CD']
    attr_data = read_data[attr_label]

    # 연도별로 뗴서 저장함. 연도는 입력한 year_arr의 순서를 따른다. 입력시 오름차순으로 입력하면 simple해질듯? 현재는 배열은 없음.
    result_arr = []
    # result_arr의 0번은 무조건 속성값
    result_arr.append(attr_data)
    # 연도별 데이터를 저장
    for year in year_arr:
        temp_data = read_data[get_year_month_arr(energy_type, year)]
        # 데이터 값이 없으면(NaN), 0으로 채움
        temp_data = temp_data.fillna(0)
        result_arr.append(temp_data)

    # 2020년은 3월까지밖에 없어서 대응을 위한 로직을 별도로 마련함
    # temp_data = read_data[['MGM_BLD_PK', energy_type+'_202001', energy_type+'_202002', energy_type+'_202003']]
    # temp_data = temp_data.fillna(0)

    # GAS/ELEC의 2020년 공란 (3월 이후 데이터)을 채우기 위한 방편임. 2020년 데이터는 쓰지 않는 것이 좋을 듯?
    # if energy_type == 'ELEC' or 'GAS':
    #     temp_data[energy_type + '_202004'] = 0
    #     temp_data[energy_type + '_202005'] = 0
    #     temp_data[energy_type + '_202006'] = 0
    #     temp_data[energy_type + '_202007'] = 0
    #     temp_data[energy_type + '_202008'] = 0
    #     temp_data[energy_type + '_202009'] = 0
    #     temp_data[energy_type + '_202010'] = 0
    #     temp_data[energy_type + '_202011'] = 0
    #     temp_data[energy_type + '_202012'] = 0
    # result_arr.append(temp_data)

    return result_arr

def input_db(dataframe, connection, table_name):
    dataframe.to_sql(name=table_name, con=connection, if_exists='replace', index=False, dtype=get_dtype(dataframe.columns.tolist()))
    print('Data saved to DB with table name: ' + str(table_name))


# ======================================================================================================================
year_arr = ['2014', '2015', '2016', '2017', '2018', '2019']
#year_arr = ['2020', '2021']
energy_type = 'GAS'
energy_type_lowercase = 'gas'   # DB규칙을 위한 소문자 값.
txt_read_result = read_df_from_text('./BDT_BLDRGST_GAS.txt', energy_type, year_arr, seperator='\t', encoding='cp949')

# DB저장을 위한 테이블 이름배열 작성
arr_for_dbsave = [energy_type_lowercase+'_attribute']
for item in year_arr:
    arr_for_dbsave.append(energy_type_lowercase+'_'+item)

# 여기도 마찬가지로 2020년도를 위한 예외가 필요함 (year_arr에 들어가지 않기 때문.)
# arr_for_dbsave.append(energy_type_lowercase+'_2020')

print(arr_for_dbsave)

# 오류를 방지하기 위해 테이블 길이를 비교하고 이상하면 종료시킴
if len(arr_for_dbsave) != len(txt_read_result):
    print('ERROR: array length for DB saving is different.')
    sys.exit(0)

print('length confirmed, starting saving data with the table names below:')
print(arr_for_dbsave)
i = 0
for dataframe in txt_read_result:
    input_db(dataframe, db_connection, arr_for_dbsave[i])
    i = i + 1

# print(get_year_month_arr('GAS', 2021))





import scipy as sp
import scipy.stats
import pymysql
import pandas as pd
from functions import *
import numpy as np
import sqlalchemy
import time

from functions import *
from DB_INPUT.db_insert_functions import *

# 건축물인허가 기본개요를 입력하기 위한 로직

'''energy_db = pymysql.connect(
    user = 'root',
    passwd = 'atdt01410',
    host = '127.0.0.1',
    db = 'energy_data',
    charset = 'utf8'
)'''

# data.go.kr과 통일시키기 위한 딕셔너리
apikey_eng_dict = {
    '관리_허가대장_PK': 'mgmPmsrgstPk',
    '대지_위치': 'platPlc',
    '건물_명': 'bldNm',
    '시군구_코드': 'sigunguCd',
    '법정동_코드': 'bjdongCd',
    '대지_구분_코드': 'platGbCd',
    '번': 'bun',
    '지': 'ji',
    '특수지_명': 'splotNm',
    '블록': 'block',
    '로트': 'lot',
    '지목_코드_명': 'jimokCdNm',
    '지역_코드_명': 'juyukCdNm',
    '지구_코드_명': 'jiguCdNm',
    '구역_코드_명': 'guyukCdNm',
    '지목_코드': 'jimokCd',
    '지역_코드': 'juyukCd',
    '지구_코드': 'jiguCd',
    '구역_코드': 'guyukCd',
    '건축_구분_코드': 'archGbCd',
    '건축_구분_코드_명': 'archGbCdNm',
    '대지_면적(㎡)': 'platArea',
    '건축_면적(㎡)': 'archArea',
    '건폐_율(%)': 'bcRat',
    '연면적(㎡)': 'totArea',
    '용적_률_산정_연면적(㎡)': 'vlRatEstmTotArea',
    '용적_률(%)': 'vlRat',
    '주_건축물_수': 'mainBldCnt',
    '부속_건축물_동_수': 'atchBldCnt',
    '주_용도_코드': 'mainPurpsCd',
    '주_용도_코드_명': 'mainPurpsCdNm',
    '세대_수(세대)': 'hhldCnt',
    '호_수(호)': 'hoCnt',
    '가구_수(가구)': 'fmlyCnt',
    '총_주차_수': 'totPkngCnt',
    '착공_예정_일': 'stcnsSchedDay',
    '착공_연기_일': 'stcnsDelayDay',
    '실제_착공_일': 'realStcnsDay',
    '건축_허가_일': 'archPmsDay',
    '사용승인_일': 'useAprDay',
    '생성_일자': 'crtnDay'
}

# energy_db_another = pymysql.connect(
#     user = 'root',
#     passwd = 'atdt01410',
#     host = '127.0.0.1',
#     db = 'energy_data_another',
#     charset = 'utf8'
# )

# 파일 데이터를 로드
f = open('C:/Users/user/Downloads/mart_djy_01.txt', 'r')
line_arr = f.readlines()
f.close()
print(line_arr)
print(len(line_arr))
time.sleep(10000)
sgg_arr = ['11740', '11290', '11530', '11305', '11410', '11500', '11440', '11710', '11230', '11140', '11110', '11350', '11680', '11560', '11620', '11590', '11200', '11170', '11380', '11260', '11215', '11545', '11320', '11650', '11470', '11000']

temp_res = []
for i in range(41):
    temp_res.append([])

for element in line_arr:
    element_mod = element.split('\n')[0]
    #print(element_mod)
    splitted_arr = element_mod.split('|')
    if str(splitted_arr[3]) in sgg_arr:    # 다른 파일을 쓸 때는 여기도 반드시 체크할 것
        for i in range(len(splitted_arr)):
            temp_res[i].append(splitted_arr[i])

key_arr = read_eais_basedata(1, 'C:/Users/Swellfish/Downloads/건축인허가_기본개요.xls', apikey_eng_dict)
base_df = make_basedict(key_arr, temp_res, type='df')

base_df.to_csv('tempresult_archapproval_basicinfo_Seoul.csv', encoding='utf-8-sig')
print('csv exported')

# 결과 데이터프레임을 db에 저장한다.
# 저장에 앞선 기본값 설정
db_connection_str = 'mysql+pymysql://root:atdt01410@127.0.0.1/energy_data'
db_connection = sqlalchemy.create_engine(db_connection_str)
data_type_matrix = read_eais_basedata(2, 'C:/Users/Swellfish/Downloads/건축인허가_기본개요.xls', apikey_eng_dict)
print('connected')
print(data_type_matrix)

# NUMERIC에 '' 입력이 안되므로 NULL로 바꾸어 주어야 한다.
for key in data_type_matrix.keys():
    if 'NUMERIC' in str(type(data_type_matrix[key])):
        base_df[key].replace('', None, inplace=True)

def input_db(dataframe, connection, table_name):
    dataframe.to_sql(name=table_name, con=connection, if_exists='replace', index=True, dtype=data_type_matrix)
    print('Data saved to DB with table name: ' + str(table_name))

input_db(base_df, db_connection, 'building_approval_basicinfo_seoul')     # 수정해야 하는 주석


# cursor = energy_db_another.cursor(pymysql.cursors.DictCursor)
#
# table_list = ['heat']
# for table_name in table_list:
#     query_for_PK = 'ALTER TABLE ' + table_name + ' MODIFY ' + pk_name + ' VARCHAR(33) not null Primary Key'
#     cursor.execute(query_for_PK)


# 메모용 덤프커맨드 (CMD - sql서버 bin디렉터리 내에서 실행)
# mysqldump -u[username] -p[password] [database name] > [dumpfile name (.sql extension)]
# 덤프로 복원시에는 < 로 반대방향 입력.

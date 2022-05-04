import scipy as sp
import scipy.stats
import pymysql
import pandas as pd
from functions import *
import numpy as np
import sqlalchemy

from functions import *

# energy_db = pymysql.connect(
#     user = 'root',
#     passwd = 'atdt01410',
#     host = '127.0.0.1',
#     db = 'energy_data',
#     charset = 'utf8'
# )
#
# energy_db_another = pymysql.connect(
#     user = 'root',
#     passwd = 'atdt01410',
#     host = '127.0.0.1',
#     db = 'energy_data_another',
#     charset = 'utf8'
# )

# 파일 데이터를 로드
f = open('C:/Users/user/Downloads/국토교통부_건축물대장_표제부+(2022년+03월)/mart_djy_03.txt', 'r')
line_arr = f.readlines()
f.close()

temp_res = []
for i in range(77):
    temp_res.append([])

for element in line_arr:
    element_mod = element.split('\n')[0]
    print(element_mod)
    splitted_arr = element_mod.split('|')
    for i in range(len(splitted_arr)):
        temp_res[i].append(splitted_arr[i])

base_dict = {
'mgmBldrgstPk' : temp_res[1],
'regstrGbCd' : temp_res[2],
'regstrGbCdNm' : temp_res[3],
'regstrKindCd' : temp_res[4],
'regstrKindCdNm' : temp_res[5],
'platPlc' : temp_res[6],
'newPlatPlc' : temp_res[7],
'bldNm' : temp_res[8],
'sigunguCd' : temp_res[9],
'bjdongCd' : temp_res[10],
'platGbCd' : temp_res[11],
'bun' : temp_res[12],
'ji' : temp_res[13],
'splotNm' : temp_res[14],
'block' : temp_res[15],
'lot' : temp_res[16],
'bylotCnt' : temp_res[17],
'naRoadCd' : temp_res[18],
'naBjdongCd' : temp_res[19],
'naUgrndCd' : temp_res[20],
'naMainBun' : temp_res[21],
'naSubBun' : temp_res[22],
'dongNm' : temp_res[23],
'mainAtchGbCd' : temp_res[24],
'mainAtchGbCdNm' : temp_res[25],
'platArea' : temp_res[26],
'archArea' : temp_res[27],
'bcRat' : temp_res[28],
'totArea' : temp_res[29],
'vlRatEstmTotArea' : temp_res[30],
'vlRat' : temp_res[31],
'strctCd' : temp_res[32],
'strctCdNm' : temp_res[33],
'etcStrct' : temp_res[34],
'mainPurpsCd' : temp_res[35],
'mainPurpsCdNm' : temp_res[36],
'etcPurps' : temp_res[37],
'roofCd' : temp_res[38],
'roofCdNm' : temp_res[39],
'etcRoof' : temp_res[40],
'hhldCnt' : temp_res[41],
'fmlyCnt' : temp_res[42],
'heit' : temp_res[43],
'grndFlrCnt' : temp_res[44],
'ugrndFlrCnt' : temp_res[45],
'rideUseElvtCnt' : temp_res[46],
'emgenUseElvtCnt' : temp_res[47],
'atchBldCnt' : temp_res[48],
'atchBldArea' : temp_res[49],
'totDongTotArea' : temp_res[50],
'indrMechUtcnt' : temp_res[51],
'indrMechArea' : temp_res[52],
'oudrMechUtcnt' : temp_res[53],
'oudrMechArea' : temp_res[54],
'indrAutoUtcnt' : temp_res[55],
'indrAutoArea' : temp_res[56],
'oudrAutoUtcnt' : temp_res[57],
'oudrAutoArea' : temp_res[58],
'pmsDay' : temp_res[59],
'stcnsDay' : temp_res[60],
'useAprDay' : temp_res[61],
'pmsnoYear' : temp_res[62],
'pmsnoKikCd' : temp_res[63],
'pmsnoKikCdNm' : temp_res[64],
'pmsnoGbCd' : temp_res[65],
'pmsnoGbCdNm' : temp_res[66],
'hoCnt' : temp_res[67],
'engrGrade' : temp_res[68],
'engrRat' : temp_res[69],
'engrEpi' : temp_res[70],
'gnBldGrade' : temp_res[71],
'gnBldCert' : temp_res[72],
'itgBldGrade' : temp_res[73],
'itgBldCert' : temp_res[74],
'crtnDay' : temp_res[75],
'rserthqkDsgnApplyYn' : temp_res[76],
'rserthqkAblty' : temp_res[77]
}

base_df = pd.DataFrame(base_dict)


# 결과 데이터프레임을 db에 저장한다.
# 저장에 앞선 기본값 설정
db_connection_str = 'mysql+pymysql://root:atdt01410@127.0.0.1/energy_data'
db_connection = sqlalchemy.create_engine(db_connection_str, use_batch_mode=True)
data_type_matrix = {
    'mgmBldrgstPk' : sqlalchemy.types.VARCHAR(33),
    'regstrGbCd' : sqlalchemy.types.VARCHAR(1),
    'regstrGbCdNm' : sqlalchemy.types.VARCHAR(100),
    'regstrKindCd' : sqlalchemy.types.VARCHAR(1),
    'regstrKindCdNm' : sqlalchemy.types.VARCHAR(100),
    'platPlc' : sqlalchemy.types.VARCHAR(500),
    'newPlatPlc' : sqlalchemy.types.VARCHAR(400),
    'bldNm' : sqlalchemy.types.VARCHAR(100),
    'sigunguCd' : sqlalchemy.types.VARCHAR(5),
    'bjdongCd' : sqlalchemy.types.VARCHAR(5),
    'platGbCd' : sqlalchemy.types.VARCHAR(1),
    'bun' : sqlalchemy.types.VARCHAR(4),
    'ji' : sqlalchemy.types.VARCHAR(4),
    'splotNm' : sqlalchemy.types.VARCHAR(200),
    'block' : sqlalchemy.types.VARCHAR(20),
    'lot' : sqlalchemy.types.VARCHAR(20),
    'bylotCnt' : sqlalchemy.types.INT,
    'naRoadCd' : sqlalchemy.types.VARCHAR(12),
    'naBjdongCd' : sqlalchemy.types.VARCHAR(5),
    'naUgrndCd' : sqlalchemy.types.VARCHAR(1),
    'naMainBun' : sqlalchemy.types.INT,
    'naSubBun' : sqlalchemy.types.INT,
    'dongNm' : sqlalchemy.types.VARCHAR(100),
    'mainAtchGbCd' : sqlalchemy.types.CHAR(1),
    'mainAtchGbCdNm' : sqlalchemy.types.VARCHAR(100),
    'platArea' : sqlalchemy.types.FLOAT,
    'archArea' : sqlalchemy.types.FLOAT,
    'bcRat' : sqlalchemy.types.FLOAT,
    'totArea' : sqlalchemy.types.FLOAT,
    'vlRatEstmTotArea' : sqlalchemy.types.FLOAT,
    'vlRat' : sqlalchemy.types.FLOAT,
    'strctCd' : sqlalchemy.types.VARCHAR(2),
    'strctCdNm' : sqlalchemy.types.VARCHAR(100),
    'etcStrct' : sqlalchemy.types.VARCHAR(500),
    'mainPurpsCd' : sqlalchemy.types.VARCHAR(5),
    'mainPurpsCdNm' : sqlalchemy.types.VARCHAR(100),
    'etcPurps' : sqlalchemy.types.VARCHAR(500),
    'roofCd' : sqlalchemy.types.VARCHAR(2),
    'roofCdNm' : sqlalchemy.types.VARCHAR(100),
    'etcRoof' : sqlalchemy.types.VARCHAR(500),
    'hhldCnt' : sqlalchemy.types.INT,
    'fmlyCnt' : sqlalchemy.types.INT,
    'heit' : sqlalchemy.types.FLOAT,
    'grndFlrCnt' : sqlalchemy.types.INT,
    'ugrndFlrCnt' : sqlalchemy.types.INT,
    'rideUseElvtCnt' : sqlalchemy.types.INT,
    'emgenUseElvtCnt' : sqlalchemy.types.INT,
    'atchBldCnt' : sqlalchemy.types.INT,
    'atchBldArea' : sqlalchemy.types.FLOAT,
    'totDongTotArea' : sqlalchemy.types.FLOAT,
    'indrMechUtcnt' : sqlalchemy.types.INT,
    'indrMechArea' : sqlalchemy.types.FLOAT,
    'oudrMechUtcnt' : sqlalchemy.types.INT,
    'oudrMechArea' : sqlalchemy.types.FLOAT,
    'indrAutoUtcnt' : sqlalchemy.types.INT,
    'indrAutoArea' : sqlalchemy.types.FLOAT,
    'oudrAutoUtcnt' : sqlalchemy.types.INT,
    'oudrAutoArea' : sqlalchemy.types.FLOAT,
    'pmsDay' : sqlalchemy.types.VARCHAR(8),
    'stcnsDay' : sqlalchemy.types.VARCHAR(8),
    'useAprDay' : sqlalchemy.types.VARCHAR(8),
    'pmsnoYear' : sqlalchemy.types.VARCHAR(4),
    'pmsnoKikCd' : sqlalchemy.types.CHAR(7),
    'pmsnoKikCdNm' : sqlalchemy.types.VARCHAR(100),
    'pmsnoGbCd' : sqlalchemy.types.VARCHAR(4),
    'pmsnoGbCdNm' : sqlalchemy.types.VARCHAR(100),
    'hoCnt' : sqlalchemy.types.INT,
    'engrGrade' : sqlalchemy.types.VARCHAR(4),
    'engrRat' : sqlalchemy.types.FLOAT,
    'engrEpi' : sqlalchemy.types.FLOAT,
    'gnBldGrade' : sqlalchemy.types.CHAR(1),
    'gnBldCert' : sqlalchemy.types.FLOAT,
    'itgBldGrade' : sqlalchemy.types.CHAR(1),
    'itgBldCert' : sqlalchemy.types.FLOAT,
    'crtnDay' : sqlalchemy.types.VARCHAR(8),
    'rserthqkDsgnApplyYn' : sqlalchemy.types.VARCHAR(1),
    'rserthqkAblty' : sqlalchemy.types.VARCHAR(200)
}

print('connected')

def input_db(dataframe, connection, table_name):
    dataframe.to_sql(name=table_name, con=connection, if_exists='replace', index=True, dtype=data_type_matrix, method='multi')
    print('Data saved to DB with table name: ' + str(table_name))

input_db(base_df, db_connection, 'Building_legister_title')     # 수정해야 하는 주석


# cursor = energy_db_another.cursor(pymysql.cursors.DictCursor)
#
# table_list = ['heat']
# for table_name in table_list:
#     query_for_PK = 'ALTER TABLE ' + table_name + ' MODIFY ' + pk_name + ' VARCHAR(33) not null Primary Key'
#     cursor.execute(query_for_PK)


# 메모용 덤프커맨드 (CMD - sql서버 bin디렉터리 내에서 실행)
# mysqldump -u[username] -p[password] [database name] > [dumpfile name (.sql extension)]
# 덤프로 복원시에는 < 로 반대방향 입력.

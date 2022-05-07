import scipy as sp
import scipy.stats
import pymysql
import pandas as pd
from functions import *
import numpy as np
import sqlalchemy

from functions import *

'''energy_db = pymysql.connect(
    user = 'root',
    passwd = 'atdt01410',
    host = '127.0.0.1',
    db = 'energy_data',
    charset = 'utf8'
)'''

# energy_db_another = pymysql.connect(
#     user = 'root',
#     passwd = 'atdt01410',
#     host = '127.0.0.1',
#     db = 'energy_data_another',
#     charset = 'utf8'
# )

# 파일 데이터를 로드
f = open('C:/Users/user/Downloads/mart_djy_03.txt', 'r')
line_arr = f.readlines()
f.close()

sgg_arr = ['11740', '11290', '11530', '11305', '11410', '11500', '11440', '11710', '11230', '11140', '11110', '11350', '11680', '11560', '11620', '11590', '11200', '11170', '11380', '11260', '11215', '11545', '11320', '11650', '11470', '11000']

temp_res = []
for i in range(77):
    temp_res.append([])

for element in line_arr:
    element_mod = element.split('\n')[0]
    #print(element_mod)
    splitted_arr = element_mod.split('|')
    if str(splitted_arr[8]) in sgg_arr:
        for i in range(len(splitted_arr)):
            temp_res[i].append(splitted_arr[i])

base_dict = {
'mgmBldrgstPk' : temp_res[0],
'regstrGbCd' : temp_res[1],
'regstrGbCdNm' : temp_res[2],
'regstrKindCd' : temp_res[3],
'regstrKindCdNm' : temp_res[4],
'platPlc' : temp_res[5],
'newPlatPlc' : temp_res[6],
'bldNm' : temp_res[7],
'sigunguCd' : temp_res[8],
'bjdongCd' : temp_res[9],
'platGbCd' : temp_res[10],
'bun' : temp_res[11],
'ji' : temp_res[12],
'splotNm' : temp_res[13],
'block' : temp_res[14],
'lot' : temp_res[15],
'bylotCnt' : temp_res[16],
'naRoadCd' : temp_res[17],
'naBjdongCd' : temp_res[18],
'naUgrndCd' : temp_res[19],
'naMainBun' : temp_res[20],
'naSubBun' : temp_res[21],
'dongNm' : temp_res[22],
'mainAtchGbCd' : temp_res[23],
'mainAtchGbCdNm' : temp_res[24],
'platArea' : temp_res[25],
'archArea' : temp_res[26],
'bcRat' : temp_res[27],
'totArea' : temp_res[28],
'vlRatEstmTotArea' : temp_res[29],
'vlRat' : temp_res[30],
'strctCd' : temp_res[31],
'strctCdNm' : temp_res[32],
'etcStrct' : temp_res[33],
'mainPurpsCd' : temp_res[34],
'mainPurpsCdNm' : temp_res[35],
'etcPurps' : temp_res[36],
'roofCd' : temp_res[37],
'roofCdNm' : temp_res[38],
'etcRoof' : temp_res[39],
'hhldCnt' : temp_res[40],
'fmlyCnt' : temp_res[41],
'heit' : temp_res[42],
'grndFlrCnt' : temp_res[43],
'ugrndFlrCnt' : temp_res[44],
'rideUseElvtCnt' : temp_res[45],
'emgenUseElvtCnt' : temp_res[46],
'atchBldCnt' : temp_res[47],
'atchBldArea' : temp_res[48],
'totDongTotArea' : temp_res[49],
'indrMechUtcnt' : temp_res[50],
'indrMechArea' : temp_res[51],
'oudrMechUtcnt' : temp_res[52],
'oudrMechArea' : temp_res[53],
'indrAutoUtcnt' : temp_res[54],
'indrAutoArea' : temp_res[55],
'oudrAutoUtcnt' : temp_res[56],
'oudrAutoArea' : temp_res[57],
'pmsDay' : temp_res[58],
'stcnsDay' : temp_res[59],
'useAprDay' : temp_res[60],
'pmsnoYear' : temp_res[61],
'pmsnoKikCd' : temp_res[62],
'pmsnoKikCdNm' : temp_res[63],
'pmsnoGbCd' : temp_res[64],
'pmsnoGbCdNm' : temp_res[65],
'hoCnt' : temp_res[66],
'engrGrade' : temp_res[67],
'engrRat' : temp_res[68],
'engrEpi' : temp_res[69],
'gnBldGrade' : temp_res[70],
'gnBldCert' : temp_res[71],
'itgBldGrade' : temp_res[72],
'itgBldCert' : temp_res[73],
'crtnDay' : temp_res[74],
'rserthqkDsgnApplyYn' : temp_res[75],
'rserthqkAblty' : temp_res[76]
}

base_df = pd.DataFrame(base_dict)
base_df.to_csv('tempresult_buildinglegister_Seoul_2020.csv', encoding='utf-8-sig')
print('csv exported')

# 결과 데이터프레임을 db에 저장한다.
# 저장에 앞선 기본값 설정
db_connection_str = 'mysql+pymysql://root:atdt01410@127.0.0.1/energy_data'
db_connection = sqlalchemy.create_engine(db_connection_str)
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
    'naMainBun' : sqlalchemy.types.VARCHAR(5),
    'naSubBun' : sqlalchemy.types.VARCHAR(5),
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
    dataframe.to_sql(name=table_name, con=connection, if_exists='replace', index=True, dtype=data_type_matrix)
    print('Data saved to DB with table name: ' + str(table_name))

input_db(base_df, db_connection, 'Building_legister_title_seoul')     # 수정해야 하는 주석


# cursor = energy_db_another.cursor(pymysql.cursors.DictCursor)
#
# table_list = ['heat']
# for table_name in table_list:
#     query_for_PK = 'ALTER TABLE ' + table_name + ' MODIFY ' + pk_name + ' VARCHAR(33) not null Primary Key'
#     cursor.execute(query_for_PK)


# 메모용 덤프커맨드 (CMD - sql서버 bin디렉터리 내에서 실행)
# mysqldump -u[username] -p[password] [database name] > [dumpfile name (.sql extension)]
# 덤프로 복원시에는 < 로 반대방향 입력.

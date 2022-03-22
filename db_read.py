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

    # 공통부를 채우기 위한 함수(사용승인일 및 사용용도)
    # df_1에 null이 있을 경우 df_2에서 가져와서 채움. null이 없으면 기본적으로 앞의 것을 신뢰함.
    def fill_null(df_1, df_2):
        fill_null = lambda s1, s2: s2 if pd.isna(s1) is True else s1
        for index in ['USEAPR_DAY', 'MAIN_PURPS_NM']:
            df_1[index] = df_1[index].combine(df_2[index], fill_null)
        return df_1

    # 코드 가독성을 위해 gas_data를 복사한 다음 elec_data, heat_data와 각각 머징
    result = gas_data

    result = result.merge(elec_data['ELEC_converged_EUI'], how='outer', on='MGM_BLD_PK')
    result = fill_null(result, elec_data)

    result = result.merge(heat_data['HEAT_converged_EUI'], how='outer', on='MGM_BLD_PK')
    result = fill_null(result, heat_data)

    # EUI의 총합을 계산해서 합산
    # fillna로 NaN 데이터값을 0으로 치환(합만 구해서 사용하므로)
    result['GAS_converged_EUI'] = result['GAS_converged_EUI'].fillna(0)
    result['ELEC_converged_EUI'] = result['ELEC_converged_EUI'].fillna(0)
    result['HEAT_converged_EUI'] = result['HEAT_converged_EUI'].fillna(0)
    result['total_converged_EUI'] = result['GAS_converged_EUI'] + result['ELEC_converged_EUI'] + result['HEAT_converged_EUI']

    print('full data loaded')
    print(result.head())
    return result

get_fulldata()


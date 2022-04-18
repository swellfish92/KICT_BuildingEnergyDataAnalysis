# 긴급히 코드를 수정해야 하기 때문에 이 곳을 사용함.
# Issue는 기존의 gas/heat/elec DB가 합쳐지지 않은 것이 원인임.
# 여기에 202004~202109가 저장되어 있는데, 이것을 받은 txt파일과 합쳐야 한다...
# 그냥 하나로 뭉쳐져 있을 텐데 어딘가에....

# 아무튼 시간이 없으니 죄다 하드코딩으로 돌림.

import scipy as sp
import scipy.stats
import pymysql
import pandas as pd
from functions import *
import numpy as np
import sqlalchemy


energy_db = pymysql.connect(
    user = 'root',
    passwd = 'atdt01410',
    host = '127.0.0.1',
    db = 'energy_data',
    charset = 'utf8'
)

def load_sql(cursor, load_query):
    cursor.execute(load_query)
    result = cursor.fetchall()
    return pd.DataFrame(result)

# Cursor 세팅 및 Sql 쿼리 사전정의
cursor = energy_db.cursor(pymysql.cursors.DictCursor)

heat_arr = ['HEAT_202001', 'HEAT_202002', 'HEAT_202003', 'HEAT_202004', 'HEAT_202005', 'HEAT_202006', 'HEAT_202007', 'HEAT_202008', 'HEAT_202009', 'HEAT_202010', 'HEAT_202011', 'HEAT_202012']
elec_arr = ['ELEC_202001', 'ELEC_202002', 'ELEC_202003', 'ELEC_202004', 'ELEC_202005', 'ELEC_202006', 'ELEC_202007', 'ELEC_202008', 'ELEC_202009', 'ELEC_202010', 'ELEC_202011', 'ELEC_202012']
gas_arr = ['GAS_202001', 'GAS_202002', 'GAS_202003', 'GAS_202004', 'GAS_202005', 'GAS_202006', 'GAS_202007', 'GAS_202008', 'GAS_202009', 'GAS_202010', 'GAS_202011', 'GAS_202012']

def make_string_for_db_call(arr):
    temp_result = ''
    for item in arr:
        temp_result = temp_result + ', ' + item
    return temp_result

def call_2020_data():
    # # 3~12월 데이터를 로드
    # query_elec_2020 = "SELECT MGM_BLD_PK" + make_string_for_db_call(elec_arr[3:12]) + " FROM elec"
    # query_gas_2020 = "SELECT MGM_BLD_PK" + make_string_for_db_call(gas_arr[3:12]) + " FROM gas"
    # query_heat_2020 = "SELECT MGM_BLD_PK" + make_string_for_db_call(heat_arr[3:12]) + " FROM heat"
    #
    # elec_2020_data = load_sql(cursor, query_elec_2020)
    # gas_2020_data = load_sql(cursor, query_gas_2020)
    # heat_2020_data = load_sql(cursor, query_heat_2020)
    #
    # # MGM_BLD_PK를 인덱스로 설정
    # elec_2020_data.set_index('MGM_BLD_PK', drop=True, inplace=True)
    # gas_2020_data.set_index('MGM_BLD_PK', drop=True, inplace=True)
    # heat_2020_data.set_index('MGM_BLD_PK', drop=True, inplace=True)
    #
    # # 1~3월 데이터를 로드
    # query_elec = "SELECT MGM_BLD_PK" + make_string_for_db_call(elec_arr[0:3]) + " FROM elec_2020"
    # query_gas = "SELECT MGM_BLD_PK" + make_string_for_db_call(gas_arr[0:3]) + " FROM gas_2020"
    # query_heat = "SELECT MGM_BLD_PK" + make_string_for_db_call(heat_arr[0:3]) + " FROM heat_2020"
    #
    # elec_data = load_sql(cursor, query_elec)
    # gas_data = load_sql(cursor, query_gas)
    # heat_data = load_sql(cursor, query_heat)
    #
    # # MGM_BLD_PK를 인덱스로 설정
    # elec_data.set_index('MGM_BLD_PK', drop=True, inplace=True)
    # gas_data.set_index('MGM_BLD_PK', drop=True, inplace=True)
    # heat_data.set_index('MGM_BLD_PK', drop=True, inplace=True)
    #
    # final_elec_data = elec_data.join(elec_2020_data, how='outer')
    # print(final_elec_data)
    # final_gas_data = gas_data.join(gas_2020_data, how='outer')
    # print(final_gas_data)
    # final_heat_data = heat_data.join(heat_2020_data, how='outer')
    # print(final_heat_data)
    #
    #
    # final_elec_data.to_excel('final_elec_data_backup.xlsx')
    # final_gas_data.to_excel('final_gas_data_backup.xlsx')
    # final_heat_data.to_excel('final_heat_data_backup.xlsx')


    # 데이터를 저장

    final_elec_data = pd.read_excel('final_elec_data_backup.xlsx')
    final_gas_data = pd.read_excel('final_gas_data_backup.xlsx')
    final_heat_data = pd.read_excel('final_heat_data_backup.xlsx')

    # 저장에 앞선 기본값 설정
    db_connection_str = 'mysql+pymysql://root:atdt01410@127.0.0.1/energy_data'
    db_connection = sqlalchemy.create_engine(db_connection_str)
    data_type_matrix = {
        'MGM_BLD_PK': sqlalchemy.types.VARCHAR(33)
    }

    print('connected')

    def input_db(dataframe, connection, table_name):
        dataframe.to_sql(name=table_name, con=connection, if_exists='replace', index=False,
                         dtype={'MGM_BLD_PK': sqlalchemy.types.VARCHAR(33)})
        print('Data saved to DB with table name: ' + str(table_name))


    input_db(final_elec_data, db_connection, 'elec_2020')
    input_db(final_gas_data, db_connection, 'gas_2020')
    input_db(final_heat_data, db_connection, 'heat_2020')

call_2020_data()
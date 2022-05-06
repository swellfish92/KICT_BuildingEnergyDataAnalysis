# DB입력 함수화를 위한 파일

# 베이스 파일에 대한 파일명 및 상세도 여기에 기록함
# mart_djy : 건축물대장. 뒤의 숫자는 오퍼레이션 번호 (01이 기본개요, 02가 총괄표제부, 03이 일반건축물대장/표제부
# mart_kcy_01 : 건축인허가정보. 오퍼레이션 번호와 일치하는지는 확인하지 않음 (그러나 01은 기본개요임)

import pandas as pd
import sqlalchemy

def read_eais_basedata(type, filedir, name_matrix=None):
    # 세움터(open.eais.go.kr)에서 배포하는 설명 파일을 가지고 DB입력에 필요한 base_dict를 만든다.
    # type 1은 base_dict를 작성시 쓰는 list, type 2는 alchemysql에서 사용할 data_type_matrix
    data = pd.read_excel(filedir, header=1)
    print(data)
    if type == 1:
        temp_arr = []
        if name_matrix == None:
            for i in range(len(data['컬럼 한글명'])):
                temp_arr.append(data['컬럼 한글명'].values.tolist()[i])
            return temp_arr

        else:
            print(name_matrix)
            for i in range(len(data['컬럼 한글명'])):
                temp_arr.append(name_matrix[data['컬럼 한글명'].values.tolist()[i]])
            return temp_arr

    elif type == 2:
        temp_dict = {}
        if name_matrix == None:
            for i in range(len(data['컬럼 한글명'])):
                type_str = data['데이터 타입'].values.tolist()[i]
                temp_dict[data['컬럼 한글명'].values.tolist()[i]] = type_str
            return temp_dict

        else:
            for i in range(len(data['컬럼 한글명'])):
                type_str = data['데이터 타입'].values.tolist()[i]
                if 'VARCHAR' in type_str:
                    length = type_str.split('(')[1].split(')')[0]
                    temp_dict[name_matrix[data['컬럼 한글명'].values.tolist()[i]]] = sqlalchemy.types.VARCHAR(int(length))
                elif 'NUMERIC' in type_str:
                    length = type_str.split('(')[1].split(')')[0]
                    if ',' in length and length.split(',')[1] != ':':
                        len_2 = int(length.split(',')[1])
                    else:
                        len_2 = None
                    temp_dict[name_matrix[data['컬럼 한글명'].values.tolist()[i]]] = sqlalchemy.types.NUMERIC(precision=int(length.split(',')[0]), scale=len_2)
                elif 'CHAR' in type_str:
                    length = type_str.split('(')[1].split(')')[0]
                    temp_dict[name_matrix[data['컬럼 한글명'].values.tolist()[i]]] = sqlalchemy.types.CHAR(int(length))
            return temp_dict
    else:
        print('Type Value Error, insert 1|2')
        raise IOError

def make_basedict(key_arr, data_arr, type='df'):
    # 일차배열 key_arr과 이차배열 data_arr로 DB에 넣을 데이터를 만듬
    res_dict = {}
    for i in range(len(key_arr)):
        res_dict[key_arr[i]] = data_arr[i]
    if type == 'dict':
        return res_dict
    elif type == 'df':
        return pd.DataFrame(res_dict)

# k = read_eais_basedata(1, 'C:/Users/Swellfish/Downloads/건축물대장_표제부.xls')
# print(k)
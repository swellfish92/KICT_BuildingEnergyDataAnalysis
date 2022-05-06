import pandas as pd
import time

# main_data = pd.read_csv('result(EUI_sum)_v7_20220425.csv')
# main_data.set_index('MGM_BLD_PK', drop=True, inplace=True)
# area_data_title = pd.read_csv('tempresult_buildinglegister_title_Seoul.csv')
# area_data_title.set_index('mgmBldrgstPk', drop=True, inplace=True)
# area_data_recaptitle = pd.read_csv('tempresult_buildinglegister_recaptitle_Seoul.csv')
# area_data_recaptitle.set_index('mgmBldrgstPk', drop=True, inplace=True)
#
# main_data = main_data.join(area_data_title, how='left', rsuffix='_title')
# main_data = main_data.join(area_data_recaptitle, how='left', rsuffix='_recaptitle')
#
# main_data.to_csv('result(EUI_sum)_V7_area_attached.csv', encoding='utf-8-sig')


# ======================================================================================================================

# base_data = pd.read_csv('temp_pklist.csv')
# base_data.set_index('Raw_PK', drop=True, inplace=True)
#
# main_data = pd.read_csv('result(EUI_sum)_v7_20220425.csv')
# main_data.set_index('MGM_BLD_PK', drop=True, inplace=True)
#
# area_data_title = pd.read_csv('tempresult_buildinglegister_title_Seoul.csv')
# area_data_title.set_index('mgmBldrgstPk', drop=True, inplace=True)
# area_data_title = area_data_title[['platPlc', 'totArea', 'mainPurpsCdNm', 'etcPurps', 'mainAtchGbCdNm', 'regstrKindCdNm', 'bldNm']]
#
#
# area_data_recaptitle = pd.read_csv('tempresult_buildinglegister_recaptitle_Seoul.csv')
# area_data_recaptitle.set_index('mgmBldrgstPk', drop=True, inplace=True)
# area_data_recaptitle = area_data_recaptitle[['platPlc', 'totArea', 'mainPurpsCdNm', 'etcPurps', 'mainBldCnt', 'atchBldCnt', 'regstrKindCdNm', 'bldNm']]
#
#
# main_data = base_data.join(main_data, how='left', rsuffix='_energydb')
# main_data = main_data.join(area_data_title, how='left', rsuffix='_title')
# main_data = main_data.join(area_data_recaptitle, how='left', rsuffix='_recaptitle')
#
# main_data.to_csv('missing_pkcode_area_attached.csv', encoding='utf-8-sig')

# ======================================================================================================================
def add_pnu(dataframe):
    # dataframe['PNU'] = str(dataframe['sigunguCd']) + str(dataframe['bjdongCd']) + str(dataframe['platGbCd']) + str(dataframe['bun']) + str(dataframe['ji'])
    dataframe = dataframe.astype({'sigunguCd': 'str', 'bjdongCd':'str', 'platGbCd':'str', 'bun':'str', 'ji':'str'})
    dataframe['bun'] = dataframe['bun'].str.pad(width=4, side='left', fillchar='0')
    dataframe['ji'] = dataframe['ji'].str.pad(width=4, side='left', fillchar='0')
    dataframe['PNU'] = dataframe['sigunguCd'].str.cat(dataframe['bjdongCd'].str.cat(dataframe['platGbCd'].str.cat(dataframe['bun'].str.cat(dataframe['ji']))))
    return dataframe

# main_data = pd.read_csv('result(EUI_sum)_v7_20220425.csv')
# main_data.set_index('MGM_BLD_PK', drop=True, inplace=True)

'''data_title = pd.read_csv('tempresult_buildinglegister_title_Seoul.csv')
#data_title = data_title.loc[0:100]
data_title = add_pnu(data_title)
temp_dict = {}

# temp_dict의 초기값 설정
key_list = data_title.columns.tolist()
print(key_list)
arr_key_list = ['platArea_arr', 'archArea_arr', 'bcRat_arr', 'totArea_arr', 'atchBldCnt_arr', 'atchBldArea_arr', 'totDongTotArea_arr', 'mgmBldrgstPk_arr', 'platPlc_arr', 'newPlatPlc_arr', 'mainAtchGbCdNm_arr', 'mainPurpsCdNm_arr', 'etcPurps_arr', 'pmsDay_arr', 'stcnsDay_arr', 'useAprDay_arr']

for item in key_list:
    temp_dict[item] = []
for item in arr_key_list:
    temp_dict[item] = []

for i in range(len(data_title)):
    row = data_title.loc[i]
    #print(row)
    if row['PNU'] in temp_dict['PNU']:
        # PNU가 이미 존재할 경우, 인덱스 값으로 배열의 순서를 구함
        iter_num = temp_dict['PNU'].index(row['PNU'])
        # 해당순서 배열에 해당하는 것들 중 가산할 것
        # 1. 면적
        temp_dict['platArea'][iter_num] = temp_dict['platArea'][iter_num] + row['platArea']
        temp_dict['platArea_arr'][iter_num].append(row['platArea'])
        temp_dict['archArea'][iter_num] = temp_dict['archArea'][iter_num] + row['archArea']
        temp_dict['archArea_arr'][iter_num].append(row['archArea'])
        temp_dict['bcRat'][iter_num] = temp_dict['bcRat'][iter_num] + row['bcRat']
        temp_dict['bcRat_arr'][iter_num].append(row['bcRat'])
        temp_dict['totArea'][iter_num] = temp_dict['totArea'][iter_num] + row['totArea']
        temp_dict['totArea_arr'][iter_num].append(row['totArea'])
        # 2. 부속건축물 수 및 면적
        temp_dict['atchBldCnt'][iter_num] = temp_dict['atchBldCnt'][iter_num] + row['atchBldCnt']
        temp_dict['atchBldCnt_arr'][iter_num].append(row['atchBldCnt'])
        temp_dict['atchBldArea'][iter_num] = temp_dict['atchBldArea'][iter_num] + row['atchBldArea']
        temp_dict['atchBldArea_arr'][iter_num].append(row['atchBldArea'])
        temp_dict['totDongTotArea'][iter_num] = temp_dict['totDongTotArea'][iter_num] + row['totDongTotArea']
        temp_dict['totDongTotArea_arr'][iter_num].append(row['totDongTotArea'])
        # 가산하지는 않으나 배열에 추가할 것
        # 1. PK코드
        temp_dict['mgmBldrgstPk_arr'][iter_num].append(row['mgmBldrgstPk'])
        # 2. 지번주소/도로명주소
        temp_dict['platPlc_arr'][iter_num].append(row['platPlc'])
        temp_dict['newPlatPlc_arr'][iter_num].append(row['newPlatPlc'])
        # 3. 건축물구분(주/부속), 용도/부속용도
        temp_dict['mainAtchGbCdNm_arr'][iter_num].append(row['mainAtchGbCdNm'])
        temp_dict['mainPurpsCdNm_arr'][iter_num].append(row['mainPurpsCdNm'])
        temp_dict['etcPurps_arr'][iter_num].append(row['etcPurps'])
        # 4. 허가일/착공일/사용승인일
        temp_dict['pmsDay_arr'][iter_num].append(row['pmsDay'])
        temp_dict['stcnsDay_arr'][iter_num].append(row['stcnsDay'])
        temp_dict['useAprDay_arr'][iter_num].append(row['useAprDay'])

    else:
        # PNU가 없을 경우, 새로 항목을 추가함, 키 값도 없을 경우는 새로 만듬
        for key in row.keys():
            if key not in temp_dict:
                temp_dict[key] = [row[key]]
            else:
                temp_dict[key].append(row[key])
        # arr항목들은 있을 수 없으니, 직접 지정한다
        for key_arr in arr_key_list:
            if key_arr not in temp_dict:
                temp_dict[key_arr] = [row[key_arr.split('_')[0]]]
            else:
                temp_dict[key_arr].append([row[key_arr.split('_')[0]]])
print(temp_dict)
title_df = pd.DataFrame(temp_dict)
title_df.set_index('PNU', drop=True, inplace=True)
print(title_df)
title_df.to_csv('bind_result_title.csv', encoding='utf-8 sig')
'''
title_df = pd.read_csv('bind_result_title.csv')
title_df.set_index('PNU', drop=True, inplace=True)

# 총괄표제부로 한번 더
data_title = pd.read_csv('tempresult_buildinglegister_recaptitle_Seoul.csv')
#data_title = data_title.loc[0:100]
data_title = add_pnu(data_title)
temp_dict = {}

# temp_dict의 초기값 설정
key_list = data_title.columns.tolist()
print(key_list)
arr_key_list = ['platArea_arr', 'archArea_arr', 'bcRat_arr', 'totArea_arr', 'mainBldCnt_arr', 'atchBldCnt_arr', 'atchBldArea_arr', 'totPkngCnt_arr', 'mgmBldrgstPk_arr', 'platPlc_arr', 'newPlatPlc_arr', 'mainPurpsCdNm_arr', 'etcPurps_arr', 'pmsDay_arr', 'stcnsDay_arr', 'useAprDay_arr']

for item in key_list:
    temp_dict[item] = []
for item in arr_key_list:
    temp_dict[item] = []

for i in range(len(data_title)):
    row = data_title.loc[i]
    #print(row)
    if row['PNU'] in temp_dict['PNU']:
        # PNU가 이미 존재할 경우, 인덱스 값으로 배열의 순서를 구함
        iter_num = temp_dict['PNU'].index(row['PNU'])
        # 해당순서 배열에 해당하는 것들 중 가산할 것
        # 1. 면적
        temp_dict['platArea'][iter_num] = temp_dict['platArea'][iter_num] + row['platArea']
        temp_dict['platArea_arr'][iter_num].append(row['platArea'])
        temp_dict['archArea'][iter_num] = temp_dict['archArea'][iter_num] + row['archArea']
        temp_dict['archArea_arr'][iter_num].append(row['archArea'])
        temp_dict['bcRat'][iter_num] = temp_dict['bcRat'][iter_num] + row['bcRat']
        temp_dict['bcRat_arr'][iter_num].append(row['bcRat'])
        temp_dict['totArea'][iter_num] = temp_dict['totArea'][iter_num] + row['totArea']
        temp_dict['totArea_arr'][iter_num].append(row['totArea'])
        # 2. 부속건축물 수 및 면적
        temp_dict['mainBldCnt'][iter_num] = temp_dict['mainBldCnt'][iter_num] + row['mainBldCnt']   # 총괄표제부에만 있는 값 (주건축물 수)
        temp_dict['mainBldCnt_arr'][iter_num].append(row['mainBldCnt'])
        temp_dict['atchBldCnt'][iter_num] = temp_dict['atchBldCnt'][iter_num] + row['atchBldCnt']
        temp_dict['atchBldCnt_arr'][iter_num].append(row['atchBldCnt'])
        temp_dict['atchBldArea'][iter_num] = temp_dict['atchBldArea'][iter_num] + row['atchBldArea']
        temp_dict['atchBldArea_arr'][iter_num].append(row['atchBldArea'])
        # temp_dict['totDongTotArea'][iter_num] = temp_dict['totDongTotArea'][iter_num] + row['totDongTotArea'] # 일반건축물대장/표제부에만 있는 값
        # temp_dict['totDongTotArea_arr'][iter_num].append(row['totDongTotArea'])
        temp_dict['totPkngCnt'][iter_num] = temp_dict['totPkngCnt'][iter_num] + row['totPkngCnt']   # 총괄표제부에만 있는 값 (총 할당된 PK수)
        temp_dict['totPkngCnt_arr'][iter_num].append(row['totPkngCnt'])
        # 가산하지는 않으나 배열에 추가할 것
        # 1. PK코드
        temp_dict['mgmBldrgstPk_arr'][iter_num].append(row['mgmBldrgstPk'])
        # 2. 지번주소/도로명주소
        temp_dict['platPlc_arr'][iter_num].append(row['platPlc'])
        temp_dict['newPlatPlc_arr'][iter_num].append(row['newPlatPlc'])
        # 3. 건축물구분(주/부속), 용도/부속용도
        # temp_dict['mainAtchGbCdNm_arr'][iter_num].append(row['mainAtchGbCdNm'])   # 일반건축물대장/표제부에만 있는 값
        temp_dict['mainPurpsCdNm_arr'][iter_num].append(row['mainPurpsCdNm'])
        temp_dict['etcPurps_arr'][iter_num].append(row['etcPurps'])
        # 4. 허가일/착공일/사용승인일
        temp_dict['pmsDay_arr'][iter_num].append(row['pmsDay'])
        temp_dict['stcnsDay_arr'][iter_num].append(row['stcnsDay'])
        temp_dict['useAprDay_arr'][iter_num].append(row['useAprDay'])

    else:
        # PNU가 없을 경우, 새로 항목을 추가함, 키 값도 없을 경우는 새로 만듬
        for key in row.keys():
            if key not in temp_dict:
                temp_dict[key] = [row[key]]
            else:
                temp_dict[key].append(row[key])
        # arr항목들은 있을 수 없으니, 직접 지정한다
        for key_arr in arr_key_list:
            if key_arr not in temp_dict:
                temp_dict[key_arr] = [row[key_arr.split('_')[0]]]
            else:
                temp_dict[key_arr].append([row[key_arr.split('_')[0]]])
print(temp_dict)
recap_df = pd.DataFrame(temp_dict)
recap_df.set_index('PNU', drop=True, inplace=True)
print(recap_df)
recap_df.to_csv('bind_result_recaptitle.csv', encoding='utf-8 sig')

# 두 개를 다 뽑으면, outer join시킴
total_df = recap_df.join(title_df, how='outer', rsuffix='_title', lsuffix='_recap')

total_df.to_csv('bind_result_total.csv', encoding='utf-8 sig')













#
# data_title.set_index('mgmBldrgstPk', drop=True, inplace=True)
#
#
#
# area_data_recaptitle = pd.read_csv('tempresult_buildinglegister_recaptitle_Seoul.csv')
# area_data_recaptitle.set_index('mgmBldrgstPk', drop=True, inplace=True)
# area_data_recaptitle = area_data_recaptitle[['platPlc', 'totArea', 'mainPurpsCdNm', 'etcPurps', 'mainBldCnt', 'atchBldCnt', 'regstrKindCdNm', 'bldNm']]
#
#
# main_data = base_data.join(main_data, how='left', rsuffix='_energydb')
# main_data = main_data.join(area_data_title, how='left', rsuffix='_title')
# main_data = main_data.join(area_data_recaptitle, how='left', rsuffix='_recaptitle')
#
# main_data.to_csv('missing_pkcode_area_attached.csv', encoding='utf-8-sig')
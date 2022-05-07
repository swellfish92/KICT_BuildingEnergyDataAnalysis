# -*- coding: utf-8 -*-

import pandas as pd
import time

sgg_code_dict = {
    '종로구' : '11110',
    '중구' : '11140',
    '용산구' : '11170',
    '성동구' : '11200',
    '광진구' : '11215',
    '동대문구' : '11230',
    '중랑구' : '11260',
    '성북구' : '11290',
    '강북구' : '11305',
    '도봉구' : '11320',
    '노원구' : '11350',
    '은평구' : '11380',
    '서대문구' : '11410',
    '마포구' : '11440',
    '양천구' : '11470',
    '강서구' : '11500',
    '구로구' : '11530',
    '금천구' : '11545',
    '영등포구' : '11560',
    '동작구' : '11590',
    '관악구' : '11620',
    '서초구' : '11650',
    '강남구' : '11680',
    '송파구' : '11710',
    '강동구' : '11740'
}

bjd_code_dict = {
    '청운동': '10100',
    '신교동': '10200',
    '궁정동': '10300',
    '효자동': '10400',
    '창성동': '10500',
    '통의동': '10600',
    '적선동': '10700',
    '통인동': '10800',
    '누상동': '10900',
    '누하동': '11000',
    '옥인동': '11100',
    '체부동': '11200',
    '필운동': '11300',
    '내자동': '11400',
    '사직동': '11500',
    '도렴동': '11600',
    '당주동': '11700',
    '내수동': '11800',
    '세종로': '11900',
    '신문로1가': '12000',
    '신문로2가': '12100',
    '청진동': '12200',
    '서린동': '12300',
    '수송동': '12400',
    '중학동': '12500',
    '종로1가': '12600',
    '공평동': '12700',
    '관훈동': '12800',
    '견지동': '12900',
    '와룡동': '13000',
    '권농동': '13100',
    '운니동': '13200',
    '익선동': '13300',
    '경운동': '13400',
    '관철동': '13500',
    '인사동': '13600',
    '낙원동': '13700',
    '종로2가': '13800',
    '팔판동': '13900',
    '삼청동': '14000',
    '안국동': '14100',
    '소격동': '14200',
    '화동': '14300',
    '사간동': '14400',
    '송현동': '14500',
    '가회동': '14600',
    '재동': '14700',
    '계동': '14800',
    '원서동': '14900',
    '훈정동': '15000',
    '묘동': '15100',
    '봉익동': '15200',
    '돈의동': '15300',
    '장사동': '15400',
    '관수동': '15500',
    '종로3가': '15600',
    '인의동': '15700',
    '예지동': '15800',
    '원남동': '15900',
    '연지동': '16000',
    '종로4가': '16100',
    '효제동': '16200',
    '종로5가': '16300',
    '종로6가': '16400',
    '이화동': '16500',
    '연건동': '16600',
    '충신동': '16700',
    '동숭동': '16800',
    '혜화동': '16900',
    '명륜1가': '17000',
    '명륜2가': '17100',
    '명륜4가': '17200',
    '명륜3가': '17300',
    '창신동': '17400',
    '숭인동': '17500',
    '교남동': '17600',
    '평동': '17700',
    '송월동': '17800',
    '홍파동': '17900',
    '교북동': '18000',
    '행촌동': '18100',
    '구기동': '18200',
    '평창동': '18300',
    '부암동': '18400',
    '홍지동': '18500',
    '신영동': '18600',
    '무악동': '18700',
    '무교동': '10100',
    '다동': '10200',
    '태평로1가': '10300',
    '을지로1가': '10400',
    '을지로2가': '10500',
    '남대문로1가': '10600',
    '삼각동': '10700',
    '수하동': '10800',
    '장교동': '10900',
    '수표동': '11000',
    '소공동': '11100',
    '남창동': '11200',
    '북창동': '11300',
    '태평로2가': '11400',
    '남대문로2가': '11500',
    '남대문로3가': '11600',
    '남대문로4가': '11700',
    '남대문로5가': '11800',
    '봉래동1가': '11900',
    '봉래동2가': '12000',
    '회현동1가': '12100',
    '회현동2가': '12200',
    '회현동3가': '12300',
    '충무로1가': '12400',
    '충무로2가': '12500',
    '명동1가': '12600',
    '명동2가': '12700',
    '남산동1가': '12800',
    '남산동2가': '12900',
    '남산동3가': '13000',
    '저동1가': '13100',
    '충무로4가': '13200',
    '충무로5가': '13300',
    '인현동2가': '13400',
    '예관동': '13500',
    '묵정동': '13600',
    '필동1가': '13700',
    '필동2가': '13800',
    '필동3가': '13900',
    '남학동': '14000',
    '주자동': '14100',
    '예장동': '14200',
    '장충동1가': '14300',
    '장충동2가': '14400',
    '광희동1가': '14500',
    '광희동2가': '14600',
    '쌍림동': '14700',
    '을지로6가': '14800',
    '을지로7가': '14900',
    '을지로4가': '15000',
    '을지로5가': '15100',
    '주교동': '15200',
    '방산동': '15300',
    '오장동': '15400',
    '을지로3가': '15500',
    '입정동': '15600',
    '산림동': '15700',
    '충무로3가': '15800',
    '초동': '15900',
    '인현동1가': '16000',
    '저동2가': '16100',
    '신당동': '16200',
    '흥인동': '16300',
    '무학동': '16400',
    '황학동': '16500',
    '서소문동': '16600',
    '정동': '16700',
    '순화동': '16800',
    '의주로1가': '16900',
    '충정로1가': '17000',
    '중림동': '17100',
    '의주로2가': '17200',
    '만리동1가': '17300',
    '만리동2가': '17400',
    '후암동': '10100',
    '용산동2가': '10200',
    '용산동4가': '10300',
    '갈월동': '10400',
    '남영동': '10500',
    '용산동1가': '10600',
    '동자동': '10700',
    '서계동': '10800',
    '청파동1가': '10900',
    '청파동2가': '11000',
    '청파동3가': '11100',
    '원효로1가': '11200',
    '원효로2가': '11300',
    '신창동': '11400',
    '산천동': '11500',
    '청암동': '11600',
    '원효로3가': '11700',
    '원효로4가': '11800',
    '효창동': '11900',
    '도원동': '12000',
    '용문동': '12100',
    '문배동': '12200',
    '신계동': '12300',
    '한강로1가': '12400',
    '한강로2가': '12500',
    '용산동3가': '12600',
    '용산동5가': '12700',
    '한강로3가': '12800',
    '이촌동': '12900',
    '이태원동': '13000',
    '한남동': '13100',
    '동빙고동': '13200',
    '서빙고동': '13300',
    '주성동': '13400',
    '용산동6가': '13500',
    '보광동': '13600',
    '상왕십리동': '10100',
    '하왕십리동': '10200',
    '홍익동': '10300',
    '도선동': '10400',
    '마장동': '10500',
    '사근동': '10600',
    '행당동': '10700',
    '응봉동': '10800',
    '금호동1가': '10900',
    '금호동2가': '11000',
    '금호동3가': '11100',
    '금호동4가': '11200',
    '옥수동': '11300',
    '성수동1가': '11400',
    '성수동2가': '11500',
    '송정동': '11800',
    '용답동': '12200',
    '중곡동': '10100',
    '능동': '10200',
    '구의동': '10300',
    '광장동': '10400',
    '자양동': '10500',
    '화양동': '10700',
    '군자동': '10900',
    '신설동': '10100',
    '용두동': '10200',
    '제기동': '10300',
    '전농동': '10400',
    '답십리동': '10500',
    '장안동': '10600',
    '청량리동': '10700',
    '회기동': '10800',
    '휘경동': '10900',
    '이문동': '11000',
    '면목동': '10100',
    '상봉동': '10200',
    '중화동': '10300',
    '묵동': '10400',
    '망우동': '10500',
    '신내동': '10600',
    '성북동': '10100',
    '성북동1가': '10200',
    '돈암동': '10300',
    '동소문동1가': '10400',
    '동소문동2가': '10500',
    '동소문동3가': '10600',
    '동소문동4가': '10700',
    '동소문동5가': '10800',
    '동소문동6가': '10900',
    '동소문동7가': '11000',
    '삼선동1가': '11100',
    '삼선동2가': '11200',
    '삼선동3가': '11300',
    '삼선동4가': '11400',
    '삼선동5가': '11500',
    '동선동1가': '11600',
    '동선동2가': '11700',
    '동선동3가': '11800',
    '동선동4가': '11900',
    '동선동5가': '12000',
    '안암동1가': '12100',
    '안암동2가': '12200',
    '안암동3가': '12300',
    '안암동4가': '12400',
    '안암동5가': '12500',
    '보문동4가': '12600',
    '보문동5가': '12700',
    '보문동6가': '12800',
    '보문동7가': '12900',
    '보문동1가': '13000',
    '보문동2가': '13100',
    '보문동3가': '13200',
    '정릉동': '13300',
    '길음동': '13400',
    '종암동': '13500',
    '하월곡동': '13600',
    '상월곡동': '13700',
    '장위동': '13800',
    '석관동': '13900',
    '미아동': '10100',
    '번동': '10200',
    '수유동': '10300',
    '우이동': '10400',
    '쌍문동': '10500',
    '방학동': '10600',
    '창동': '10700',
    '도봉동': '10800',
    '월계동': '10200',
    '공릉동': '10300',
    '하계동': '10400',
    '상계동': '10500',
    '중계동': '10600',
    '수색동': '10100',
    '녹번동': '10200',
    '불광동': '10300',
    '갈현동': '10400',
    '구산동': '10500',
    '대조동': '10600',
    '응암동': '10700',
    '역촌동': '10800',
    '신사동': '10900',
    '증산동': '11000',
    '진관동': '11400',
    '충정로2가': '10100',
    '충정로3가': '10200',
    '합동': '10300',
    '미근동': '10400',
    '냉천동': '10500',
    '천연동': '10600',
    '옥천동': '10700',
    '영천동': '10800',
    '현저동': '10900',
    '북아현동': '11000',
    '홍제동': '11100',
    '대현동': '11200',
    '대신동': '11300',
    '신촌동': '11400',
    '봉원동': '11500',
    '창천동': '11600',
    '연희동': '11700',
    '홍은동': '11800',
    '북가좌동': '11900',
    '남가좌동': '12000',
    '아현동': '10100',
    '공덕동': '10200',
    '신공덕동': '10300',
    '도화동': '10400',
    '용강동': '10500',
    '토정동': '10600',
    '마포동': '10700',
    '대흥동': '10800',
    '염리동': '10900',
    '노고산동': '11000',
    '신수동': '11100',
    '현석동': '11200',
    '구수동': '11300',
    '창전동': '11400',
    '상수동': '11500',
    '하중동': '11600',
    '신정동': '11700',
    '당인동': '11800',
    '서교동': '12000',
    '동교동': '12100',
    '합정동': '12200',
    '망원동': '12300',
    '연남동': '12400',
    '성산동': '12500',
    '중동': '12600',
    '상암동': '12700',
    '목동': '10200',
    '신월동': '10300',
    '염창동': '10100',
    '등촌동': '10200',
    '화곡동': '10300',
    '가양동': '10400',
    '마곡동': '10500',
    '내발산동': '10600',
    '외발산동': '10700',
    '공항동': '10800',
    '방화동': '10900',
    '개화동': '11000',
    '과해동': '11100',
    '오곡동': '11200',
    '오쇠동': '11300',
    '신도림동': '10100',
    '구로동': '10200',
    '가리봉동': '10300',
    '고척동': '10600',
    '개봉동': '10700',
    '오류동': '10800',
    '궁동': '10900',
    '온수동': '11000',
    '천왕동': '11100',
    '항동': '11200',
    '가산동': '10100',
    '독산동': '10200',
    '시흥동': '10300',
    '영등포동': '10100',
    '영등포동1가': '10200',
    '영등포동2가': '10300',
    '영등포동3가': '10400',
    '영등포동4가': '10500',
    '영등포동5가': '10600',
    '영등포동6가': '10700',
    '영등포동7가': '10800',
    '영등포동8가': '10900',
    '여의도동': '11000',
    '당산동1가': '11100',
    '당산동2가': '11200',
    '당산동3가': '11300',
    '당산동4가': '11400',
    '당산동5가': '11500',
    '당산동6가': '11600',
    '당산동': '11700',
    '도림동': '11800',
    '문래동1가': '11900',
    '문래동2가': '12000',
    '문래동3가': '12100',
    '문래동4가': '12200',
    '문래동5가': '12300',
    '문래동6가': '12400',
    '양평동1가': '12500',
    '양평동2가': '12600',
    '양평동3가': '12700',
    '양평동4가': '12800',
    '양평동5가': '12900',
    '양평동6가': '13000',
    '양화동': '13100',
    '신길동': '13200',
    '대림동': '13300',
    '양평동': '13400',
    '노량진동': '10100',
    '상도동': '10200',
    '상도1동': '10300',
    '본동': '10400',
    '흑석동': '10500',
    '동작동': '10600',
    '사당동': '10700',
    '대방동': '10800',
    '신대방동': '10900',
    '봉천동': '10100',
    '신림동': '10200',
    '남현동': '10300',
    '방배동': '10100',
    '양재동': '10200',
    '우면동': '10300',
    '원지동': '10400',
    '잠원동': '10600',
    '반포동': '10700',
    '서초동': '10800',
    '내곡동': '10900',
    '염곡동': '11000',
    '신원동': '11100',
    '역삼동': '10100',
    '개포동': '10300',
    '청담동': '10400',
    '삼성동': '10500',
    '대치동': '10600',
    '논현동': '10800',
    '압구정동': '11000',
    '세곡동': '11100',
    '자곡동': '11200',
    '율현동': '11300',
    '일원동': '11400',
    '수서동': '11500',
    '도곡동': '11800',
    '잠실동': '10100',
    '신천동': '10200',
    '풍납동': '10300',
    '송파동': '10400',
    '석촌동': '10500',
    '삼전동': '10600',
    '가락동': '10700',
    '문정동': '10800',
    '장지동': '10900',
    '방이동': '11100',
    '오금동': '11200',
    '거여동': '11300',
    '마천동': '11400',
    '명일동': '10100',
    '고덕동': '10200',
    '상일동': '10300',
    '길동': '10500',
    '둔촌동': '10600',
    '암사동': '10700',
    '성내동': '10800',
    '천호동': '10900',
    '강일동': '11000'
}

plat_gb_cd_dict = {
    '일반': '0',
    '산': '1',
    '블럭': '2',
    '블록': '2'
}




def add_pnu_mod(dataframe):
    # dataframe['PNU'] = str(dataframe['sigunguCd']) + str(dataframe['bjdongCd']) + str(dataframe['platGbCd']) + str(dataframe['bun']) + str(dataframe['ji'])
    #dataframe[['SIGUNGU_NM', 'BJDONG_NM']].dropna(inplace=True)
    dataframe = dataframe[(dataframe['SIGUNGU_NM'].isna() == False) & (dataframe['BJDONG_NM'].isna() == False)]
    temp_list = []
    for item in dataframe['SIGUNGU_NM'].tolist():
        temp_list.append(sgg_code_dict[item])
    dataframe['sigunguCd'] = temp_list
    temp_list = []
    for item in dataframe['BJDONG_NM'].tolist():
        temp_list.append(bjd_code_dict[item])
    dataframe['bjdongCd'] = temp_list
    temp_list = []
    for item in dataframe['PLAT_GB_CD'].tolist():
        temp_list.append(plat_gb_cd_dict[item])
    dataframe['platGbCd'] = temp_list
    dataframe = dataframe.astype({'platGbCd': 'int', 'BUN': 'int', 'JI': 'int'})
    dataframe = dataframe.astype({'sigunguCd': 'str', 'bjdongCd':'str', 'platGbCd':'str', 'BUN':'str', 'JI':'str'})
    dataframe['BUN'] = dataframe['BUN'].str.pad(width=4, side='left', fillchar='0')
    dataframe['JI'] = dataframe['JI'].str.pad(width=4, side='left', fillchar='0')
    dataframe['PNU'] = dataframe['sigunguCd'].str.cat(dataframe['bjdongCd'].str.cat(dataframe['platGbCd'].str.cat(dataframe['BUN'].str.cat(dataframe['JI']))))
    print(dataframe['PNU'])
    return dataframe


def address_search(dataframe, address_string):
    # 데이터프레임 내부에서 주소의 목록을 뽑음
    addr_list = dataframe['platPlc'].values.tolist()
    temp_index_arr = []
    temp_dict = {}
    for i in range(len(addr_list)):
        if address_string in addr_list[i]:
            temp_index_arr.append(i)
    return dataframe.loc[temp_index_arr]






'''
df = pd.read_csv('bind_result_total.csv')
df = df[['PNU', 'mgmBldrgstPk_recap', 'platPlc_recap', 'newPlatPlc_recap', 'bldNm_recap', 'platArea_recap', 'archArea_recap', 'bcRat_recap', 'totArea_recap', 'mainPurpsCdNm_recap', 'mainBldCnt', 'atchBldCnt_recap', 'atchBldArea_recap', 'totPkngCnt', 'pmsDay_recap', 'stcnsDay_recap', 'useAprDay_recap', 'platArea_arr_recap', 'archArea_arr_recap', 'bcRat_arr_recap', 'totArea_arr_recap', 'mainBldCnt_arr', 'atchBldCnt_arr_recap', 'atchBldArea_arr_recap', 'totPkngCnt_arr', 'mgmBldrgstPk_arr_recap', 'platPlc_arr_recap', 'newPlatPlc_arr_recap', 'mainPurpsCdNm_arr_recap', 'etcPurps_arr_recap', 'pmsDay_arr_recap', 'stcnsDay_arr_recap', 'useAprDay_arr_recap', 'mgmBldrgstPk_title', 'platPlc_title', 'newPlatPlc_title', 'bldNm_title', 'dongNm', 'platArea_title', 'archArea_title', 'bcRat_title', 'totArea_title', 'mainPurpsCdNm_title', 'atchBldCnt_title', 'atchBldArea_title', 'totDongTotArea', 'pmsDay_title', 'stcnsDay_title', 'useAprDay_title', 'platArea_arr_title', 'archArea_arr_title', 'bcRat_arr_title', 'totArea_arr_title', 'atchBldCnt_arr_title', 'atchBldArea_arr_title', 'totDongTotArea_arr', 'mgmBldrgstPk_arr_title', 'platPlc_arr_title', 'newPlatPlc_arr_title', 'mainAtchGbCdNm_arr', 'mainPurpsCdNm_arr_title', 'etcPurps_arr_title', 'pmsDay_arr_title', 'stcnsDay_arr_title', 'useAprDay_arr_title']]
df = df.astype({'PNU': 'str'})
df.set_index('PNU', drop=True, inplace=True)

carbon_col_arr = ['PNU', 'MGM_BLD_PK', 'HEAT_converged_Carbon_sum_2014', 'HEAT_converged_Carbon_sum_2015', 'HEAT_converged_Carbon_sum_2016', 'HEAT_converged_Carbon_sum_2017', 'HEAT_converged_Carbon_sum_2018', 'HEAT_converged_Carbon_sum_2019', 'HEAT_converged_Carbon_sum_2020', 'ELEC_converged_Carbon_sum_2014', 'ELEC_converged_Carbon_sum_2015', 'ELEC_converged_Carbon_sum_2016', 'ELEC_converged_Carbon_sum_2017', 'ELEC_converged_Carbon_sum_2018', 'ELEC_converged_Carbon_sum_2019', 'ELEC_converged_Carbon_sum_2020', 'GAS_converged_Carbon_sum_2014', 'GAS_converged_Carbon_sum_2015', 'GAS_converged_Carbon_sum_2016', 'GAS_converged_Carbon_sum_2017', 'GAS_converged_Carbon_sum_2018', 'GAS_converged_Carbon_sum_2019', 'GAS_converged_Carbon_sum_2020']
toe_col_arr = ['PNU', 'MGM_BLD_PK', 'HEAT_converged_toe_sum_2014', 'HEAT_converged_toe_sum_2015', 'HEAT_converged_toe_sum_2016', 'HEAT_converged_toe_sum_2017', 'HEAT_converged_toe_sum_2018', 'HEAT_converged_toe_sum_2019', 'HEAT_converged_toe_sum_2020', 'ELEC_converged_toe_sum_2014', 'ELEC_converged_toe_sum_2015', 'ELEC_converged_toe_sum_2016', 'ELEC_converged_toe_sum_2017', 'ELEC_converged_toe_sum_2018', 'ELEC_converged_toe_sum_2019', 'ELEC_converged_toe_sum_2020', 'GAS_converged_toe_sum_2014', 'GAS_converged_toe_sum_2015', 'GAS_converged_toe_sum_2016', 'GAS_converged_toe_sum_2017', 'GAS_converged_toe_sum_2018', 'GAS_converged_toe_sum_2019', 'GAS_converged_toe_sum_2020']

energy_df_carbon = pd.read_csv('./KICT_BuildingEnergyDataAnalysis/result(Carbon_sum)_v7_20220425.csv')
energy_df_carbon = add_pnu_mod(energy_df_carbon)
energy_df_carbon = energy_df_carbon.astype({'PNU': 'str'})
energy_df_carbon = energy_df_carbon[carbon_col_arr]

energy_df_carbon['Carbon_sum_2020'] = energy_df_carbon['HEAT_converged_Carbon_sum_2020'].fillna(0) + energy_df_carbon['ELEC_converged_Carbon_sum_2020'].fillna(0) + energy_df_carbon['GAS_converged_Carbon_sum_2020'].fillna(0)
energy_df_carbon['Carbon_sum_2019'] = energy_df_carbon['HEAT_converged_Carbon_sum_2019'].fillna(0) + energy_df_carbon['ELEC_converged_Carbon_sum_2019'].fillna(0) + energy_df_carbon['GAS_converged_Carbon_sum_2019'].fillna(0)
energy_df_carbon['Carbon_sum_2018'] = energy_df_carbon['HEAT_converged_Carbon_sum_2018'].fillna(0) + energy_df_carbon['ELEC_converged_Carbon_sum_2018'].fillna(0) + energy_df_carbon['GAS_converged_Carbon_sum_2018'].fillna(0)
energy_df_carbon['Carbon_sum_2017'] = energy_df_carbon['HEAT_converged_Carbon_sum_2017'].fillna(0) + energy_df_carbon['ELEC_converged_Carbon_sum_2017'].fillna(0) + energy_df_carbon['GAS_converged_Carbon_sum_2017'].fillna(0)
energy_df_carbon['Carbon_sum_2016'] = energy_df_carbon['HEAT_converged_Carbon_sum_2016'].fillna(0) + energy_df_carbon['ELEC_converged_Carbon_sum_2016'].fillna(0) + energy_df_carbon['GAS_converged_Carbon_sum_2016'].fillna(0)
energy_df_carbon['Carbon_sum_2015'] = energy_df_carbon['HEAT_converged_Carbon_sum_2015'].fillna(0) + energy_df_carbon['ELEC_converged_Carbon_sum_2015'].fillna(0) + energy_df_carbon['GAS_converged_Carbon_sum_2015'].fillna(0)
energy_df_carbon['Carbon_sum_2014'] = energy_df_carbon['HEAT_converged_Carbon_sum_2014'].fillna(0) + energy_df_carbon['ELEC_converged_Carbon_sum_2014'].fillna(0) + energy_df_carbon['GAS_converged_Carbon_sum_2014'].fillna(0)

energy_df_carbon.set_index('PNU', drop=True, inplace=True)


energy_df_toe = pd.read_csv('./KICT_BuildingEnergyDataAnalysis/result(toe_sum)_v7_20220425.csv')
energy_df_toe = add_pnu_mod(energy_df_toe)
energy_df_toe = energy_df_toe.astype({'PNU': 'str'})
energy_df_toe = energy_df_toe[toe_col_arr]

energy_df_toe['toe_sum_2020'] = energy_df_toe['HEAT_converged_toe_sum_2020'].fillna(0) + energy_df_toe['ELEC_converged_toe_sum_2020'].fillna(0) + energy_df_toe['GAS_converged_toe_sum_2020'].fillna(0)
energy_df_toe['toe_sum_2019'] = energy_df_toe['HEAT_converged_toe_sum_2019'].fillna(0) + energy_df_toe['ELEC_converged_toe_sum_2019'].fillna(0) + energy_df_toe['GAS_converged_toe_sum_2019'].fillna(0)
energy_df_toe['toe_sum_2018'] = energy_df_toe['HEAT_converged_toe_sum_2018'].fillna(0) + energy_df_toe['ELEC_converged_toe_sum_2018'].fillna(0) + energy_df_toe['GAS_converged_toe_sum_2018'].fillna(0)
energy_df_toe['toe_sum_2017'] = energy_df_toe['HEAT_converged_toe_sum_2017'].fillna(0) + energy_df_toe['ELEC_converged_toe_sum_2017'].fillna(0) + energy_df_toe['GAS_converged_toe_sum_2017'].fillna(0)
energy_df_toe['toe_sum_2016'] = energy_df_toe['HEAT_converged_toe_sum_2016'].fillna(0) + energy_df_toe['ELEC_converged_toe_sum_2016'].fillna(0) + energy_df_toe['GAS_converged_toe_sum_2016'].fillna(0)
energy_df_toe['toe_sum_2015'] = energy_df_toe['HEAT_converged_toe_sum_2015'].fillna(0) + energy_df_toe['ELEC_converged_toe_sum_2015'].fillna(0) + energy_df_toe['GAS_converged_toe_sum_2015'].fillna(0)
energy_df_toe['toe_sum_2014'] = energy_df_toe['HEAT_converged_toe_sum_2014'].fillna(0) + energy_df_toe['ELEC_converged_toe_sum_2014'].fillna(0) + energy_df_toe['GAS_converged_toe_sum_2014'].fillna(0)

energy_df_toe.set_index('PNU', drop=True, inplace=True)

result = df.join(energy_df_carbon, how='left', lsuffix='_legister', rsuffix='_carbon')
result = result.join(energy_df_toe, how='left', rsuffix='_toe')

result.to_csv('final_result_20220506.csv', encoding='utf-8 sig')

print('finished')'''



'''org_data = pd.read_csv('final_result_20220506.csv')

# 일반건축물 주거 제외
data = org_data[(org_data['mainPurpsCdNm_title'] != '단독주택') & (org_data['mainPurpsCdNm_title'] != '공동주택')]
# 총괄표제부 있는 것 제외
title_data = data[(data['mgmBldrgstPk_recap'].isna() == True)]
div_data = title_data['totArea_arr_title']
final_arr = []
for item in div_data:
    sliced_item = item.split('[')[1].split(']')[0].split(',')
    temp_arr = []
    for element in sliced_item:
        temp_arr.append(float(element))
    final_arr.append(sum(temp_arr))

title_data['sum_totarea'] = final_arr
print(title_data['sum_totarea'])
title_data = title_data[(title_data['sum_totarea'] <= 100)]
print('총괄표제부 없는 일반건축물 수 / 연면적3000이상 : ' + str(len(title_data['sum_totarea'])))
print('총괄표제부 없는 일반건축물 연면적합 / 연면적3000이상 : ' + str(sum(title_data['sum_totarea'])))

# 총괄표제부 있는 것 뽑기

data = org_data[(org_data['mainPurpsCdNm_recap'] != '단독주택') & (org_data['mainPurpsCdNm_recap'] != '공동주택')]

recap_data = data[(data['mgmBldrgstPk_recap'].isna() == False)]
div_data = recap_data['totArea_arr_recap']
#print(div_data)
final_arr = []
for item in div_data:
    sliced_item = item.split('[')[1].split(']')[0].split(',')
    temp_arr = []
    for element in sliced_item:
        temp_arr.append(float(element))
    final_arr.append(sum(temp_arr))

recap_data['sum_totarea'] = final_arr
recap_data = recap_data[(recap_data['sum_totarea'] <= 100)]
print('총괄표제부 수 / 연면적3000이상 : ' + str(sum(recap_data['mainBldCnt']) + sum(recap_data['atchBldCnt_recap'])) )
print('총괄표제부 연면적합 / 연면적3000이상 : ' + str(sum(recap_data['sum_totarea'])))



time.sleep(10000)'''

# df = pd.read_csv('./addrsearch_result_20220506.csv')
# df['mgmBldrgstPk'] = df['mgmBldrgstPk'].dropna()
# df.set_index('mgmBldrgstPk', drop=True, inplace=True)
#
# energy_df = pd.read_csv('./KICT_BuildingEnergyDataAnalysis/result(Carbon_sum)_v7_20220425.csv')
# energy_df.set_index('MGM_BLD_PK', drop=True, inplace=True)
# result = df.join(energy_df, how='left')
# result.to_csv('energy_binded_result.csv', encoding='utf-8 sig')
# print('finished')
# time.sleep(1000)

'''
legister_title_data = pd.read_csv('C:/Users/user/PycharmProjects/KICT_BuildingEnergyDataAnalysis/Data_join/tempresult_buildinglegister_title_Seoul.csv')
legister_recaptitle_data = pd.read_csv('C:/Users/user/PycharmProjects/KICT_BuildingEnergyDataAnalysis/Data_join/tempresult_buildinglegister_recaptitle_Seoul.csv')
arch_approval_data = pd.read_csv('C:/Users/user/PycharmProjects/KICT_BuildingEnergyDataAnalysis/Data_join/tempresult_archapproval_basicinfo_Seoul.csv')

address_list = ['서울특별시 중구 태평로1가 60-6', '서울특별시 중구 신당동 193-29', '중구 을지로5가 40-3', '서울특별시 중구 만리동2가 6-1', '서울특별시 용산구 후암동 30-84', '서울특별시 용산구 한남동 108', '서울특별시 성동구 송정동 73-377', '서울특별시 광진구 구의동 164-2', '서울특별시 동대문구 장안동 329-1', '서울특별시 중랑구 신내동 316', '서울특별시 중랑구 면목동 378-5', '서울특별시 중랑구 면목동 168-2', '서울특별시 성북구 장위동 65-154', '서울특별시 노원구 상계동 772', '서울특별시 은평구 구산동 172-2', '서울특별시 은평구 녹번동 산1-1', '서울특별시 은평구 응암동 40', '서울특별시 은평구 응암동 42-5', '서울특별시 은평구 역촌동 산31-1', '서울특별시 은평구 녹번동 156-17', '서울특별시 마포구 성산동 670', '서울특별시 마포구 성산동 515', '서울특별시 강서구 개화동 388-1', '서울특별시 금천구 가산동 345-58', '서울특별시 영등포구 양화동 1-29', '서울특별시 서초구 우면동 15', '강남구 도곡동 459-4', '강남구 삼성동 171-3 ', '강동구 암사동 산 1-1', '광진구 구의동 253-23 ', '구로구 구로동 98-5', '노원구 중계동 산 42-3 ', '노원구 하계동 21 ', '노원구 하계동 224-9 ', '동대문구 신설동 109-20', '동대문구 장안동 300-1 ', '동작구 흑석동 95-7', '마포구 아현동 711-2', '서대문구 홍제동 산 1-189', '신반포로 지하 200 ', '서초구 서초동 393-1', '성동구 성수동1가 685-6', '성동구 용답동 246', '성동구 용답동 246-5', '성동구 자동차시장길 41', '성동구 용답동 250', '성동구 행당동 142-1', '성동구 행당동 192-8', '송파구 방이동 88-3 ', '송파구 신천동 15', '송파구 잠실동 10-2', '송파구 잠실동 10-2', '양천구 목동 919-6', '양천구 신정동 319-15', '용산구 이촌동 302-6', '용산구 한남동 산 10-212', '은평구 녹번동 48-5', '은평구 응암동 산 6-46 ', '은평구 진관동 54', '은평구 진관동 54', '은평구 진관동 54', '은평구 진관동 54', '종로구 종로6가 287-1 ', '종로구 창신동 197-17', '중구 방산동 4-10 ', '중구 소공동 87-3 ', '중구 예장동 6-7', '중구 예장동 8-20', '중구 예장동 산 4-5', '중구 예장동 산 4-5', '중구 예장동 산 5-85 ', '중구 태평로1가 60-1 ', '중랑구 상봉동 136-18 ', '중랑구 신내동  644-2', '관악구 신림동 544', '은평구 구산동  172-2', '중구 무학동  43', '동작구 신대방동 470-11', '성동구 성수동1가  642-1', '강북구 번동 377', '서울특별시 동대문구 전농동 694', '서울특별시 양천구 신정동 781-9', '서울특별시 강북구 월계로 173', '서울특별시 강북구 월계로 173', '서울특별시 동대문구 전농동 694', '서울특별시 동대문구 전농동 694', '서울특별시 동대문구 전농동 694', '서울특별시 동대문구 전농동 694', '서울특별시 동대문구 전농동 694', '서울특별시 동대문구 전농동 694', '강서구 화곡동 809-1', '서울특별시 동대문구 전농동 694', '서울특별시 동대문구 전농동 694', '은평구 녹번동 7', '은평구 녹번동 7', '은평구 녹번동 7', '서울특별시 구로구 천왕동 14-120', '서울특별시 동대문구 전농동 694', '강남구 대치동 514', '서울특별시 동대문구 전농동 694', '서울특별시 동대문구 전농동 694', '서울특별시 동대문구 전농동 694', '서울특별시 동대문구 전농동 694', '은평구 녹번동 115', '은평구 녹번동 7', '은평구 녹번동 7', '마포구 상암동 438', '성동구 성수동1가 642-25', '서울특별시 동대문구 전농동 694', '서울특별시 동대문구 전농동 694', '서울특별시 동대문구 전농동 694', '서울특별시 동대문구 전농동 694', '서울특별시 동대문구 전농동 694', '서울특별시 동대문구 전농동 694', '서울특별시 동대문구 전농동 694', '서울특별시 동대문구 전농동 694']

final_result = pd.DataFrame({'mgmBldrgstPk':[''], 'platPlc':[''], 'newPlatPlc':[''], 'totArea':[''], 'mainPurpsCdNm':[''], 'etcPurps':['']})

for address in address_list:
    legister_title_res = address_search(legister_title_data, address)
    legister_recaptitle_res = address_search(legister_recaptitle_data, address)
    arch_approval_res = address_search(arch_approval_data, address)
    legister_title_res['type'] = '일반건축물대장/표제부'
    legister_recaptitle_res['type'] = '총괄표제부'
    arch_approval_res['type'] = '건축인허가대장'

    legister_title_res = legister_title_res[['type', 'mgmBldrgstPk', 'platPlc', 'newPlatPlc', 'totArea', 'mainPurpsCdNm', 'etcPurps']]
    legister_recaptitle_res = legister_recaptitle_res[['type', 'mgmBldrgstPk', 'platPlc', 'newPlatPlc', 'totArea', 'mainPurpsCdNm', 'etcPurps']]
    arch_approval_res = arch_approval_res[['type', 'mgmPmsrgstPk', 'platPlc', 'bldNm', 'totArea', 'mainPurpsCdNm', 'archGbCdNm']]

    temp_res = pd.concat([legister_title_res, legister_recaptitle_res, arch_approval_res], axis=0)
    #final_result = final_result.concat(arch_approval_res, axis=1)
    final_result = pd.concat([final_result, temp_res], axis=0)

final_result.to_csv('addrsearch_result_20220506.csv', encoding='utf-8 sig')

print(legister_title_res)
print(legister_recaptitle_res)
print(arch_approval_res)


time.sleep(1000)
'''












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
    dataframe['bjdongCd'] = dataframe['bjdongCd'].str.pad(width=6, side='right', fillchar='-')
    dataframe['platGbCd'] = dataframe['platGbCd'].str.pad(width=2, side='right', fillchar='-')
    dataframe['bun'] = dataframe['bun'].str.pad(width=4, side='left', fillchar='0')
    dataframe['ji'] = dataframe['ji'].str.pad(width=4, side='left', fillchar='0')
    dataframe['PNU'] = dataframe['sigunguCd'].str.cat(dataframe['bjdongCd'].str.cat(dataframe['platGbCd'].str.cat(dataframe['bun'].str.cat(dataframe['ji']))))
    return dataframe

# 에너지데이터를 붙이는 과정
# 이 부분은 나중에 함수화가 필수일 듯?


data_title = pd.read_csv('C:/Users/user/PycharmProjects/tempresult_buildinglegister_title_Seoul_2020.csv')
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
title_df = title_df.astype({'PNU': 'str'})
title_df.set_index('PNU', drop=True, inplace=True)
print(title_df)
title_df.to_csv('bind_result_title_2020.csv', encoding='utf-8 sig')





dataframe = pd.read_csv('./2020_title_legister.csv')
dataframe = add_pnu(dataframe)
key_list = dataframe.columns.tolist()
print(key_list)
key_list.append('count')
key_list.append('atch_count')
key_list.append('etc_count')

temp_dict = {}
for item in key_list:
    temp_dict[item] = []

print(len(dataframe))
for i in range(len(dataframe)):
    row = dataframe.loc[i]
    if row['PNU'] in temp_dict['PNU']:
        # PNU가 이미 존재할 경우, 인덱스 값으로 배열의 순서를 구함
        iter_num = temp_dict['PNU'].index(row['PNU'])
        # 해당순서 배열에 해당하는 것들 중 가산할 것
        temp_dict['totArea'][iter_num] = temp_dict['totArea'][iter_num] + row['totArea']

        if row['mainAtchGbCdNm'] == '주건축물':
            temp_dict['count'][iter_num] = temp_dict['count'][iter_num] + 1
        elif row['mainAtchGbCdNm'] == '부속건축물':
            temp_dict['atch_count'][iter_num] = temp_dict['atch_count'][iter_num] + 1
        else:
            temp_dict['etc_count'][iter_num] = temp_dict['etc_count'][iter_num] + 1

    else:
        # PNU가 없을 경우, 새로 항목을 추가함, 키 값도 없을 경우는 새로 만듬
        for key in row.keys():
            if key not in temp_dict:
                temp_dict[key] = [row[key]]
            else:
                temp_dict[key].append(row[key])

        if 'count' not in temp_dict:
            temp_dict['count'] = [0]
        else:
            temp_dict['count'].append(0)
        if 'atch_count' not in temp_dict:
            temp_dict['atch_count'] = [0]
        else:
            temp_dict['atch_count'].append(0)
        if 'etc_count' not in temp_dict:
            temp_dict['etc_count'] = [0]
        else:
            temp_dict['etc_count'].append(0)

        #print(temp_dict['count'])
        if row['mainAtchGbCdNm'] == '주건축물':
            temp_dict['count'].pop(-1)
            temp_dict['count'].append(1)
        elif row['mainAtchGbCdNm'] == '부속건축물':
            temp_dict['atch_count'].pop(-1)
            temp_dict['atch_count'].append(1)
        else:
            temp_dict['etc_count'].pop(-1)
            temp_dict['etc_count'].append(1)

            # print(temp_dict['count'])
            # print(temp_dict['atch_count'])
            # print(temp_dict['etc_count'])
            # else:
            #     if row['mainAtchGbCdNm'] == '부속건축물':
            #         temp_dict['atch_count'].append(1)
            #     else:
            #         temp_dict['atch_count'].append(0)
            #
            # if 'etc_count' not in temp_dict:
            #     temp_dict['etc_count'] = []
            # else:
            #     if row['mainAtchGbCdNm'] != '주건축물' and row['mainAtchGbCdNm'] != '부속건축물':
            #         temp_dict['etc_count'].append(1)
            #     else:
            #         temp_dict['etc_count'].append(0)

print(len(temp_dict['PNU']))
print(len(temp_dict['count']))
print(len(temp_dict['atch_count']))
print(len(temp_dict['etc_count']))
# print(temp_dict)
title_df = pd.DataFrame(temp_dict)
title_df = title_df.astype({'PNU': 'str'})
title_df.set_index('PNU', drop=True, inplace=True)
print(title_df)
title_df.to_csv('최종_result_title_2020_count.csv', encoding='utf-8 sig')

print('끝끝끝')
raise IOError




# main_data = pd.read_csv('result(EUI_sum)_v7_20220425.csv')
# main_data.set_index('MGM_BLD_PK', drop=True, inplace=True)

data_title = pd.read_csv('C:/Users/user/PycharmProjects/tempresult_buildinglegister_title_Seoul_2020.csv')
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
title_df = title_df.astype({'PNU': 'str'})
title_df.set_index('PNU', drop=True, inplace=True)
print(title_df)
title_df.to_csv('bind_result_title_2020.csv', encoding='utf-8 sig')

# title_df = pd.read_csv('C:/Users/user/Downloads/bind_result_title_2020.csv')
# title_df = title_df.astype({'PNU': 'str'})
# title_df.set_index('PNU', drop=True, inplace=True)

# 총괄표제부로 한번 더
data_title = pd.read_csv('C:/Users/user/PycharmProjects/tempresult_buildinglegister_recaptitle_Seoul_2020.csv')
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
recap_df = recap_df.astype({'PNU': 'str'})
recap_df.set_index('PNU', drop=True, inplace=True)
print(recap_df)

#recap_df.to_csv('bind_result_recaptitle.csv', encoding='utf-8 sig')

print(title_df.index)
print(recap_df.index)

# 두 개를 다 뽑으면, outer join시킴
total_df = recap_df.join(title_df, how='outer', rsuffix='_title', lsuffix='_recap') #, on='PNU')
print(total_df)
total_df.to_csv('bind_result_total_2020.csv', encoding='utf-8 sig')













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

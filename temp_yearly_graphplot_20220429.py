import numpy as np

from db_read import *

# 한글 폰트 사용을 위해서 세팅
from matplotlib import font_manager, rc
font_path = "C:/Windows/Fonts/malgunbd.TTF"
font = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font)
import time

def get_range_label(arr):
    temp_result = []
    for i in range(len(arr)):
        if i == len(arr)-1:
            joined_string = str('{:0,.0f}'.format(arr[i])) + '~'
        else:
            joined_string = str('{:0,.0f}'.format(arr[i])) + '~' + str('{:0,.0f}'.format(arr[i+1]))
        temp_result.append(joined_string)
    return temp_result

def div_by_age(data, return_type='dataframe' ,age_label = 'BLDG_AGE'):
    # 건축물 연령별로 구간을 나눈다. 혹여 2022년이 아닌 순간에 이것을 사용하게 될 경우에는 숫자를 보정해야 한다.....
    year_range = [0, 12, 22, 32, 42, 52, 62, 72]
    label_set = ['2010~', '2000~2009', '1990~1999', '1980~1989', '1970~1979', '1960~1969', '1950~1959', '~1950']
    temp_result = []
    # 기본적으로 쪼개진 데이터프레임을 배열에 넣어서 돌려줌. 통합관리를 위해 연도 레이블목록도 여기서 돌려준다.
    if return_type == 'dataframe':
        for idx in range(len(year_range)):
            if idx == len(year_range)-1:
                temp_data = data[(data[age_label] >= year_range[idx])]
            else:
                temp_data = data[(data[age_label] < year_range[idx+1]) & (data[age_label] >= year_range[idx])]
            temp_result.append(temp_data)
    # 히스토그램을 위해 숫자만 필요한 경우에는 여기서 돌려준다.
    elif return_type == 'count':
        for idx in range(len(year_range)):
            if idx == len(year_range)-1:
                temp_data = data[(data[age_label] >= year_range[idx])]
            else:
                temp_data = data[(data[age_label] < year_range[idx+1]) & (data[age_label] >= year_range[idx])]
            temp_result.append(len(temp_data))

    return temp_result, label_set

# def div_by_area_special(data, range, return_type='dataframe' ,age_label = 'TOTAREA'):
#     # 건축물 면적별로 구간을 나눈다. 충돌하는 요구사항 (3000으로 거르고 다시 면적별로....)에 대응하기 위한 하드코딩
#     range = [3000, 5000, 10000, 30000, 50000, 100000]
#     label_set = ['3000~5000', '5000~10000', '10000~30000', '30000~50000', '50000~100000', '100000~']
#     temp_result = []
#     # 기본적으로 쪼개진 데이터프레임을 배열에 넣어서 돌려줌. 통합관리를 위해 연도 레이블목록도 여기서 돌려준다.
#     if return_type == 'dataframe':
#         for idx in range(len(range)):
#             if idx == len(range)-1:
#                 temp_data = data[(data[age_label] >= range[idx])]
#             else:
#                 temp_data = data[(data[age_label] < range[idx+1]) & (data[age_label] >= range[idx])]
#             temp_result.append(temp_data)
#     # 히스토그램을 위해 숫자만 필요한 경우에는 여기서 돌려준다.
#     elif return_type == 'count':
#         for idx in range(len(range)):
#             if idx == len(range)-1:
#                 temp_data = data[(data[age_label] >= range[idx])]
#             else:
#                 temp_data = data[(data[age_label] < range[idx+1]) & (data[age_label] >= range[idx])]
#             temp_result.append(len(temp_data))
#
#     return temp_result, label_set

def div_by_area(data, data_range, return_type='dataframe' ,area_label = 'TOTAREA'):
    # 건축물 면적별로 구간을 나눈다.
    label_set = get_range_label(data_range)
    temp_result = []
    # 기본적으로 쪼개진 데이터프레임을 배열에 넣어서 돌려줌. 통합관리를 위해 연도 레이블목록도 여기서 돌려준다.
    if return_type == 'dataframe':
        for idx in range(len(data_range)):
            if idx == len(data_range)-1:
                temp_data = data[(data[area_label] >= data_range[idx])]
            else:
                temp_data = data[(data[area_label] < data_range[idx+1]) & (data[area_label] >= data_range[idx])]
            temp_result.append(temp_data)
    # 히스토그램을 위해 숫자만 필요한 경우에는 여기서 돌려준다.
    elif return_type == 'count':
        print(data[area_label])
        for idx in range(len(data_range)):
            if idx == len(data_range)-1:
                temp_data = data[(data[area_label] >= data_range[idx])]
            else:
                temp_data = data[(data[area_label] < data_range[idx+1]) & (data[area_label] >= data_range[idx])]
            temp_result.append(len(temp_data))

    return temp_result, label_set

def div_by_energy(data, data_range, return_type='dataframe' ,energy_label = 'TOTAREA'):
    # 건축물 면적별로 구간을 나눈다.
    label_set = get_range_label(data_range)
    temp_result = []
    # 기본적으로 쪼개진 데이터프레임을 배열에 넣어서 돌려줌. 통합관리를 위해 연도 레이블목록도 여기서 돌려준다.
    if return_type == 'dataframe':
        for idx in range(len(data_range)):
            if idx == len(data_range)-1:
                temp_data = data[(data[energy_label] >= data_range[idx])]
            else:
                temp_data = data[(data[energy_label] < data_range[idx+1]) & (data[energy_label] >= data_range[idx])]
            temp_result.append(temp_data)
    # 히스토그램을 위해 숫자만 필요한 경우에는 여기서 돌려준다.
    elif return_type == 'count':
        for idx in range(len(data_range)):
            if idx == len(data_range)-1:
                temp_data = data[(data[energy_label] >= data_range[idx])]
            else:
                temp_data = data[(data[energy_label] < data_range[idx+1]) & (data[energy_label] >= data_range[idx])]
            temp_result.append(len(temp_data))

    return temp_result, label_set

def input_bar_number(bar):
    for item in bar:
        height = item.get_height()
        text = '{:0,.0f}'.format(height)
        plt.text(item.get_x() + item.get_width()/2.0, height, text, ha='center', va='bottom')

def draw_histogram_age(data):
    # 건축물의 연령이니 극단값을 쳐낼 필요 자체가 없음
    # x_range는 대체할 구간을 통째로 집어넣어 준다.
    divided_res, div_label = div_by_age(data, 'count', 'BLDG_AGE')
    bar = plt.bar(range(len(divided_res)), divided_res)
    plt.xticks(range(len(divided_res)), div_label)
    input_bar_number(bar)

def draw_energy_by_area(data, energy_range, label):
    # x축이 늘어지는걸 막기 위해 면적의 극단값을 쳐낸다.
    #data = drop_extreme(data, label)
    # 데이터프레임을 결과로 받아온다 (분할된 것의 합을 구해야 하므로)
    divided_res, div_label = div_by_area(data, energy_range, 'dataframe', 'TOTAREA')
    # divided_res(데이터프레임 배열)을 기반으로 구간당 합을 계산
    # 하단의 plt.bar과 plt.xticks에서 dataframe배열을 집어넣으면 hash 오류가 생김 (iterable 문제인 듯...?)
    # 매번 데이터프레임에서 원하는 값을 뽑아줄 필요가 있음.
    energy_sum_arr = []
    for i in range(len(divided_res)):
        energy_sum_arr.append(divided_res[i][label].sum())
    print(energy_sum_arr)
    bar = plt.bar(range(len(energy_sum_arr)), energy_sum_arr)
    plt.xticks(range(len(energy_sum_arr)), div_label)
    input_bar_number(bar)

def draw_energy_per_bldg_by_area(data, energy_range, label):
    # x축이 늘어지는걸 막기 위해 면적의 극단값을 쳐낸다.
    # data = drop_extreme(data, label)
    # 데이터프레임을 결과로 받아온다 (분할된 것의 합을 구해야 하므로)
    divided_res, div_label = div_by_area(data, energy_range, 'dataframe', 'TOTAREA')
    # divided_res(데이터프레임 배열)을 기반으로 구간당 합을 계산
    # 하단의 plt.bar과 plt.xticks에서 dataframe배열을 집어넣으면 hash 오류가 생김 (iterable 문제인 듯...?)
    # 매번 데이터프레임에서 원하는 값을 뽑아줄 필요가 있음.
    energy_sum_arr = []
    for i in range(len(divided_res)):
        energy_sum_arr.append(divided_res[i][label].mean())
    print(energy_sum_arr)
    bar = plt.bar(range(len(energy_sum_arr)), energy_sum_arr)
    plt.xticks(range(len(energy_sum_arr)), div_label)
    input_bar_number(bar)

def draw_histogram_area(data, data_range, label='TOTAREA', spctype = 0):
    # 건축물의 면적이므로 극단값을 쳐낸다
    # data = drop_extreme(data, label)
    # x_range는 대체할 구간을 통째로 집어넣어 준다.
    #if spctype == 0:
    divided_res, div_label = div_by_area(data, data_range, 'count', label)
    print(divided_res)
    bar = plt.bar(range(len(divided_res)), divided_res)
    plt.xticks(range(len(divided_res)), div_label)
    input_bar_number(bar)
    # elif spctype == 1:
    #     divided_res, div_label = div_by_area_special(data, 'count', label)
    #     plt.bar(range(len(divided_res)), divided_res)
    #     plt.xticks(range(len(divided_res)), div_label)

def draw_energy_by_energy(data, energy_range, label):
    # x축이 늘어지는걸 막기 위해 면적의 극단값을 쳐낸다.
    #data = drop_extreme(data, label)
    # 데이터프레임을 결과로 받아온다 (분할된 것의 합을 구해야 하므로)
    divided_res, div_label = div_by_area(data, energy_range, 'dataframe', 'total_converged_toe_sum_2020')
    # divided_res(데이터프레임 배열)을 기반으로 구간당 합을 계산
    # 하단의 plt.bar과 plt.xticks에서 dataframe배열을 집어넣으면 hash 오류가 생김 (iterable 문제인 듯...?)
    # 매번 데이터프레임에서 원하는 값을 뽑아줄 필요가 있음.
    energy_sum_arr = []
    print(divided_res)
    print(div_label)
    for i in range(len(divided_res)):
        energy_sum_arr.append(divided_res[i][label].sum())
    print(energy_sum_arr)
    bar = plt.bar(range(len(energy_sum_arr)), energy_sum_arr)
    plt.xticks(range(len(energy_sum_arr)), div_label)
    input_bar_number(bar)

def draw_graph_set():
    # # 데이터 가져오는 부분
    # data = pd.read_excel('result(toe_sum)_v5_20220423.xlsx')
    # data['total_converged_toe_sum_2020'] = data['HEAT_converged_toe_sum_2020'] + data['ELEC_converged_toe_sum_2020'] + data['GAS_converged_toe_sum_2020']
    # age_data = pd.read_excel('Building_age_data.xlsx')
    #
    # data.set_index('MGM_BLD_PK', drop=True, inplace=True)
    # age_data.set_index('MGM_BLD_PK', drop=True, inplace=True)
    # joined_data = data.join(age_data, how='left')
    #
    # # 빠른 테스트를 위해 임시로 순한맛 사용
    # # joined_data = pd.read_excel('toe_sum_age_linked.xlsx')
    # # joined_data.set_index('MGM_BLD_PK', drop=True, inplace=True)
    # joined_data['total_converged_toe_sum_2020'] = joined_data['HEAT_converged_toe_sum_2020'].fillna(0) + joined_data['ELEC_converged_toe_sum_2020'].fillna(0) + joined_data['GAS_converged_toe_sum_2020'].fillna(0)
    # joined_data.to_excel('toe_sum_age_linked_v3.xlsx')

    # 에너지데이터 DB 로드
    data = pd.read_csv('toe_sum_v6.csv')
    data.set_index('MGM_BLD_PK', drop=True, inplace=True)
    #data.drop(['TOTAREA', 'USEAPR_DAY'], axis='columns', inplace=True)

    # 건축물 나이데이터를 로드해서 합침
    age_data = pd.read_csv('Building_agedata.csv')
    age_data.set_index('MGM_BLD_PK', drop=True, inplace=True)
    data = data.join(age_data, how='left')
    # 건축물 면적데이터를 로드해서 합침
    area_data = pd.read_csv('Building_areadata.csv')
    area_data.set_index('MGM_BLD_PK', drop=True, inplace=True)
    data = data.join(area_data, how='left')

    # 연도별 합 구하기
    data['total_converged_toe_sum_2014'] = data['HEAT_converged_toe_sum_2014'].fillna(0) + data['ELEC_converged_toe_sum_2014'].fillna(0) + data['GAS_converged_toe_sum_2014'].fillna(0)
    data['total_converged_toe_sum_2015'] = data['HEAT_converged_toe_sum_2015'].fillna(0) + data['ELEC_converged_toe_sum_2015'].fillna(0) + data['GAS_converged_toe_sum_2015'].fillna(0)
    data['total_converged_toe_sum_2016'] = data['HEAT_converged_toe_sum_2016'].fillna(0) + data['ELEC_converged_toe_sum_2016'].fillna(0) + data['GAS_converged_toe_sum_2016'].fillna(0)
    data['total_converged_toe_sum_2017'] = data['HEAT_converged_toe_sum_2017'].fillna(0) + data['ELEC_converged_toe_sum_2017'].fillna(0) + data['GAS_converged_toe_sum_2017'].fillna(0)
    data['total_converged_toe_sum_2018'] = data['HEAT_converged_toe_sum_2018'].fillna(0) + data['ELEC_converged_toe_sum_2018'].fillna(0) + data['GAS_converged_toe_sum_2018'].fillna(0)
    data['total_converged_toe_sum_2019'] = data['HEAT_converged_toe_sum_2019'].fillna(0) + data['ELEC_converged_toe_sum_2019'].fillna(0) + data['GAS_converged_toe_sum_2019'].fillna(0)
    data['total_converged_toe_sum_2020'] = data['HEAT_converged_toe_sum_2020'].fillna(0) + data['ELEC_converged_toe_sum_2020'].fillna(0) + data['GAS_converged_toe_sum_2020'].fillna(0)

    # 용도별로 데이터를 분리
    residential_data = data[(data['MAIN_PURPS_NM'] == '단독주택') | (data['MAIN_PURPS_NM'] == '공동주택')]
    another_data = data[(data['MAIN_PURPS_NM'] != '단독주택') & (data['MAIN_PURPS_NM'] != '공동주택')]

    residential_data.drop(['11710-534'], axis=0, inplace=True)
    print(residential_data)
    print(another_data)
    print(sum(residential_data['TOTAREA'].fillna(0)))
    print(sum(another_data['TOTAREA'].fillna(0)))


    '''    # 연도별 데이터로 데이터프레임을 작성
    year_arr = [2014, 2015, 2016, 2017, 2018, 2019, 2020]
    basedata_for_dfarr = []
    for year in year_arr:
        temp_arr = []
        temp_arr.append(str(year))
        age = 2022-year
        filtered_residential_data = residential_data[(residential_data['BLDG_AGE'] > age)]
        filtered_another_data = another_data[(another_data['BLDG_AGE'] > age)]
        temp_arr.append(sum(filtered_residential_data['total_converged_toe_sum_' + str(year)]))
        temp_arr.append(sum(filtered_another_data['total_converged_toe_sum_' + str(year)]))
        basedata_for_dfarr.append(temp_arr)
    # 작성된 데이터프레임으로 그래프 출력
    print(basedata_for_dfarr)
    df = pd.DataFrame(basedata_for_dfarr, columns=["year", "주거용", "비주거용"])
    bar = df.plot(x="year", y=["주거용", "비주거용"], kind="bar", rot=0)
    # 막대 위에 값 넣기
    for p in bar.patches:
        left, bottom, width, height = p.get_bbox().bounds
        bar.annotate("%.1f" % (height / 1000000), (left + width / 2, height * 1.01), ha='center')
    plt.title('연도별 건축물 에너지사용량 변동 (TOE)')
    plt.xlabel('연도 (년)')
    plt.ylabel('에너지사용량 총합(TOE)')
    plt.legend()
    plt.show()
    #plt.savefig('./annual_graph/연도별 건축물 에너지사용량 변동.png')
    plt.clf()
    df.set_index('year', drop=True, inplace=True)
    df.to_excel('./annual_graph/연도별 건축물 에너지사용량 변동.xlsx')

    # 연도별 면적합 구하기
    year_arr = [2014, 2015, 2016, 2017, 2018, 2019, 2020]
    basedata_for_dfarr = []
    for year in year_arr:
        temp_arr = []
        temp_arr.append(str(year))
        age = 2022-year
        filtered_residential_data = residential_data[(residential_data['BLDG_AGE'] > age)].fillna(0)
        filtered_another_data = another_data[(another_data['BLDG_AGE'] > age)].fillna(0)
        print(sum(filtered_residential_data['TOTAREA']))
        print(sum(filtered_another_data['TOTAREA']))
        temp_arr.append(sum(filtered_residential_data['TOTAREA']))
        temp_arr.append(sum(filtered_another_data['TOTAREA']))
        basedata_for_dfarr.append(temp_arr)
    # 작성된 데이터프레임으로 그래프 출력
    print(basedata_for_dfarr)
    df = pd.DataFrame(basedata_for_dfarr, columns=["year", "주거용", "비주거용"])
    bar = df.plot(x="year", y=["주거용", "비주거용"], kind="bar")
    # 막대 위에 값 넣기
    for p in bar.patches:
        left, bottom, width, height = p.get_bbox().bounds
        bar.annotate("%.1f" % (height / 100000000), (left + width / 2, height * 1.01), ha='center')
    plt.title('연도별 건축물 연면적 합 (㎡)')
    plt.xlabel('연도 (년)')
    plt.ylabel('연면적 합 (㎡)')
    plt.legend()
    plt.show()
    #plt.savefig('./annual_graph/연도별 건축물 연면적 변동.png')
    plt.clf()
    df.set_index('year', drop=True, inplace=True)
    df.to_excel('./annual_graph/연도별 건축물 연면적 변동.xlsx')

    # 연도별 면적당 TOE 구하기
    year_arr = [2014, 2015, 2016, 2017, 2018, 2019, 2020]
    basedata_for_dfarr = []
    for year in year_arr:
        temp_arr = []
        temp_arr.append(str(year))
        age = 2022-year
        filtered_residential_data = residential_data[(residential_data['BLDG_AGE'] > age)].fillna(0)
        filtered_another_data = another_data[(another_data['BLDG_AGE'] > age)].fillna(0)
        temp_arr.append(sum(filtered_residential_data['total_converged_toe_sum_' + str(year)])/sum(filtered_residential_data['TOTAREA']))
        temp_arr.append(sum(filtered_another_data['total_converged_toe_sum_' + str(year)])/sum(filtered_another_data['TOTAREA']))
        basedata_for_dfarr.append(temp_arr)
    # 작성된 데이터프레임으로 그래프 출력
    print(basedata_for_dfarr)
    df = pd.DataFrame(basedata_for_dfarr, columns=["year", "주거용", "비주거용"])
    bar = df.plot(x="year", y=["주거용", "비주거용"], kind="bar")
    # 막대 위에 값 넣기
    for p in bar.patches:
        left, bottom, width, height = p.get_bbox().bounds
        bar.annotate("%.4f" % (height), (left + width / 2, height * 1.01), ha='center')
    plt.title('연도별 건축물 원단위 에너지사용량 (TOE/㎡)')
    plt.xlabel('연도 (년)')
    plt.ylabel('원단위 에너지사용량 (TOE/㎡)')
    plt.legend()
    plt.show()
    #plt.savefig('./annual_graph/연도별 건축물 원단위에너지사용량 변동.png')
    plt.clf()
    df.set_index('year', drop=True, inplace=True)
    df.to_excel('./annual_graph/연도별 건축물 원단위에너지사용량 변동.xlsx')
    '''


    # 2022.05.02 추가 ================================================================================================
    # 세움터 데이터로 면적 역산한 버전
    # 주거용은 주거용만, 비주거용은 상업용+문교사회용의 데이터를 사용한다! 참조되는 역산근거 파일을 볼 것
    residential_ratio = [0.9427, 0.9556, 0.9664, 0.9735, 0.9797, 0.9889, 1]
    another_ratio = [0.8907, 0.8842, 0.9221, 0.9380, 0.9547, 0.9704, 1]
    # 이건 세움터 면적총합
    residential_value = [283051717.4, 286932777.9, 290153973.4, 292307480.4, 294160542.3, 296921359.9, 300255681.9]
    another_value = [214724518.9, 213155399.9, 222283541.2, 226129106.3, 230155476.4, 233932643.7, 241065996.8]



    # 연도별 데이터로 데이터프레임을 작성
    year_arr = [2014, 2015, 2016, 2017, 2018, 2019, 2020]
    basedata_for_dfarr = []
    for year in year_arr:
        temp_arr = []
        temp_arr.append(str(year))
        age = 2022-year
        filtered_residential_data = residential_data
        filtered_another_data = another_data
        temp_arr.append(sum(filtered_residential_data['total_converged_toe_sum_' + str(year)]))
        temp_arr.append(sum(filtered_another_data['total_converged_toe_sum_' + str(year)]))
        basedata_for_dfarr.append(temp_arr)
    # 작성된 데이터프레임으로 그래프 출력
    print(basedata_for_dfarr)
    df = pd.DataFrame(basedata_for_dfarr, columns=["year", "주거용", "비주거용"])
    bar = df.plot(x="year", y=["주거용", "비주거용"], kind="bar", rot=0)
    # 막대 위에 값 넣기
    for p in bar.patches:
        left, bottom, width, height = p.get_bbox().bounds
        bar.annotate("%.1f" % (height / 1000000), (left + width / 2, height * 1.01), ha='center')
    plt.title('연도별 건축물 에너지사용량 변동 (TOE)')
    plt.xlabel('연도 (년)')
    plt.ylabel('에너지사용량 총합(TOE)')
    plt.legend()
    plt.show()
    #plt.savefig('./annual_graph/연도별 건축물 에너지사용량 변동.png')
    plt.clf()
    df.set_index('year', drop=True, inplace=True)
    df.to_excel('./annual_graph_세움터면적값/연도별 건축물 에너지사용량 변동.xlsx')

    # 연도별 면적합 구하기
    year_arr = [2014, 2015, 2016, 2017, 2018, 2019, 2020]
    basedata_for_dfarr = []
    for year in year_arr:
        temp_arr = []
        temp_arr.append(str(year))
        age = 2022-year
        residential_data['TOTAREA'].fillna(0, inplace=True)
        another_data['TOTAREA'].fillna(0, inplace=True)
        filtered_residential_data = residential_data
        filtered_another_data = another_data
        temp_arr.append(residential_value[year_arr.index(year)])
        temp_arr.append(another_value[year_arr.index(year)])
        # temp_arr.append(sum(filtered_residential_data['TOTAREA'])*residential_ratio[year_arr.index(year)])
        # temp_arr.append(sum(filtered_another_data['TOTAREA'])*another_ratio[year_arr.index(year)])
        print(sum(filtered_residential_data['TOTAREA']))
        print(residential_ratio[year_arr.index(year)])
        print(sum(filtered_another_data['TOTAREA']))
        print(another_ratio[year_arr.index(year)])
        basedata_for_dfarr.append(temp_arr)
    # 작성된 데이터프레임으로 그래프 출력
    print(basedata_for_dfarr)
    df = pd.DataFrame(basedata_for_dfarr, columns=["year", "주거용", "비주거용"])
    bar = df.plot(x="year", y=["주거용", "비주거용"], kind="bar")
    # 막대 위에 값 넣기
    for p in bar.patches:
        left, bottom, width, height = p.get_bbox().bounds
        bar.annotate("%.1f" % (height / 100000000), (left + width / 2, height * 1.01), ha='center')
    plt.title('연도별 건축물 연면적 합 (㎡)')
    plt.xlabel('연도 (년)')
    plt.ylabel('연면적 합 (㎡)')
    plt.legend()
    plt.show()
    #plt.savefig('./annual_graph/연도별 건축물 연면적 변동.png')
    plt.clf()
    df.set_index('year', drop=True, inplace=True)
    df.to_excel('./annual_graph_세움터면적값/연도별 건축물 연면적 변동.xlsx')

    # 연도별 면적당 TOE 구하기
    year_arr = [2014, 2015, 2016, 2017, 2018, 2019, 2020]
    basedata_for_dfarr = []
    for year in year_arr:
        temp_arr = []
        temp_arr.append(str(year))
        age = 2022-year
        filtered_residential_data = residential_data.fillna(0)
        filtered_another_data = another_data.fillna(0)
        temp_arr.append(sum(filtered_residential_data['total_converged_toe_sum_' + str(year)])/residential_value[year_arr.index(year)])
        temp_arr.append(sum(filtered_another_data['total_converged_toe_sum_' + str(year)])/another_value[year_arr.index(year)])
        # temp_arr.append(sum(filtered_residential_data['total_converged_toe_sum_' + str(year)])/(sum(filtered_residential_data['TOTAREA'])*residential_ratio[year_arr.index(year)]))
        # temp_arr.append(sum(filtered_another_data['total_converged_toe_sum_' + str(year)])/(sum(filtered_another_data['TOTAREA'])*another_ratio[year_arr.index(year)]))
        basedata_for_dfarr.append(temp_arr)
    # 작성된 데이터프레임으로 그래프 출력
    print(basedata_for_dfarr)
    df = pd.DataFrame(basedata_for_dfarr, columns=["year", "주거용", "비주거용"])
    bar = df.plot(x="year", y=["주거용", "비주거용"], kind="bar")
    # 막대 위에 값 넣기
    for p in bar.patches:
        left, bottom, width, height = p.get_bbox().bounds
        bar.annotate("%.4f" % (height), (left + width / 2, height * 1.01), ha='center')
    plt.title('연도별 건축물 원단위 에너지사용량 (TOE/㎡)')
    plt.xlabel('연도 (년)')
    plt.ylabel('원단위 에너지사용량 (TOE/㎡)')
    plt.legend()
    plt.show()
    #plt.savefig('./annual_graph/연도별 건축물 원단위에너지사용량 변동.png')
    plt.clf()
    df.set_index('year', drop=True, inplace=True)
    df.to_excel('./annual_graph_세움터면적값/연도별 건축물 원단위에너지사용량 변동.xlsx')






    time.sleep(10000)

    # 기본 값을 설정
    std_area_range = [0, 100, 500, 1000, 3000, 5000, 10000, 30000]

    # 1. TOE 2000 이상 값만을 필터링
    filtered_data_toe = joined_data[(joined_data['total_converged_toe_sum_2020'] >= 2000)]
    print(filtered_data_toe)
    # 1-1. TOE 2000 이상 건축물의 건령별 개수분포
    draw_histogram_age(filtered_data_toe)
    plt.title('건축물연령구간당 개수 (TOE>2000)')
    plt.xlabel('건축물건립연도 (년)')
    plt.ylabel('건축물 수 (개)')
    current_values = plt.gca().get_yticks()
    plt.gca().set_yticklabels(['{:,.0f}'.format(x) for x in current_values])
    plt.show()
    plt.clf()
    # 1-2. TOE 2000 이상 건축물의 면적별 개수분포
    special_area_range = [0, 100, 500, 1000, 3000, 5000, 10000, 30000, 50000, 100000, 200000, 300000, 500000, 1000000]
    draw_histogram_area(filtered_data_toe, special_area_range, 'TOTAREA')
    plt.title('건축물면적구간당 개수 (TOE>2000)')
    plt.xlabel('연면적 (㎡)')
    plt.ylabel('건축물 수 (개)')
    current_values = plt.gca().get_yticks()
    plt.gca().set_yticklabels(['{:,.0f}'.format(x) for x in current_values])
    plt.show()
    plt.clf()

    # 2. 연면적 3000 이상 값만을 필터링
    filtered_data_area = joined_data[(joined_data['TOTAREA'] >= 3000)]
    # 2-1. 연면적 3000이상 건축물의 건령별 개수분포
    draw_histogram_age(filtered_data_area)
    plt.title('건축물연령구간당 개수 (area>3000㎡)')
    plt.xlabel('건축물건립연도 (년)')
    plt.ylabel('건축물 수 (개)')
    current_values = plt.gca().get_yticks()
    plt.gca().set_yticklabels(['{:,.0f}'.format(x) for x in current_values])
    plt.show()
    plt.clf()
    # 2-2. 연면적 3000 이상 건축물의 면적별 개수분포
    special_area_range = [3000, 5000, 10000, 30000, 50000, 100000]
    draw_histogram_area(filtered_data_area, special_area_range, 'TOTAREA', 0)
    plt.title('건축물면적구간당 개수 (area>3000㎡)')
    plt.xlabel('연면적 (㎡)')
    plt.ylabel('건축물 수 (개)')
    current_values = plt.gca().get_yticks()
    plt.gca().set_yticklabels(['{:,.0f}'.format(x) for x in current_values])
    plt.show()
    plt.clf()

    # 3-1. 전체건물 면적별 개수분포 (어제 하다가 터짐)
    draw_histogram_area(joined_data, std_area_range, 'TOTAREA')
    plt.title('건축물면적구간당 개수 (전체 건축물)')
    plt.xlabel('연면적 (㎡)')
    plt.ylabel('건축물 수 (개)')
    current_values = plt.gca().get_yticks()
    plt.gca().set_yticklabels(['{:,.0f}'.format(x) for x in current_values])
    plt.show()
    plt.clf()
    # 3-2. 전체건물 면적별 에너지소비량(TOE)분포
    spc_area_range = [0, 100, 500, 1000, 3000, 5000, 10000, 30000, 50000, 100000, 200000, 300000, 500000, 1000000]
    draw_energy_by_area(joined_data, spc_area_range, 'total_converged_toe_sum_2020')
    plt.title('건축물면적구간당 TOE 총량 (전체 건축물)')
    plt.xlabel('연면적 (㎡)')
    plt.ylabel('TOE')
    current_values = plt.gca().get_yticks()
    plt.gca().set_yticklabels(['{:,.0f}'.format(x) for x in current_values])
    plt.show()
    plt.clf()

    # 3-3. 전체건물 면적별 건물당에너지소비량(TOE/Bldg)분포
    spc_area_range = [0, 100, 500, 1000, 3000, 5000, 10000, 30000, 50000, 100000, 200000, 300000, 500000, 1000000]
    draw_energy_per_bldg_by_area(joined_data, spc_area_range, 'total_converged_toe_sum_2020')
    plt.title('건축물면적구간당 개별건축물 TOE 평균 (전체 건축물)')
    plt.xlabel('연면적 (㎡)')
    plt.ylabel('TOE')
    current_values = plt.gca().get_yticks()
    plt.gca().set_yticklabels(['{:,.0f}'.format(x) for x in current_values])
    plt.show()
    plt.clf()

    # 4. 에너지 소비량 구간별 개수분포
    energy_range = [0, 2, 4, 6, 8, 10, 15, 20, 50, 150, 200, 500, 1000, 2000, 3000]
    draw_histogram_area(joined_data, energy_range, 'total_converged_toe_sum_2020')
    plt.title('건축물TOE구간당 개수 (전체 건축물)')
    plt.xlabel('TOE')
    plt.ylabel('건축물 수 (개)')
    current_values = plt.gca().get_yticks()
    plt.gca().set_yticklabels(['{:,.0f}'.format(x) for x in current_values])
    plt.show()
    plt.clf()


    # 5. 에너지 소비량 구간별 개수분포 (확장)
    energy_range = [3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 15000, 20000, 50000]
    draw_histogram_area(joined_data, energy_range, 'total_converged_toe_sum_2020')
    plt.title('건축물TOE구간당 개수 (전체 건축물)')
    plt.xlabel('TOE')
    plt.ylabel('건축물 수 (개)')
    current_values = plt.gca().get_yticks()
    plt.gca().set_yticklabels(['{:,.0f}'.format(x) for x in current_values])
    plt.show()
    plt.clf()

    # 6. 에너지 소비량 구간별 에너지소비합
    energy_range = [0, 10, 30, 100, 500, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 15000, 20000, 50000]
    draw_energy_by_energy(joined_data, energy_range, 'total_converged_toe_sum_2020')
    plt.title('건축물TOE구간당 TOE합 (전체 건축물)')
    plt.xlabel('TOE')
    plt.ylabel('TOE')
    current_values = plt.gca().get_yticks()
    plt.gca().set_yticklabels(['{:,.0f}'.format(x) for x in current_values])
    plt.show()
    plt.clf()

draw_graph_set()
#
#
#
print('finished!')

# =============================================================================================================
# 여기부터는 분석을 위한 별도 그래프 플로팅임

def input_bar_number_float(bar):
    for item in bar:
        height = item.get_height()
        text = '{:0,.6f}'.format(height)
        plt.text(item.get_x() + item.get_width() / 2.0, height, text, ha='center', va='bottom')

def draw_energy_divarea_by_area(data, energy_range, label):
    # x축이 늘어지는걸 막기 위해 면적의 극단값을 쳐낸다.
    #data = drop_extreme(data, label)
    # 데이터프레임을 결과로 받아온다 (분할된 것의 합을 구해야 하므로)
    divided_res, div_label = div_by_area(data, energy_range, 'dataframe', 'TOTAREA')
    # divided_res(데이터프레임 배열)을 기반으로 구간당 합을 계산
    # 하단의 plt.bar과 plt.xticks에서 dataframe배열을 집어넣으면 hash 오류가 생김 (iterable 문제인 듯...?)
    # 매번 데이터프레임에서 원하는 값을 뽑아줄 필요가 있음.
    energy_sum_arr = []
    for i in range(len(divided_res)):
        energy_sum_arr.append(divided_res[i][label].mean())
    bar = plt.bar(range(len(energy_sum_arr)), energy_sum_arr)
    plt.xticks(range(len(energy_sum_arr)), div_label)
    input_bar_number_float(bar)

def draw_age_TOE_histogram(data, label, x_limit, resolution):
    # 건축물의 연령이니 극단값을 쳐낼 필요 자체가 없음
    divided_res, div_label = div_by_age(data, 'dataframe', 'BLDG_AGE')
    x_range = []
    #print(divided_res['total_converged_toe_sum_2020'])
    for i in range(0, resolution):
        x_range.append(i*x_limit/resolution)
    # 결과물로부터 그래프를 출력
    for i in range(len(divided_res)):
        # print(divided_res[i][label])
        plt.hist(divided_res[i][label], alpha=0.5, bins=x_range, histtype='step', label=div_label[i])
        # data_for_plot = divided_res[i][label]
        # #print(data_for_plot)
        # data_for_plot = data_for_plot/0.000086
        # # data_for_plot = data_for_plot.replace([np.inf, -np.inf], np.nan)
        # # data_for_plot.dropna()
        # # max_val = data_for_plot.max()
        # # min_val = data_for_plot.min()
        # # print(data_for_plot)
        # # data_for_plot = (data_for_plot-min_val)/(max_val-min_val)
        # #print(data_for_plot)
        # #sns.distplot(divided_res[i][label], label=div_label[i], hist=False)
        # sns.kdeplot(data_for_plot, label=div_label[i])

def draw_histogram_area_mod(data, data_range, label='TOTAREA', spctype = 0):
    def input_bar_number_float_mod(bar):
        for item in bar:
            height = item.get_height()
            text = '{:0,.0f}'.format(height)
            plt.text(item.get_x() + item.get_width() / 2.0, height, text, ha='center', va='bottom')
    # 건축물의 면적이므로 극단값을 쳐낸다
    # data = drop_extreme(data, label)
    # x_range는 대체할 구간을 통째로 집어넣어 준다.
    #if spctype == 0:
    divided_res, div_label = div_by_area(data, data_range, 'count', label)
    print(divided_res)
    print(div_label)
    bar = plt.bar(range(len(divided_res)), divided_res)
    plt.xticks(range(len(divided_res)), div_label)
    input_bar_number_float_mod(bar)
    # elif spctype == 1:
    #     divided_res, div_label = div_by_area_special(data, 'count', label)
    #     plt.bar(range(len(divided_res)), divided_res)
    #     plt.xticks(range(len(divided_res)), div_label)

joined_data = pd.read_excel('toe_sum_age_linked_v4.xlsx')
joined_data.set_index('MGM_BLD_PK', drop=True, inplace=True)
joined_data['total_converged_toe_sum_divarea_2020'] = joined_data['total_converged_toe_sum_2020']/joined_data['TOTAREA']

# divided_res, div_label = div_by_age(joined_data, 'dataframe', 'BLDG_AGE')
# x_range = []
# # print(divided_res['total_converged_toe_sum_2020'])
# # 결과물로부터 그래프를 출력
# def pdf_drawer(data, label, dist_res, pdf_sort, label_text):
#     # 기본적으로 위의 data_fitting2와 같지만, 최종그래프 출력을 위해 따로 만든 것임.
#     # distifit 라이브러리의 결과에서 분포의 종류를 리스트로 바꿔 저장함 (분포명에 맞는 loc, scale을 가져오기 위함)
#     print('dist_res')
#     print(dist_res)
#     dist_res_arr = dist_res['distr'].tolist()
#     # 데이터 라벨로 데이터를 배열로 바꿈
#     data_for_fit = data[label].values
#
#     # 범위 설정. 데이터의 최소-최대 값 기준에 resolution은 10000.
#     range = np.linspace(min(data_for_fit), max(data_for_fit), 10000)
#
#     # 이 케이스에서는 확률밀도함수의 종류는 1개로 한정지음 (최적의 1개를 선택했다고 가정)
#     pdf_count = dist_res_arr.index(pdf_sort)
#     distribution = generate_pdf(pdf_sort, dist_res['loc'][pdf_count], dist_res['scale'][pdf_count],
#                                 dist_res['arg'][pdf_count])
#     # range에 맞게 분포를 기준으로 확률밀도함수를 생성
#     pdf = distribution.pdf(range)
#     # 해당 내용으로 확률밀도함수를 플로팅
#     plt.plot(range, pdf, label= label_text)
#
# for i in range(len(divided_res)):
#     print(divided_res[i]['total_converged_toe_sum_divarea_2020'])
#     data_for_plot = divided_res[i]
#     if data_for_plot.size == 0:
#         continue
#     else:
#         data_for_plot['total_converged_toe_sum_divarea_2020'] = data_for_plot['total_converged_toe_sum_divarea_2020'].replace([np.inf, -np.inf], np.nan)
#         data_for_plot = data_for_plot.dropna()
#         fit_result = data_fitting(data_for_plot, 'total_converged_toe_sum_divarea_2020')
#         pdf_drawer(data_for_plot, 'total_converged_toe_sum_divarea_2020', fit_result, 't',  div_label[i])
#         plt.show()
# plt.title('TOE 히스토그램 (전체 건축물)')
# plt.legend()
# plt.show()


#filtered_joined_data_total = joined_data[(joined_data['TOTAREA'] >= 100)&(joined_data['TOTAREA'] < 3000)]

# filtered_joined_data = joined_data[(joined_data['TOTAREA'] >= 100)&(joined_data['TOTAREA'] < 500)]
# # 면적당사용량 값의 구간별 히스토그램
# energy_range = [0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 1]
# draw_histogram_area_mod(filtered_joined_data, energy_range, 'total_converged_toe_sum_divarea_2020')
# plt.title('건축물 단위면적당 TOE 개수 (Area: 100~500㎡)')
# plt.xlabel('TOE/㎡')
# plt.ylabel('건축물 수 (개)')
# current_values = plt.gca().get_yticks()
# plt.gca().set_yticklabels(['{:,.0f}'.format(x) for x in current_values])
# plt.show()
# plt.clf()
#
# filtered_joined_data = joined_data[(joined_data['TOTAREA'] >= 500)&(joined_data['TOTAREA'] < 1000)]
# # 면적당사용량 값의 구간별 히스토그램
# energy_range = [0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 1]
# draw_histogram_area_mod(filtered_joined_data, energy_range, 'total_converged_toe_sum_divarea_2020')
# plt.title('건축물 단위면적당 TOE 개수 (Area: 500~1000㎡)')
# plt.xlabel('TOE/㎡')
# plt.ylabel('건축물 수 (개)')
# current_values = plt.gca().get_yticks()
# plt.gca().set_yticklabels(['{:,.0f}'.format(x) for x in current_values])
# plt.show()
# plt.clf()
#
# filtered_joined_data = joined_data[(joined_data['TOTAREA'] >= 1000)&(joined_data['TOTAREA'] < 3000)]
# # 면적당사용량 값의 구간별 히스토그램
# energy_range = [0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 1]
# draw_histogram_area_mod(filtered_joined_data, energy_range, 'total_converged_toe_sum_divarea_2020')
# plt.title('건축물 단위면적당 TOE 개수 (Area: 1000~3000㎡)')
# plt.xlabel('TOE/㎡')
# plt.ylabel('건축물 수 (개)')
# current_values = plt.gca().get_yticks()
# plt.gca().set_yticklabels(['{:,.0f}'.format(x) for x in current_values])
# plt.show()
# plt.clf()

# # =================================================================================================================
# 연령별 TOE 히스토그램 - 단위면적당 TOE
draw_age_TOE_histogram(joined_data, 'total_converged_toe_sum_divarea_2020', 0.1, 100)
plt.title('TOE 히스토그램 (전체 건축물)')
plt.legend()
plt.show()
#
# # 면적구간별로 끊어서 출력 (하드코드로 때움)
# filtered_joined_data = joined_data[(joined_data['TOTAREA'] >= 0)&(joined_data['TOTAREA'] < 100)]
# draw_age_TOE_histogram(filtered_joined_data, 'total_converged_toe_sum_divarea_2020', 1, 1000)
# plt.title('TOE 히스토그램 (area:~100㎡)')
# plt.xlabel('TOE')
# plt.ylabel('건축물 수 (개)')
# current_values = plt.gca().get_yticks()
# plt.gca().set_yticklabels(['{:,.0f}'.format(x) for x in current_values])
# plt.legend()
# plt.show()
#
# filtered_joined_data = joined_data[(joined_data['TOTAREA'] >= 100)&(joined_data['TOTAREA'] < 500)]
# draw_age_TOE_histogram(filtered_joined_data, 'total_converged_toe_sum_divarea_2020', 1, 1000)
# plt.title('TOE 히스토그램 (area:100~500㎡)')
# plt.xlabel('TOE')
# plt.ylabel('건축물 수 (개)')
# current_values = plt.gca().get_yticks()
# plt.gca().set_yticklabels(['{:,.0f}'.format(x) for x in current_values])
# plt.legend()
# plt.show()
#
# filtered_joined_data = joined_data[(joined_data['TOTAREA'] >= 500)&(joined_data['TOTAREA'] < 1000)]
# draw_age_TOE_histogram(filtered_joined_data, 'total_converged_toe_sum_divarea_2020', 1, 1000)
# plt.title('TOE 히스토그램 (area:500~1000㎡)')
# plt.xlabel('TOE')
# plt.ylabel('건축물 수 (개)')
# current_values = plt.gca().get_yticks()
# plt.gca().set_yticklabels(['{:,.0f}'.format(x) for x in current_values])
# plt.legend()
# plt.show()
#
# filtered_joined_data = joined_data[(joined_data['TOTAREA'] >= 1000)&(joined_data['TOTAREA'] < 3000)]
# draw_age_TOE_histogram(filtered_joined_data, 'total_converged_toe_sum_divarea_2020', 1, 1000)
# plt.title('TOE 히스토그램 (area:1000~3000㎡)')
# plt.xlabel('TOE')
# plt.ylabel('건축물 수 (개)')
# current_values = plt.gca().get_yticks()
# plt.gca().set_yticklabels(['{:,.0f}'.format(x) for x in current_values])
# plt.legend()
# plt.show()
#
# filtered_joined_data = joined_data[(joined_data['TOTAREA'] >= 3000)&(joined_data['TOTAREA'] < 5000)]
# draw_age_TOE_histogram(filtered_joined_data, 'total_converged_toe_sum_divarea_2020', 1, 1000)
# plt.title('TOE 히스토그램 (area:3000~5000㎡)')
# plt.xlabel('TOE')
# plt.ylabel('건축물 수 (개)')
# current_values = plt.gca().get_yticks()
# plt.gca().set_yticklabels(['{:,.0f}'.format(x) for x in current_values])
# plt.legend()
# plt.show()
#
# filtered_joined_data = joined_data[(joined_data['TOTAREA'] >= 5000)&(joined_data['TOTAREA'] < 10000)]
# draw_age_TOE_histogram(filtered_joined_data, 'total_converged_toe_sum_divarea_2020', 1, 1000)
# plt.title('TOE 히스토그램 (area:5000~10000㎡)')
# plt.xlabel('TOE')
# plt.ylabel('건축물 수 (개)')
# current_values = plt.gca().get_yticks()
# plt.gca().set_yticklabels(['{:,.0f}'.format(x) for x in current_values])
# plt.legend()
# plt.show()
#
# filtered_joined_data = joined_data[(joined_data['TOTAREA'] >= 10000)&(joined_data['TOTAREA'] < 30000)]
# draw_age_TOE_histogram(filtered_joined_data, 'total_converged_toe_sum_divarea_2020', 4, 2000)
# plt.title('TOE 히스토그램 (area:10000~30000㎡)')
# plt.xlabel('TOE')
# plt.ylabel('건축물 수 (개)')
# current_values = plt.gca().get_yticks()
# plt.gca().set_yticklabels(['{:,.0f}'.format(x) for x in current_values])
# plt.legend()
# plt.show()
#
# filtered_joined_data = joined_data[(joined_data['TOTAREA'] >= 30000)]
# draw_age_TOE_histogram(filtered_joined_data, 'total_converged_toe_sum_divarea_2020', 60, 600)
# plt.title('TOE 히스토그램 (area:30000㎡~)')
# plt.xlabel('TOE')
# plt.ylabel('건축물 수 (개)')
# current_values = plt.gca().get_yticks()
# plt.gca().set_yticklabels(['{:,.0f}'.format(x) for x in current_values])
# plt.legend()
# plt.show()
#
#
#
# # =================================================================================================================
# # 연령별 TOE 히스토그램 - TOE총량
# draw_age_TOE_histogram(joined_data, 'total_converged_toe_sum_2020', 400, 4000)
# plt.title('TOE 히스토그램 (전체 건축물)')
# plt.xlabel('TOE')
# plt.ylabel('건축물 수 (개)')
# current_values = plt.gca().get_yticks()
# plt.gca().set_yticklabels(['{:,.0f}'.format(x) for x in current_values])
# plt.legend()
# plt.show()
#
# # 면적구간별로 끊어서 출력 (하드코드로 때움)
# filtered_joined_data = joined_data[(joined_data['TOTAREA'] >= 0)&(joined_data['TOTAREA'] < 100)]
# draw_age_TOE_histogram(filtered_joined_data, 'total_converged_toe_sum_2020', 400, 4000)
# plt.title('TOE 히스토그램 (area:~100㎡)')
# plt.xlabel('TOE')
# plt.ylabel('건축물 수 (개)')
# current_values = plt.gca().get_yticks()
# plt.gca().set_yticklabels(['{:,.0f}'.format(x) for x in current_values])
# plt.legend()
# plt.show()
#
# filtered_joined_data = joined_data[(joined_data['TOTAREA'] >= 100)&(joined_data['TOTAREA'] < 500)]
# draw_age_TOE_histogram(filtered_joined_data, 'total_converged_toe_sum_2020', 400, 4000)
# plt.title('TOE 히스토그램 (area:100~500㎡)')
# plt.xlabel('TOE')
# plt.ylabel('건축물 수 (개)')
# current_values = plt.gca().get_yticks()
# plt.gca().set_yticklabels(['{:,.0f}'.format(x) for x in current_values])
# plt.legend()
# plt.show()
#
# filtered_joined_data = joined_data[(joined_data['TOTAREA'] >= 500)&(joined_data['TOTAREA'] < 1000)]
# draw_age_TOE_histogram(filtered_joined_data, 'total_converged_toe_sum_2020', 400, 4000)
# plt.title('TOE 히스토그램 (area:500~1000㎡)')
# plt.xlabel('TOE')
# plt.ylabel('건축물 수 (개)')
# current_values = plt.gca().get_yticks()
# plt.gca().set_yticklabels(['{:,.0f}'.format(x) for x in current_values])
# plt.legend()
# plt.show()
#
# filtered_joined_data = joined_data[(joined_data['TOTAREA'] >= 1000)&(joined_data['TOTAREA'] < 3000)]
# draw_age_TOE_histogram(filtered_joined_data, 'total_converged_toe_sum_2020', 400, 400)
# plt.title('TOE 히스토그램 (area:1000~3000㎡)')
# plt.xlabel('TOE')
# plt.ylabel('건축물 수 (개)')
# current_values = plt.gca().get_yticks()
# plt.gca().set_yticklabels(['{:,.0f}'.format(x) for x in current_values])
# plt.legend()
# plt.show()
#
# filtered_joined_data = joined_data[(joined_data['TOTAREA'] >= 3000)&(joined_data['TOTAREA'] < 5000)]
# draw_age_TOE_histogram(filtered_joined_data, 'total_converged_toe_sum_2020', 200, 75)
# plt.title('TOE 히스토그램 (area:3000~5000㎡)')
# plt.xlabel('TOE')
# plt.ylabel('건축물 수 (개)')
# current_values = plt.gca().get_yticks()
# plt.gca().set_yticklabels(['{:,.0f}'.format(x) for x in current_values])
# plt.legend()
# plt.show()
#
# filtered_joined_data = joined_data[(joined_data['TOTAREA'] >= 5000)&(joined_data['TOTAREA'] < 10000)]
# draw_age_TOE_histogram(filtered_joined_data, 'total_converged_toe_sum_2020', 300, 50)
# plt.title('TOE 히스토그램 (area:5000~10000㎡)')
# plt.xlabel('TOE')
# plt.ylabel('건축물 수 (개)')
# current_values = plt.gca().get_yticks()
# plt.gca().set_yticklabels(['{:,.0f}'.format(x) for x in current_values])
# plt.legend()
# plt.show()
#
# filtered_joined_data = joined_data[(joined_data['TOTAREA'] >= 10000)&(joined_data['TOTAREA'] < 30000)]
# draw_age_TOE_histogram(filtered_joined_data, 'total_converged_toe_sum_2020', 1000, 50)
# plt.title('TOE 히스토그램 (area:10000~30000㎡)')
# plt.xlabel('TOE')
# plt.ylabel('건축물 수 (개)')
# current_values = plt.gca().get_yticks()
# plt.gca().set_yticklabels(['{:,.0f}'.format(x) for x in current_values])
# plt.legend()
# plt.show()
#
# filtered_joined_data = joined_data[(joined_data['TOTAREA'] >= 30000)]
# draw_age_TOE_histogram(filtered_joined_data, 'total_converged_toe_sum_2020', 60000, 600)
# plt.title('TOE 히스토그램 (area:30000㎡~)')
# plt.xlabel('TOE')
# plt.ylabel('건축물 수 (개)')
# current_values = plt.gca().get_yticks()
# plt.gca().set_yticklabels(['{:,.0f}'.format(x) for x in current_values])
# plt.legend()
# plt.show()
#
# # 면적당사용량 값의 구간별 히스토그램
# energy_range = [0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 1]
# draw_histogram_area_mod(joined_data, energy_range, 'total_converged_toe_sum_divarea_2020')
# plt.title('건축물 단위면적당 TOE 개수 (전체 건축물)')
# plt.xlabel('TOE/㎡')
# plt.ylabel('건축물 수 (개)')
# current_values = plt.gca().get_yticks()
# plt.gca().set_yticklabels(['{:,.0f}'.format(x) for x in current_values])
# plt.show()
# plt.clf()
#
# # 면적구간당 단위면적당 TOE소비량 평균
# std_area_range = [0, 100, 500, 1000, 3000, 5000, 10000, 30000]
# draw_energy_divarea_by_area(joined_data, std_area_range, 'total_converged_toe_sum_divarea_2020')
# plt.title('건축물 단위면적당 TOE 평균 (전체 건축물)')
# plt.xlabel('연면적 (㎡)')
# plt.ylabel('TOE/㎡')
# current_values = plt.gca().get_yticks()
# plt.gca().set_yticklabels(['{:,.0f}'.format(x) for x in current_values])
# plt.show()
# plt.clf()

# # 1. TOE/연령 Scatterplot
# plt.scatter(joined_data['total_converged_toe_sum_2020'], joined_data['TOTAREA'], s=1)
# plt.xlabel('TOE')
# plt.ylabel('연면적 (㎡)')
# plt.show()
# plt.clf()




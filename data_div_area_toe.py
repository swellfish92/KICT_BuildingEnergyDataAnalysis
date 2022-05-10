import pandas as pd
import copy

data = pd.read_csv('E:/PycharmProjects/KICT_BuildingEnergyDataAnalysis/Data_join/최종에너지합산결과_2020_20220507_v3.csv')
#data.set_index('PNU', drop=True, inplace=True)

data = data[['PNU', 'mainPurpsCdNm', 'totArea', 'toe_2020', 'count']]
data = data[(data['mainPurpsCdNm'] != '단독주택') & (data['mainPurpsCdNm'] != '공동주택')]
data = data.astype({'PNU':'str', 'mainPurpsCdNm':'str', 'totArea':'float', 'toe_2020':'float', 'count':'int'})
res_arr_count = (
    '500TOE이하',
    '1000TOE이하',
    '1500TOE이하',
    '2000TOE이하',
    '2500TOE이하',
    '3000TOE이하',
    '5000TOE이하',
    '10000TOE이하',
    '10000TOE이상'
)

res_arr_area = copy.deepcopy(res_arr_count)
area_split_arr = [0, 100, 500, 1000, 3000, 5000, 10000, 30000]
toe_split_arr = [0, 500, 1000, 1500, 2000, 2500, 3000, 5000, 10000]
split_df = data

final_area_area_arr = []
final_area_count_arr = []
final_area_toe_arr = []
for area_iter in range(len(area_split_arr)):
    temp_toe_area_arr = []
    temp_toe_count_arr = []
    temp_toe_toe_arr = []
    for toe_iter in range(len(toe_split_arr)):
        split_df = data
        if area_iter == 0:
            split_df = split_df[(split_df['totArea'] <= area_split_arr[area_iter + 1])]
        elif area_iter == len(area_split_arr)-1:
            split_df = split_df[(split_df['totArea'] > area_split_arr[area_iter])]
        else:
            split_df = split_df[(split_df['totArea'] >= area_split_arr[area_iter]) & (split_df['totArea'] < area_split_arr[area_iter + 1])]

        if toe_iter == 0:
            split_df = split_df[(split_df['toe_2020'] <= toe_split_arr[toe_iter + 1])]
        elif toe_iter == len(toe_split_arr)-1:
            split_df = split_df[(split_df['toe_2020'] > toe_split_arr[toe_iter])]
        else:
            split_df = split_df[(split_df['toe_2020'] >= toe_split_arr[toe_iter]) & (split_df['toe_2020'] < toe_split_arr[toe_iter + 1])]

        temp_toe_area_arr.append(sum(split_df['totArea']))
        temp_toe_count_arr.append(sum(split_df['count']))
        temp_toe_toe_arr.append(sum(split_df['toe_2020']))

    final_area_area_arr.append(temp_toe_area_arr)
    final_area_count_arr.append(temp_toe_count_arr)
    final_area_toe_arr.append(temp_toe_toe_arr)

res_df_area = pd.DataFrame(final_area_area_arr, columns=res_arr_count)
res_df_count = pd.DataFrame(final_area_count_arr, columns=res_arr_count)
res_df_toe = pd.DataFrame(final_area_toe_arr, columns=res_arr_count)

res_df_area.to_csv('E:/PycharmProjects/KICT_BuildingEnergyDataAnalysis/Data_join/상업공공_연면적합_result.csv', encoding='utf-8 sig')
res_df_count.to_csv('E:/PycharmProjects/KICT_BuildingEnergyDataAnalysis/Data_join/상업공공_건축물수_result.csv', encoding='utf-8 sig')
res_df_toe.to_csv('E:/PycharmProjects/KICT_BuildingEnergyDataAnalysis/Data_join/상업공공_toe_result.csv', encoding='utf-8 sig')



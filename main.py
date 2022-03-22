# summative main method
# enlist code for each project here

from functions import *
from csv_read import *
from db_read import *

# 데이터 읽어오기 (from DB)
data = get_fulldata()

# 특정용도 데이터 출력부분(주석처리)
'''data_for_save = data[(data['MAIN_PURPS_NM'] == '업무시설')]
data_for_save.to_excel('result.xlsx')
import time
time.sleep(100)'''

# CSV를 읽어와서 건물용도 배열을 작성
# sort_list = remove_duplicated(data['MAIN_PURPS_NM'])

final_data = data[['USEAPR_DAY', 'MAIN_PURPS_NM', 'total_converged_EUI']]
print(final_data)

# 값 100이하, 2000 초과치를 제거함(극단치로 인해 정규분포 에러가 튀는 것을 막음)
final_data = final_data[(final_data['total_converged_EUI'] <= 2000) & (final_data['total_converged_EUI'] > 100)]
print(final_data['total_converged_EUI'])

# sort_list를 작성하는 방법들임
# 1. 건물용도에서 중복을 제거한 리스트 (전체)
sort_list = remove_duplicated(final_data['MAIN_PURPS_NM'])

# 2. 직접 sort_list를 작성 (원하는 건물용도만 사용)
#sort_list = ['교육연구시설', '노유자시설', '단독주택', '문화및집회시설', '위락시설', '제1종근린생활시설', '제2종근린생활시설']

print('==============================================================================================')
print('Sort List is selected as below:')
print(sort_list)
print('==============================================================================================')

# ==============================================================================================
# 여기에 아래에서 사용되는 함수들에 대한 설명을 기술함
# 그래프를 플로팅하는 함수는 크게 3종류임
# plot_fitting_comparison: 최적의 fitting함수를 비교하는 그래프임. fit_matrix를 별개로 요구하며, data에서 total_converged_EUI라벨 데이터로 그래프를 출력함
# data_fitting2: 개별 PDF 그래프를 출력함
# draw_final_graph: 개별 PDF, CDF 그래프를 출력하며, point 인자로 사전 설정된 PK코드를 조회해 해당 위치에 Line을 출력함
# ==============================================================================================

# Case 1. 비교 그래프 출력
# 직관성을 위해 공정 2단계를 별개로 main함수에 기술함
# 1. fit_matrix로 건물용도별 최적분포함수 종류를 호출
fit_matrix = get_fit_matrix(sort='excluded')

# 2. 해당 매트릭스를 인자로 비교함수를 호출
plot_fitting_comparison(fit_matrix, data, show=True, save=False, second_label='')


# Case 2. 전체 그래프 플로팅
# 맨 아래에서 플로팅함수 2개중 하나를 골라서 사용하면 됨. (사용 안할 때는 주석 처리)

#특정 분류만을 출력할 경우, 아래처럼 sort_list를 재정의. (위를 다시 바꾸기 귀찮으니...)
sort_list = ['업무시설']

for purpose in sort_list:
    sample_data = final_data[(data['MAIN_PURPS_NM'] == purpose)]

    #
    #sample_data = final_data.sample(n=50000)
    #sample_data = final_data

    #distribute_plot(sample_data, 'total_converged_EUI')
    #print(sample_data)

    print('start fitting for : ' + str(purpose))
    print('==============================================================================================')
    fit_result = data_fitting(sample_data, 'total_converged_EUI')
    pd.set_option('display.max_rows', 10000)
    pd.set_option('display.max_columns', 10000)
    # print(fit_result)
    print('==============================================================================================')
    print('starting graph plotting')
    # dists =  ['norm', 'expon', 'dweibull', 't', 'beta']
    dists = ['norm', 't', 'loggamma', 'dweibull']  # for normal data
    # dists = fit_result['distr']

    # data_fitting2 : 개별 PDF 그래프를 플로팅
    #data_fitting2(sample_data, 'total_converged_EUI', fit_result, dists, show=True, save=False, second_label=purpose)

    # draw_final_graph : 개별 PDF, CDF그래프를 출력하고, 사전지정된 특정건물(서울시청사)을 라인으로 출력. 이 경우 분포는 개별설정.
    draw_final_graph(sample_data, 'total_converged_EUI', fit_result, 't', title='All_data', show=True, save=False, point=True, second_label=purpose)


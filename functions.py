import seaborn as sns
import numpy as np
import scipy as sp
from fitter import Fitter, get_common_distributions, get_distributions
import matplotlib.pyplot as plt
import propagate
import pandas as pd

# 한글 폰트 사용을 위해서 세팅
from matplotlib import font_manager, rc
font_path = "C:/Windows/Fonts/NGULIM.TTF"
font = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font)





# 중복을 제거한 배열을 반환함
def remove_duplicated(list):
    temp_list = []
    for item in list:
        if item not in temp_list:
            temp_list.append(item)
    return temp_list

# 시설용도의 영문배열명 변환
def facility_kor_to_eng(korname):
    kor_list = ['위락시설', '단독주택', '공동주택', '제2종근린생활시설', '교육연구시설', '노유자시설', '제1종근린생활시설', '문화및집회시설', '종교시설', '의료시설', '업무시설', '숙박시설', '창고시설', '판매시설', '', '자동차관련시설', '위험물저장및처리시설', '공장', '운동시설', '수련시설', '교정및군사시설', '운수시설', '방송통신시설', '관광휴게시설', '동.식물관련시설', '발전시설', '장례식장', '자원순환관련시설', '묘지관련시설', '야영장시설']
    eng_list = ['Amusement facilities', 'detached houses', 'communal houses', 'second-class neighborhood living facilities', 'educational research facilities', 'older facilities', 'first-class neighborhood living facilities', 'cultural and assembly facilities', 'religious facilities', 'medical facilities', 'business facilities', 'lodging facilities', 'warehouse facilities', 'sales facilities', '', 'vehicle-related facilities', 'dangerous material storage and treatment facilities', 'Factory', 'exercise facility', 'training facility', 'correction and military facility', 'transport facility', 'broadcast communication facility', 'tourism rest facility', 'animal/plant related facility', 'power generation facility', 'Funeral', 'Resource circulation related facilities', 'cemetery related facilities', 'campsite facilities']
    return eng_list[kor_list.index(korname)]

def distribute_plot(data, label, type='both'):
    k = []
    target = 20000
    div = 0.01
    for i in range(0, 200):
        k.append(i / div)

    if type == 'both':
        sns.distplot(data[label], bins=k)
        plt.xlim(0, 4000)
        plt.show()
    elif type == 'hist':
        sns.displot(data[label], kde=False)
        plt.show()
    elif type == 'kde':
        sns.displot(data[label], hist=False)
        plt.show()
    else:
        print('invalid type. please use one of |both|hist|kde|')

def data_fitting(data, label):

    data_for_fit = data[label].values
    print(data_for_fit)
    '''print(get_common_distributions())
    f = Fitter(data_for_fit, distributions=get_common_distributions())
    f.fit()
    print(f)
    print(f.summary())
    best = f.get_best(method='sumsquare_error')
    print(best)

    print("----------------------------------------------")
    for item in get_common_distributions():
        print(f.fitted_param[item])
        print("----------------------------------------------")'''



    from distfit import distfit
    dist = distfit()
    result = dist.fit_transform(data_for_fit)
    print("----------------------------------------------")
    #print(result)
    print("----------------------------------------------")
    print(dist.summary.head())
    print("----------------------------------------------")
    print(dist.model)

    return dist.summary
    #dist.plot()


    # print(dist.summary)
    # dist.summary.plot()
    #
    # print(dist.plot())

def generate_pdf(sort, loc, scale, arg=()):
    if sort == 'norm':
        return sp.stats.norm(loc=loc, scale=scale)
    elif sort == 'expon':
        return sp.stats.expon(loc=loc, scale=scale)
    elif sort == 'pareto':
        return sp.stats.pareto(loc=loc, scale=scale, b=arg[0])
    elif sort == 'dweibull':
        return sp.stats.dweibull(loc=loc, scale=scale, c=arg[0])
    elif sort == 't':
        return sp.stats.t(loc=loc, scale=scale, df=arg[0])
    elif sort == 'genextreme':
        return sp.stats.genextreme(loc=loc, scale=scale, c=arg[0])
    elif sort == 'gamma':
        return sp.stats.gamma(loc=loc, scale=scale, a=arg[0])
    elif sort == 'lognorm':
        return sp.stats.lognorm(loc=loc, scale=scale, s=arg[0])
    elif sort == 'beta':
        return sp.stats.beta(loc=loc, scale=scale, a=arg[0], b=arg[1])
    elif sort == 'uniform':
        return sp.stats.uniform(loc=loc, scale=scale)
    elif sort == 'loggamma':
        return sp.stats.loggamma(loc=loc, scale=scale, c=arg[0])
    else:
        print("error // not supported pdf type")


def data_fitting2(data, label, dist_res, pdf_sorts,  show=True, save=False, second_label=''):
    # 시설분류를 영문으로 전환 (폰트가 깨져서...)
    # Update로 한글 폰트 지원됨 (지금은 이 부분을 쓸 이유가 없음)
    # if second_label != '':
    #     second_label = facility_kor_to_eng(second_label)

    # distifit 라이브러리의 결과에서 분포의 종류를 리스트로 바꿔 저장함 (분포명에 맞는 loc, scale을 가져오기 위함)
    dist_res_arr = dist_res['distr'].tolist()

    # 데이터 라벨로 데이터를 배열로 바꿈
    data_for_fit = data[label].values

    # 범위 설정. 데이터의 최소-최대 값 기준에 resolution은 10000.
    range = np.linspace(min(data_for_fit), max(data_for_fit), 10000)

    #이 부분의 pdf생성을 확률밀도함수 타입별로 바뀌게 해야함. (작업 완료되었고, 작업 이전 레거시 코드를 보존용으로 아래와 같이 남김.)
    #pdf_count = dist_res_arr.index('norm')
    '''print('data from distfit')
    print((dist_res['loc'][pdf_count], dist_res['scale'][pdf_count]))
    print('data from scipy')
    mu, std = sp.stats.norm.fit(data_for_fit)
    print((mu, std))
    p = sp.stats.norm.pdf(range, mu, std)
    plt.plot(range, p, 'k', linewidth=2, label='normal_dist_2')

    pdf = sp.stats.norm.pdf(range, dist_res['loc'][pdf_count], dist_res['scale'][pdf_count])
    plt.plot(pdf, label='normal_dist')
    #plt.legend()
    #plt.show()'''


    #새로 바뀐 타입별 확률밀도함수 생성 코드
    for pdf_sort in pdf_sorts:
        pdf_count = dist_res_arr.index(pdf_sort)
        print(pdf_count)
        data_for_fit = data[label].values
        print(dist_res['loc'][pdf_count])
        print(dist_res['scale'][pdf_count])
        distribution = generate_pdf(pdf_sort, dist_res['loc'][pdf_count], dist_res['scale'][pdf_count], dist_res['arg'][pdf_count])

        # range에 맞게 분포를 기준으로 확률밀도함수를 생성
        pdf = distribution.pdf(range)

        # 해당 내용으로 확률밀도함수를 플로팅
        plt.plot(range, pdf, label=pdf_sort)

    # 지정된 건물을 표기
    # PK-code 11140-185 건물(서소문청사)
    ''' PK = '11140-185'
    highlight_data = data.iloc[data.index.tolist().index('11140-185')]
    print('Result for ' + str(PK))
    print(data.iloc[data.index.tolist().index('11140-185')])

    plt.axvline(x=highlight_data['total_converged_EUI'], color='red', label='point for ' + str(PK))'''

    # 배경 히스토그램
    plt.hist(data_for_fit, bins=100, range=(0, 2000), density=True, color='lightgrey')

    # 최종 출력
    plt.legend()
    plt.title('Histogram and PDFs of ' + str(second_label))

    if show == True:
        plt.show()
    if save == True:
        plt.savefig('PDF_percentile_' + '(' + pdf_sort + '_' + second_label + ')' + '.png')

    # 플롯 초기화
    plt.clf()

def draw_final_graph(data, label, dist_res, pdf_sort, title='default_title', show=True, save=False, point=True, second_label=''):
    #기본적으로 위의 data_fitting2와 같지만, 최종그래프 출력을 위해 따로 만든 것임.

    # distifit 라이브러리의 결과에서 분포의 종류를 리스트로 바꿔 저장함 (분포명에 맞는 loc, scale을 가져오기 위함)
    dist_res_arr = dist_res['distr'].tolist()
    # 데이터 라벨로 데이터를 배열로 바꿈
    data_for_fit = data[label].values

    # 범위 설정. 데이터의 최소-최대 값 기준에 resolution은 10000.
    range = np.linspace(min(data_for_fit), max(data_for_fit), 10000)

    #이 케이스에서는 확률밀도함수의 종류는 1개로 한정지음 (최적의 1개를 선택했다고 가정)
    pdf_count = dist_res_arr.index(pdf_sort)
    distribution = generate_pdf(pdf_sort, dist_res['loc'][pdf_count], dist_res['scale'][pdf_count], dist_res['arg'][pdf_count])
    # range에 맞게 분포를 기준으로 확률밀도함수를 생성
    pdf = distribution.pdf(range)
    # 해당 내용으로 확률밀도함수를 플로팅
    plt.plot(range, pdf, label=pdf_sort)

    if point == True:
        # 지정된 건물을 표기
        # PK-code 11140-185 건물(서소문청사)
        print(data)
        PK = '11140-185'
        highlight_data = data.iloc[data.index.tolist().index('11140-185')]  #PK변수로 줄 경우 pandas에서 에러가 발생하여, 부득이하게 하드코딩함.
        print('Result for ' + str(PK))
        print(data.iloc[data.index.tolist().index('11140-185')])    #PK변수로 줄 경우 pandas에서 에러가 발생하여, 부득이하게 하드코딩함.

        plt.axvline(x=highlight_data['total_converged_EUI'], color='red', label='point for ' + str(PK))
        #percentile = distribution.expect(highlight_data['total_converged_EUI'])
        #percentile = sp.stats.rv_continuous.expect(distribution, lb=highlight_data['total_converged_EUI'], ub=2000)
        percentile = distribution.pdf(highlight_data['total_converged_EUI'])
        print(percentile)
        plt.text(highlight_data['total_converged_EUI'], 0.01, ' ' + str(round(percentile, 4)*100)[0:5] + ' % (probability)', fontsize=10)

    # 배경 히스토그램
    plt.hist(data_for_fit, bins=100, range=(min(data_for_fit), max(data_for_fit)), density=True, color='lightgrey')

    # 최종 출력
    plt.legend()
    plt.title('Histogram and PDF')
    if show == True:
        plt.show()
    if save == True:
        plt.savefig('PDF_percentile_' + '(' + pdf_sort + '_' + second_label + ')' + '.png')

    # 플롯 초기화
    plt.clf()

    # 누적분포함수 작성
    cdf = distribution.cdf(range)

    # 해당 내용으로 누적분포함수를 플로팅
    plt.plot(range, cdf, label=pdf_sort + '_cumulative')

    if point == True:
        # 지정된 건물을 표기
        # PK-code 11140-185 건물(서소문청사)
        PK = '11140-185'
        highlight_data = data.iloc[data.index.tolist().index('11140-185')]  #PK변수로 줄 경우 pandas에서 에러가 발생하여, 부득이하게 하드코딩함.
        print('Result for ' + str(PK))
        print(data.iloc[data.index.tolist().index('11140-185')])    #PK변수로 줄 경우 pandas에서 에러가 발생하여, 부득이하게 하드코딩함.

        plt.axvline(x=highlight_data['total_converged_EUI'], color='red', label='point for 11140-185')
        #percentile = cdf.expect(highlight_data['total_converged_EUI'])
        percentile = distribution.cdf(highlight_data['total_converged_EUI'])
        print(percentile)
        plt.text(highlight_data['total_converged_EUI'], 0.5, ' ' + str(round(percentile, 4)*100) + ' % (cumulative)', fontsize=10)

    # 배경 히스토그램
    #plt.hist(data_for_fit, bins=100, range=(0, 2000), density=True, Cumulative=True, color='lightgrey')

    # 최종 출력
    plt.legend()
    plt.title('Histogram and CDF for Cumulative percentile')
    if show == True:
        plt.show()
    if save == True:
        plt.savefig('CDF_percentile_' + '(' + pdf_sort + '_' + second_label + ')' + '.png')

    # 플롯 초기화
    plt.clf()

def data_fitting_allpurposes(data, label, dist_res, pdf_sorts, second_label=''):
    '''# 시설분류를 영문으로 전환 (폰트가 깨져서...)
    if second_label != '':
        second_label = facility_kor_to_eng(second_label)'''

    # distifit 라이브러리의 결과에서 분포의 종류를 리스트로 바꿔 저장함 (분포명에 맞는 loc, scale을 가져오기 위함)
    dist_res_arr = dist_res['distr'].tolist()

    # 데이터 라벨로 데이터를 배열로 바꿈
    data_for_fit = data[label].values

    # 범위 설정. 데이터의 최소-최대 값 기준에 resolution은 10000.
    range = np.linspace(min(data_for_fit), max(data_for_fit), 10000)

    #새로 바뀐 타입별 확률밀도함수 생성 코드
    for pdf_sort in pdf_sorts:
        pdf_count = dist_res_arr.index(pdf_sort)
        print(pdf_count)
        data_for_fit = data[label].values
        print(dist_res['loc'][pdf_count])
        print(dist_res['scale'][pdf_count])
        distribution = generate_pdf(pdf_sort, dist_res['loc'][pdf_count], dist_res['scale'][pdf_count], dist_res['arg'][pdf_count])

        # range에 맞게 분포를 기준으로 확률밀도함수를 생성
        pdf = distribution.pdf(range)

        # 해당 내용으로 확률밀도함수를 플로팅
        plt.plot(range, pdf, label=second_label)

def get_fit_matrix(sort='normal'):

    if sort=='normal':
        fit_list = {
        "":"beta",
        "공동주택":"t",
        "공장":"t",
        "관광휴게시설":"모수부족",
        "교육연구시설":"beta",
        "교정및군사시설":"모수부족",
        "노유자시설":"t",
        "단독주택":"beta",
        "동.식물관련시설":"모수부족",
        "묘지관련시설":"모수부족",
        "문화및집회시설":"t",
        "발전시설":"모수부족",
        "방송통신시설":"모수부족",
        "수련시설":"모수부족",
        "숙박시설":"t",
        "야영장시설":"모수부족",
        "업무시설":"t",
        "운동시설":"t",
        "운수시설":"모수부족",
        "위락시설":"beta",
        "위험물저장및처리시설":"beta",
        "의료시설":"t",
        "자동차관련시설":"beta",
        "자원순환관련시설":"모수부족",
        "장례식장":"모수부족",
        "제1종근린생활시설":"beta",
        "제2종근린생활시설":"beta",
        "종교시설":"t",
        "창고시설":"t",
        "판매시설":"beta"
        }
    elif sort == 'excluded':
        #best fit에서 모수부족분을 제외한 것.
        fit_list = {
        "":"beta",
        "공동주택":"t",
        "공장":"t",
        "교육연구시설":"beta",
        "노유자시설":"t",
        "단독주택":"beta",
        "문화및집회시설":"t",
        "숙박시설":"t",
        "업무시설":"t",
        "운동시설":"t",
        "위락시설":"beta",
        "위험물저장및처리시설":"beta",
        "의료시설":"t",
        "자동차관련시설":"beta",
        "제1종근린생활시설":"beta",
        "제2종근린생활시설":"beta",
        "종교시설":"t",
        "창고시설":"t",
        "판매시설":"beta"
        }
    else:
        print('Error: Element is not correct // use one of [normal|excluded]')
        #에러가 나도록 빈 dict를 반환
        fit_list = {}

    return fit_list


def plot_fitting_comparison(fit_matrix, data, show=True, save=False, second_label=''):
    final_data = data[['USEAPR_DAY', 'MAIN_PURPS_NM', 'total_converged_EUI']]
    # 건축물종류별 비교를 위한 것
    sort_list = fit_matrix.keys()
    for purpose in sort_list:
        sample_data = final_data[(data['MAIN_PURPS_NM'] == purpose)]
        fit_result = data_fitting(sample_data, 'total_converged_EUI')
        # 이 부분에서 그래프를 n^2번 겹쳐 그리는 듯 한데...(문제는 없음) 나중에 확인.
        data_fitting_allpurposes(sample_data, 'total_converged_EUI', fit_result, [fit_matrix[purpose]], second_label=purpose)

    plt.legend()
    plt.title('Comparison of each PDF on purpose')

    if show == True:
        plt.show()
    if save == True:
        plt.savefig('pdfhist_' + '(all_pdf_comparison_' + second_label + ')' + '.png')

    # 플롯 초기화
    plt.clf()

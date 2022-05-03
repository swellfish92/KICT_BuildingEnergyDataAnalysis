import pandas as pd
import os
import scipy as sp
import scipy.stats

from functions import *

# 레이블에 해당하는 내용만을 CSV에서 읽어와 반환함.
def read_csv_labels(filedir, labels):
    data = pd.read_csv(filedir)
    return data[labels]

# 파일의 모든 레이블을 반환함
def read_csv_label(filedir):
    data = pd.read_csv_labels(filedir)
    print('return labels(columns) of the ' + str(filedir) + 'as below')
    print(data.columns.tolist())
    return data.columns.tolist()


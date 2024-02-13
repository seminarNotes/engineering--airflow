import FinanceDataReader as fdr
import numpy as npfdr
import pandas as pd

from datetime import datetime

import os
import shutil

from seminar.task_config import MAIN_PATH
from seminar.task_database import capsule_insert_data_stockprice

from seminar.task_config import HEAD_complete
from seminar.task_config import HEAD_fail

def extract_stock_price(ticker, date_begin, date_end) :
    PATH = MAIN_PATH + r"extract_data"

    df = fdr.DataReader(ticker, date_begin, date_end)

    if not os.path.exists(PATH):
        os.makedirs(PATH)

    if os.path.exists(PATH + r"/rawStock_%s.csv" %ticker) :
        shutil.move(PATH + r"/rawStock_%s.csv" %ticker,
                    PATH + r"/rawStock_%s_old%s.csv" %(ticker, datetime.now().strftime("%Y%m%d%H%M%S"))
                    )
        
    df.to_csv(PATH + r"/rawstock_%s.csv" %ticker)

def transform_stock_price(ticker, date_begin, date_end) :
    """(T)transform
    1. 데이터 정제(Cleaning): 불완전하거나 잘못된 데이터를 처리하고, 결측값을 다루며, 이상치를 제거하거나 대체.

    2. 데이터 변환(Transforming): 데이터의 형식을 변경하거나 조정하여 분석이나 모델링에 적합 변환.
                                예를 들어, 날짜 형식의 변환, 범주형 데이터의 인코딩, 스케일링 등.

    3. 집계 및 요약(Aggregation and Summarization): 필요에 따라 데이터를 집계하거나 요약.

    4. 특성 생성(Feature Engineering): 새로운 특성을 생성하거나 기존의 특성을 변환.

    5. 데이터 통합(Integration): 다양한 데이터 소스에서 가져온 데이터를 통합"""

    cols_of_load = ['Date', 'High', 'Low', 'Close', 'Volume']
    cols_of_save = ['Date', 'Mid', 'Close', 'Volume']
    
    PATH = MAIN_PATH + r"extract_data"

    df = pd.read_csv(PATH + r"/rawStock_%s.csv" %ticker)[cols_of_load]

    # df['Date'] : string -> datetime
    df['Date'] =  pd.to_datetime(df['Date'])
    
    # Date가 '2000-01-01' 이전 혹은 datetime.now() 이후인 데이터 필터
    df = df[(df['Date'] >= pd.to_datetime('2000-01-01')) & (df['Date'] < datetime.now())]

    # Date가 입력한 날싸 사이로 필터
    df = df[(df['Date'] >= pd.to_datetime(date_begin)) & (df['Date'] < pd.to_datetime(date_end))]

    # Date가 Null인 데이터 필터
    df = df[~df['Date'].isnull()]

    # High 가격보다 Low 가격이 높은 데이터 필터
    df = df[df['Low'] <= df['High']]

    # High, Low, Close 중 하나라도 Null 값이면, 전날 High, Low, Close의 데이터를 복사해서 입력
    df[['High', 'Low', 'Close']] = df[['High', 'Low', 'Close']].fillna(method='ffill')

    # df['Date'] : datetime -> string
    df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')

    # create Column : df['Mid']
    df['Mid'] = (df['High'] + df['Low']) * 0.5

    df = df[cols_of_save]

    PATH = MAIN_PATH + r"transform_data"

    if not os.path.exists(PATH):
        os.makedirs(PATH)

    if os.path.exists(PATH + r"/Stock_%s.csv" %ticker) :
        shutil.move(PATH + r"/Stock_%s.csv" %ticker,
                    PATH + r"/Stock_%s_old%s.csv" %(ticker, datetime.now().strftime("%Y%m%d%H%M%S"))
                    )
        
    df.to_csv(PATH + r"/Stock_%s.csv" %ticker)

    if False :
        calculate_ewma_volatility(ticker)

def calculate_ewma_volatility(ticker, vol_days = 250, ewma_lambda = 0.94, price = 'Mid') :
    year_scaler = np.sqrt(252)

    cols_of_load = ['Date', 'Mid', 'Close', 'Volume']

    PATH = MAIN_PATH + r"transform_data"

    df = pd.read_csv(PATH + r"/Stock_%s.csv" %ticker)[cols_of_load]

    if price == 'Mid' :
        df['Price'] = df.Mid

    elif price == 'Close' :
        df['Price'] = df.Close

    df['return'] = (df.Price - df.Price.shift(1)) / df.Price.shift(1)

    # 고정 기간 변동성 계산
    vol_colname = 'vol_' + str(vol_days)
    df[vol_colname] = year_scaler * df['return'].rolling(window=vol_days).std()

    # EWMA 변동성 계산 (Lambda 사용)
    tolerance_dim = -8
    cnt_weight = int(tolerance_dim / np.log10(ewma_lambda) + 1)
    weight = (1 - ewma_lambda) * ewma_lambda ** np.arange(cnt_weight)
    weight = weight[::-1]
    df['return_shifted'] = df['return'].copy().shift(1)
    df['ewma_vol'] = np.sqrt(df['return_shifted'].rolling(cnt_weight).apply(lambda x: np.sum(weight * x ** 2))) * year_scaler

    return None

def load_stock_price(ticker, date_begin, date_end) :
    cols_of_load = ['Date', 'Mid', 'Close']

    PATH = MAIN_PATH + r"transform_data"

    df = pd.read_csv(PATH + r"/Stock_%s.csv" %ticker)[cols_of_load]

    capsule_insert_data_stockprice(ticker, df)

def capsule_extract_stock_price(ticker, date_begin, date_end) :
    try :
        extract_stock_price(ticker, date_begin, date_end)
        print (HEAD_complete + " extract_stock_price")
    except :
        print (HEAD_fail + " extract_stock_price")
    
def capsule_transform_stock_price(ticker, date_begin, date_end) :
    try :
        transform_stock_price(ticker, date_begin, date_end)
        print (HEAD_complete + " transform_stock_price")
    except :
        print (HEAD_fail + " transform_stock_price")


def capsule_load_stock_price(ticker, date_begin, date_end) :
    try :
        load_stock_price(ticker, date_begin, date_end)
        print (HEAD_complete + " load_stock_price")
    except :
        print (HEAD_fail + " load_stock_price")




if __name__ == '__main__' :
    ticker = 'AAPL'
    date_begin = '2013-01-01'
    date_end = '2020-03-01'

    # extract_stock_price(ticker, date_begin, date_end)

    # transform_stock_price(ticker, date_begin, date_end)

    #calculate_ewma_volatility(ticker, vol_days = 250, ewma_lambda = 0.94)

    load_stock_price(ticker, date_begin, date_end)






import mysql.connector
import pandas as pd
from datetime import datetime
from itertools import product


from seminar.task_config import PASSWORD
from seminar.task_config import DATABASE

from seminar.task_config import HEAD
from seminar.task_config import HEAD_E
from seminar.task_config import HEAD_complete
from seminar.task_config import HEAD_fail
import time

def connect_mysql() :
    con = mysql.connector.connect(
        host = "localhost",
        user = "airflow",
        password = PASSWORD,
        database = DATABASE
    )
    return con

def create_table_mysql(table_name, column_name, column_type) :
    SQL_CREATE_TABLE = "CREATE TABLE IF NOT EXISTS %s (" % table_name
    
    for idx in range(len(column_name)) :
        SQL_CREATE_TABLE += "%s %s" %(column_name[idx], column_type[idx])
        if idx == 0 :
            SQL_CREATE_TABLE += "PRIMARY KEY, "
        elif idx == range(len(column_name))[-1] :
            SQL_CREATE_TABLE += ")"
        else :
            SQL_CREATE_TABLE += ", "

    with connect_mysql() as con:
        with con.cursor() as cur:
            cur.execute(SQL_CREATE_TABLE)
            con.commit()        
    # print (SQL_CREATE_TABLE)
            

def check_table_existence(table_name) :
    SQL_CHECK_TABLE = """SHOW TABLES LIKE '%s'""" % table_name

    with connect_mysql() as con:
        with con.cursor() as cur:
            cur.execute(SQL_CHECK_TABLE)
            result = cur.fetchall()

    if len(result) == 0:
        return False
    else :
        return True
    
    
def create_table_stockprice() :
    SQL_CREATE_TABLE = """CREATE TABLE TB_STOCK_PRICE (
                        DATE_MARKET VARCHAR(20),
                        TICKER VARCHAR(20),
                        MID FLOAT,
                        CLO FLOAT,
                        DATE_UPDATE DATETIME,
                        PRIMARY KEY (DATE_MARKET, TICKER)
    )"""
    with connect_mysql() as con:
        with con.cursor() as cur:
            cur.execute(SQL_CREATE_TABLE)
            con.commit()    

def create_table_tasklist() :
    SQL_CREATE_TABLE = """CREATE TABLE IF NOT EXISTS TB_TASK_LIST (
                        CODE_TASK VARCHAR(20),
                        EPOCH INT,
                        BATCH_SIZE INT,
                        LEARNING_RATE FLOAT,
                        RATIO_TRAIN_SET FLOAT,
                        RATIO_VALID_SET FLOAT,
                        PERIOD_PREDICTION INT,
                        SIZE_SEQUENCE INT,
                        SIZE_LAYERS INT,
                        SIZE_UNITS_INPUT INT,
                        SIZE_UNITS_HIDDEN INT,
                        SIZE_UNITS_OUTPUT INT,
                        DATE_UPDATE DATETIME,
                        PRIMARY KEY (CODE_TASK)   
    )"""
    with connect_mysql() as con:
        with con.cursor() as cur:
            cur.execute(SQL_CREATE_TABLE)
            con.commit() 

def insert_data_stockprice(ticker, df) :
    SQL_INSERT_DATA = """INSERT INTO TB_STOCK_PRICE
                        (DATE_MARKET, TICKER, MID, CLO, DATE_UPDATE)
                        VALUES
                        ('%s', '%s',%f, %f, NOW())"""
    
    with connect_mysql() as con:
        with con.cursor() as cur:
            for row in df.values :
                try :
                    SQL_INSERT = SQL_INSERT_DATA %(str(row[0]),
                                               #datetime.date(index).strftime('%Y-%m-%d'),
                                               ticker,
                                               float(row[1]), 
                                               float(row[2])
                                               )
                    cur.execute(SQL_INSERT)
                    con.commit()

                except Exception as e:
                    print (str(e))

def select_data_stockprice(ticker, date_begin, date_end) :
    SQL_SELECT_DATA = """SELECT DATE_MARKET, MID, CLO FROM TB_STOCK_PRICE 
                        WHERE TICKER = %s AND DATE_MARKET >= %s AND DATE_MARKET < %s"""
    with connect_mysql() as con:
        with con.cursor() as cur:
            cur.execute(SQL_SELECT_DATA, (ticker, date_begin, date_end, ))
            result_fetch = cur.fetchall()
    
    col_date, col_mid, col_clo = [], [], []
    for row in result_fetch :  
        col_date.append(str(row[0]))
        col_mid.append(float(row[1]))
        col_clo.append(float(row[2]))


    # DataFrame 생성
    data = {
        'Date' : col_date,
        'Mid' : col_mid,
        'Close' : col_clo,
    }

    df = pd.DataFrame(data)
    return df

def insert_data_tasklist() :
    SQL_INSERT_DATA = """INSERT INTO TB_TASK_LIST
                        (CODE_TASK, EPOCH, BATCH_SIZE, LEARNING_RATE,
                        RATIO_TRAIN_SET, RATIO_VALID_SET, PERIOD_PREDICTION,
                        SIZE_SEQUENCE, SIZE_LAYERS, SIZE_UNITS_INPUT,
                        SIZE_UNITS_HIDDEN, SIZE_UNITS_OUTPUT, DATE_UPDATE)
                        VALUES
                        ('%s', %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, NOW())
                        """
                        
    list_epoch = [10, 20, 30]
    list_batch_size = [5, 10, 20]
    list_learning_rate = [0.005, 0.01, 0.2]
    list_ratio_train_set = [0.7, 0.8, 0.9]
    list_ratio_valid_set = [0.05, 0.1, 0.15]
    list_period_prediction = [1]
    list_size_sequence = [50]

    input_size_layers = [3]
    input_size_units_input = [32, 50, 64]
    input_size_units_hidden = [64, 128]
    input_size_units_output = [1]

    
    cartesian_product = list(product(list_epoch,
                                     list_batch_size,
                                     list_learning_rate,
                                     list_ratio_train_set,
                                     list_ratio_valid_set,
                                     list_period_prediction,
                                     list_size_sequence,
                                     input_size_layers,
                                     input_size_units_input,
                                     input_size_units_hidden,
                                     input_size_units_output
                                     ))
    with connect_mysql() as con:
        with con.cursor() as cur:
            idx = 0
            for row in cartesian_product :
                idx += 1
                task_number = f"{idx:04}" 
                try :
                    SQL_INSERT = SQL_INSERT_DATA %("taskcode" + task_number,
                                                    float(row[0]),
                                                    float(row[1]),
                                                    float(row[2]),
                                                    float(row[3]),
                                                    float(row[4]),
                                                    float(row[5]),
                                                    float(row[6]),
                                                    float(row[7]),
                                                    float(row[8]),
                                                    float(row[9]),
                                                    float(row[10])
                    )                           
                    cur.execute(SQL_INSERT)
                    con.commit()

                except Exception as e:
                    print (str(e))

def select_data_tasklist() :
    # SQL_SELECT_DATA = SELECT * FROM your_table WHERE your_column LIKE '특정글자%';"""
    SQL_SELECT_DATA = """SELECT 
                        CODE_TASK, EPOCH, BATCH_SIZE, LEARNING_RATE,
                        RATIO_TRAIN_SET, RATIO_VALID_SET, PERIOD_PREDICTION,
                        SIZE_SEQUENCE, SIZE_LAYERS, SIZE_UNITS_INPUT,
                        SIZE_UNITS_HIDDEN, SIZE_UNITS_OUTPUT
                        FROM TB_TASK_LIST
                        WHERE 1=1
                        ORDER BY CODE_TASK ASC
                        """
    
    with connect_mysql() as con:
        with con.cursor() as cur:
            cur.execute(SQL_SELECT_DATA)
            result_fetch = cur.fetchall()
    
    return result_fetch


def create_table_modelscore() :
    SQL_CREATE_TABLE = """CREATE TABLE IF NOT EXISTS TB_MODEL_SCORE (
                        CODE_TASK VARCHAR(20),
                        TICKER VARCHAR(20),
                        LOSS FLOAT,
                        ACCURACY FLOAT,
                        DATE_UPDATE DATETIME,
                        PRIMARY KEY (CODE_TASK, TICKER)   
    )"""
    with connect_mysql() as con:
        with con.cursor() as cur:
            cur.execute(SQL_CREATE_TABLE)
            con.commit() 

def create_table_modelprice() :
    SQL_CREATE_TABLE = """CREATE TABLE IF NOT EXISTS TB_MODEL_PRICE (
                        CODE_TASK VARCHAR(20),
                        TICKER VARCHAR(20),
                        SEQ INT,
                        Y_REAL FLOAT,
                        Y_PRED FLOAT,
                        DATE_UPDATE DATETIME,
                        PRIMARY KEY (CODE_TASK, TICKER, SEQ)   
    )"""
    with connect_mysql() as con:
        with con.cursor() as cur:
            cur.execute(SQL_CREATE_TABLE)
            con.commit() 

def insert_data_modelscore(code_task, ticker, loss, accuracy) :

    SQL_INSERT_DATA = """INSERT INTO TB_MODEL_SCORE
                        (CODE_TASK, TICKER, LOSS, ACCURACY, DATE_UPDATE)
                        VALUES
                        ('%s', '%s', %f, %f, NOW())"""
    
    with connect_mysql() as con:
        with con.cursor() as cur:
            try :
                SQL_INSERT = SQL_INSERT_DATA %(code_task,
                                               ticker,
                                               loss,
                                               accuracy
                                               )
                cur.execute(SQL_INSERT)
                con.commit()

            except Exception as e:
                print (str(e))

def insert_data_modelprice(code_task, ticker, y_real, y_pred) :

    SQL_INSERT_DATA = """INSERT INTO TB_MODEL_PRICE
                        (CODE_TASK, TICKER, SEQ, Y_REAL, Y_PRED, DATE_UPDATE)
                        VALUES
                        ('%s', '%s', %s, %f, %f, NOW())"""
    
    with connect_mysql() as con:
        with con.cursor() as cur:
            idx = 0
            for real, pred in zip(y_real, y_pred) :
                idx += 1
                try :
                    SQL_INSERT = SQL_INSERT_DATA %(code_task,
                                                ticker,
                                                idx,
                                                real,
                                                pred
                                                )
                    cur.execute(SQL_INSERT)
                    con.commit()

                except Exception as e:
                    print (str(e))

def delete_data_modelprice(ticker) :
    SQL_DELETE_DATA = """DELETE FROM TB_STOCK_PRICE WHERE TICKER = %s"""
    with connect_mysql() as con:
        with con.cursor() as cur:
            SQL_DELETE = SQL_DELETE_DATA %(ticker)            
            cur.execute(SQL_DELETE)
            con.commit()

def delete_data_modelscore(ticker) :
    SQL_DELETE_DATA = """DELETE FROM TB_STOCK_SCORE WHERE TICKER = %s"""
    with connect_mysql() as con:
        with con.cursor() as cur:
            SQL_DELETE = SQL_DELETE_DATA %(ticker)            
            cur.execute(SQL_DELETE)
            con.commit()


def capsule_select_data_stockprice(ticker, date_begin, date_end) :
    try :
        selected = select_data_stockprice(ticker, date_begin, date_end)
        print (HEAD_complete + " select_data_stockprice")
        return selected
    
    except :
        print (HEAD_fail + " select_data_stockprice")
        return None


def capsule_select_data_tasklist() :
    try :
        selected = select_data_tasklist()
        print (HEAD_complete + " elect_data_tasklist")
        return selected
    
    except :
        print (HEAD_fail + " elect_data_tasklist")
        return None

def capsule_insert_data_modelscore(code_task, ticker, loss, accuracy) :
    try :
        insert_data_modelscore(code_task, ticker, loss, accuracy)
        print (HEAD_complete + " insert_data_modelscore")
    except :
        print (HEAD_fail + " insert_data_modelscore")


def capsule_insert_data_modelprice(code_task, ticker, y_test, y_pred) :
    try :
        insert_data_modelprice(code_task, ticker, y_test, y_pred)
        print (HEAD_complete + " insert_data_modelprice")
    except :
        print (HEAD_fail + " insert_data_modelprice")


def capsule_insert_data_stockprice(ticker, df) :
    try :
        insert_data_stockprice(ticker, df)
        print (HEAD_complete + " insert_data_stockprice")
    except :
        print (HEAD_fail + " insert_data_stockprice")


def capsule_create_table() :
    # 필요한 데이터 테이블 생성

    if check_table_existence('TB_TASK_LIST') :
        print (HEAD + ' Table "TB_MODEL_SCORE already exists')
    else :
        create_table_tasklist()
        print (HEAD + ' Table "TB_MODEL_SCORE already created')
    time.sleep(0.5)

    if check_table_existence('TB_STOCK_PRICE') :
        print (HEAD + ' Table "TB_STOCK_PRICE already exists')
    else :
        create_table_stockprice()
        print (HEAD + ' Table "TB_STOCK_PRICE already created')
    time.sleep(0.5)

    if check_table_existence('TB_MODEL_PRICE') :
        print (HEAD + ' Table "TB_MODEL_PRICE already exists')
    else :
        create_table_modelprice()
        print (HEAD + ' Table "TB_MODEL_PRICE already created')
    time.sleep(0.5)
    
    if check_table_existence('TB_MODEL_SCORE') :
        print (HEAD + ' Table "TB_MODEL_SCORE already exists')
    else :
        create_table_modelscore()
        print (HEAD + ' Table "TB_MODEL_SCORE already created')
    time.sleep(0.5)


if __name__ == '__main__' :
    ticker = 'AAPL'
    date_begin = '2013-01-01'
    date_end = '2020-03-01'
    select_data_stockprice(ticker, date_begin, date_end)


    if False :
        delete_data_modelprice(ticker)
        delete_data_modelscore(ticker)
        create_table_stockprice()
        create_table_tasklist()
        create_table_modelscore()
        create_table_modelprice()

    # print (check_table_existence('TB_TASK_LIST'))
    # insert_data_tasklist()
    # select_data_tasklist('AAPL')
        



    

    
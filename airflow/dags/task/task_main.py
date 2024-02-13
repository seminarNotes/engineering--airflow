from task_database import capsule_create_table
from task_ETL import capsule_extract_stock_price
from task_ETL import capsule_transform_stock_price
from task_ETL import capsule_load_stock_price
from task_model import capsule_train_model

if __name__ == '__main__' :
    ticker = 'AAPL'
    date_begin = '2013-01-01'
    date_end = '2020-03-01'

    capsule_create_table()

    capsule_extract_stock_price(ticker, date_begin, date_end)

    capsule_transform_stock_price(ticker, date_begin, date_end)

    capsule_load_stock_price(ticker, date_begin, date_end)

    capsule_train_model(ticker, date_begin, date_end)



    
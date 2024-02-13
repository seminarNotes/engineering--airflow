
from datetime import datetime, timedelta

from airflow import DAG

from airflow.operators.bash import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.utils.trigger_rule import TriggerRule

import sys, os
sys.path.append(os.getcwd())

## 추가한 부분
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.abspath(current_dir + "/../"))
##

# from MLproject.titanic import *

from seminar.task_database import capsule_create_table
from seminar.task_ETL import capsule_extract_stock_price
from seminar.task_ETL import capsule_transform_stock_price
from seminar.task_ETL import capsule_load_stock_price
from seminar.task_model import capsule_train_model

# titanic = TitanicMain()

def print_result(**kwargs):
    r = kwargs["task_instance"].xcom_pull(key='result_msg')
    print("message : ", r)

# 실행할 Python 함수
def my_python_function():
    print("Hello, Airflow!")

default_args = {
    'owner': 'owner-name',
    'depends_on_past': False,
    'email': ['your-email@g.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

dag_args = dict(
    dag_id="seminar",
    default_args=default_args,
    description='For woorifisa seminar',
    schedule_interval=timedelta(days=7),
    start_date=datetime(2023, 12, 1),
    tags=['example'],
)

with DAG( **dag_args ) as dag: # 각 task 정의
    start = BashOperator(
        task_id='start',
        bash_command='echo "start!"',
    )
    # PythonOperator를 사용하여 Task 정의
    # run_this_first = PythonOperator(
    #     task_id='run_this_first',
    #     python_callable=my_python_function,
    #     dag=dag,
    # )

    create_table = PythonOperator(
        task_id='create_table',
        python_callable = capsule_create_table,
    )
    
    extract_stock_price = PythonOperator(
        task_id='E',
        python_callable = capsule_extract_stock_price,
        op_kwargs={'ticker':'AAPL', 'date_begin':'2013-01-01', 'date_end':'2020-03-01'}
    )

    transform_stock_price = PythonOperator(
        task_id='T',
        python_callable = capsule_transform_stock_price,
        op_kwargs={'ticker':'AAPL', 'date_begin':'2013-01-01', 'date_end':'2020-03-01'}
    )

    load_stock_price = PythonOperator(
        task_id='L',
        python_callable = capsule_load_stock_price,
        op_kwargs={'ticker':'AAPL', 'date_begin':'2013-01-01', 'date_end':'2020-03-01'}
    )

    train_model = PythonOperator(
        task_id='train_model',
        python_callable = capsule_train_model,
        op_kwargs={'ticker':'AAPL', 'date_begin':'2013-01-01', 'date_end':'2020-03-01'}
    )

    complete = BashOperator(
        task_id='complete_bash',
        bash_command='echo "complete~!"',
    )

    start >>  create_table >> extract_stock_price >> transform_stock_price >> load_stock_price >> train_model >> complete



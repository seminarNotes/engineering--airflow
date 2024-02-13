
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

from new_seminar_1226.task01_Initialize import capsule_initialize_setting
from new_seminar_1226.task02_Extracte import extract_stock_price
from new_seminar_1226.task03_Transform_Load import capsule_transform_load_stock_price
from new_seminar_1226.task04_Model_Train import capsule_process1
from new_seminar_1226.task05_Model_Train import capsule_process2

default_args = {
    'owner': 'Seongwook',
    'depends_on_past': False,
    'email': ['your-email@g.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

dag_args = dict(
    dag_id="Machine_Learning_Pipeline",
    default_args=default_args,
    description='For woorifisa seminar',
    schedule_interval=timedelta(days=7),
    start_date=datetime(2024, 1, 1),
    tags=['ML-pipeline'],
)

ticker = 'AAPL'
date_begin = '2013-01-01'
date_end = '2020-03-01'

with DAG( **dag_args, catchup=False ) as dag: # 각 task 정의

    t_capsule_initialize_setting = PythonOperator(
        task_id='task1_Create_table',
        python_callable = capsule_initialize_setting,
    )
    
    t_extract_stock_price = PythonOperator(
        task_id='task2_Extract',
        python_callable = extract_stock_price,
        op_kwargs={'ticker':ticker, 'date_begin':date_begin, 'date_end':date_end}
    )

    t_capsule_transform_load_stock_price = PythonOperator(
        task_id='task3_Transform_Load',
        python_callable = capsule_transform_load_stock_price,
        op_kwargs={'ticker':ticker, 'date_begin':date_begin, 'date_end':date_end}
    )

    t_capsule_process1 = PythonOperator(
        task_id='task4_Train_model1',
        python_callable = capsule_process1,
        op_kwargs={'ticker':ticker, 'date_begin':date_begin, 'date_end':date_end}
    )

    t_capsule_process2 = PythonOperator(
        task_id='task5_Train_model2',
        python_callable = capsule_process2,
        op_kwargs={'ticker':ticker, 'date_begin':date_begin, 'date_end':date_end}
    )

    t_capsule_initialize_setting >> t_extract_stock_price >> \
        t_capsule_transform_load_stock_price >> [t_capsule_process1, t_capsule_process2]



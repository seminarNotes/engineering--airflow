
import datetime
import time
import pendulum

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import BranchPythonOperator
from airflow.utils.trigger_rule import TriggerRule

def random_branch_path() :
    from random import randint
    return "path1" if randint(1, 2) == 1 else "path2"



with DAG( 
    dag_id = "dag_practice1",
    schedule = "00 00 * * *", # 분 시 일 월 요일
    start_date = pendulum.datetime(2023, 12, 26, tz = "Asia/Seoul")
) as dag:

    task_1 = BashOperator(
        task_id = 'task_1',
        bash_command = 'date'
    )    

    task_2 = BranchPythonOperator(
        task_id = 'task2',
        python_callable = random_branch_path,
    )

    task_3 = BashOperator(
        task_id = 'task_3',
        depends_on_past = False,
        bash_command = 'echo "안녕하세요"'
    )

    task_4 = BashOperator(
        task_id = 'task_4',
        depends_on_past = False,
        bash_command = 'echo "Hello"'
    )

    task_5 = BashOperator(
        task_id = 'task_5',
        depends_on_past = False,
        bash_command = 'echo "complete"',
        trigger_rule = TriggerRule.NONE_FAILED
    )
    
    task_dummy = DummyOperator(task_id = 'path1')

    task_1 >> task_2 >> task_dummy >> task_3 >> task_5
    task_1 >> task_2 >> task_4 >> task_5



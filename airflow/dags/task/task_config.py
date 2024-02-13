import os
from datetime import datetime

PASSWORD = "airflow"

DATABASE = "airflow"

PATH = os.getcwd().split('\\') # 리눅스에서는 // ?

MAIN_PATH = r''
for ii in range(len(PATH)) :
    MAIN_PATH += str(PATH[ii] + r'/') 

HEAD =  "[NOTE][%s]" %datetime.now().strftime("%Y%m%d")
HEAD_E =  "[ERRO][%s]" %datetime.now().strftime("%Y%m%d")

HEAD_complete = HEAD + " Completed to execute function"
HEAD_fail = HEAD + " Failed to execute function"
    
    



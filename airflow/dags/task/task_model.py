import FinanceDataReader as fdr
import numpy as np
import pandas as pd

from datetime import datetime

import os
import shutil

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam

from seminar.task_config import MAIN_PATH
from seminar.task_config import HEAD_complete
from seminar.task_config import HEAD_fail

from seminar.task_database import capsule_select_data_stockprice
from seminar.task_database import capsule_select_data_tasklist
from seminar.task_database import capsule_insert_data_modelscore
from seminar.task_database import capsule_insert_data_modelprice
 
def build_model(*args) :
    ticker, date_begin, date_end, category_model, \
    input_epoch, input_batch_size, input_learning_rate, \
    input_ratio_train_set, input_ratio_valid_set, input_period_prediction, \
    input_size_sequence, input_size_layers, \
    input_size_units_input, input_size_units_hidden, input_size_units_output, \
    stock_price = args

    # Compute Mid Price
    price_close = stock_price['Close'].values
    price_mid = stock_price['Mid'].values
  
    # Create Window
    size_window = input_size_sequence + 1

    price_windowed = []
    price_windowed_normalized = []
    for index in range(len(price_mid) - size_window):
        price_windowed.append(price_mid[index: index + size_window])

    for window in price_windowed:
        window_normalized = [((float(p) / float(window[0])) - 1) for p in window]
        price_windowed_normalized.append(window_normalized)

    price_windowed_normalized_numpyed = np.array(price_windowed_normalized)

    # split train and test data
    number_division = int(round(price_windowed_normalized_numpyed.shape[0] * input_ratio_train_set))
    dataset_train = price_windowed_normalized_numpyed[:number_division, :]
    np.random.shuffle(dataset_train)

    X_train = dataset_train[:, :-1]
    X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))
    y_train = dataset_train[:, -1]

    X_test = price_windowed_normalized_numpyed[number_division:, :-1]
    X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
    y_test = price_windowed_normalized_numpyed[number_division:, -1]


    # LSTM model
    model = Sequential()
    if input_size_layers == 2:
        print (["구현되지 않음"])
        return None
        model.add(LSTM(input_size_units_input,
                    input_shape=(X_train.shape[1], X_train.shape[2]), 
                    return_sequences = True))
        model.add(LSTM(input_size_units_output,
                    return_sequences = False))
        model.add(Dense(y_train.shape[1]))
        optimizer = Adam(learning_rate = input_learning_rate)
        model.compile(optimizer = optimizer,
                loss = 'mse')

    elif input_size_layers == 3 :
        model = Sequential()
        model.add(LSTM(input_size_units_input,
                       return_sequences = True,
                       input_shape = (input_size_sequence, 1))
                       )
        model.add(LSTM(input_size_units_hidden,
                       return_sequences = False)
                       )
        model.add(Dense(input_size_units_output,
                        activation = 'linear')
                        )
        model.compile(loss = 'mse',
                      optimizer = 'rmsprop',
                      metrics = ["accuracy"]
                      )
        model.summary()

    history = model.fit(X_train,
                        y_train,
                        validation_data = (X_test, y_test),
                        batch_size = input_batch_size,
                        epochs = input_epoch
                        )
       
    results = model.evaluate(X_test, y_test)
    y_pred  = model.predict(X_test)
    loss    = results[0]
    acc     = results[1] 
    
    return (loss, acc, y_test, y_pred)

    
def train_model(ticker, date_begin, date_end) :
    
    set_data = capsule_select_data_stockprice(ticker, date_begin, date_end)
    
    set_parameters = capsule_select_data_tasklist()

    print (1)
    for parameter in set_parameters :
        code_task               = parameter[0]
        input_epoch             = parameter[1]
        input_batch_size        = parameter[2]
        input_learning_rate     = parameter[3]
        input_ratio_train_set   = parameter[4]
        input_ratio_valid_set   = parameter[5]
        input_period_prediction = parameter[6]
        input_size_sequence     = parameter[7]
        input_size_layers       = parameter[8]
        input_size_units_input  = parameter[9]
        input_size_units_hidden = parameter[10]
        input_size_units_output = parameter[11]
                         
        (loss, accuracy, y_pred, y_test) = build_model(ticker,
                                        date_begin,
                                        date_end,
                                        'LSTM',
                                        input_epoch,
                                        input_batch_size,
                                        input_learning_rate,
                                        input_ratio_train_set,
                                        input_ratio_valid_set,
                                        input_period_prediction,
                                        input_size_sequence,
                                        input_size_layers,
                                        input_size_units_input,
                                        input_size_units_hidden,
                                        input_size_units_output,
                                        set_data
                                        )

        capsule_insert_data_modelscore(code_task, ticker, loss, accuracy)
        capsule_insert_data_modelprice(code_task, ticker, y_test, y_pred)

def capsule_train_model(ticker, date_begin, date_end) :
    try :
        train_model(ticker, date_begin, date_end)
        print (HEAD_complete + " train_model")
    except :
        print (HEAD_fail + " train_model")


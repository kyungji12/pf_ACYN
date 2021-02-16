import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
# from xgboost import XGBClassifier
# from xgboost import plot_importance

import pickle

class Model():
    def __init__(self):
        self.loaded_model = pickle.load(open("static/upt_model.pickle.dat", "rb"))

    # def make_data(self,df_data):
    def make_data(input_data):
        input_data = input_data[0]
        
        varX = []
        varY = []
        for i in range(len(input_data)):
            if i == 0:
                varX.append(input_data[i])
            elif i % 2 == 0:
                varX.append(input_data[i])
            else :
                varY.append(input_data[i])

        varX = pd.DataFrame(varX)
        varY = pd.DataFrame(varY) 

        output_data = pd.concat([varX, varY], ignore_index = True)  
        output_data = output_data.transpose()

        return output_data

    def predict(data):
        # result = self.make_data(data)
        y_pred = self.loaded_model.predict(data)
        predictions = [round(value) for value in y_pred]
        return predictions
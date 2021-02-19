import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from xgboost import XGBClassifier
from xgboost import plot_importance
import os
import pickle

class Model():
    def __init__(self):
        modulePath = os.path.dirname(__file__)
        # print("🌷",modulePath) # /Users/yooni/Desktop/archive/UPT_dev/UPTproject/pose_app
        filePath = os.path.join(modulePath, 'static/upt_model.pickle.dat')
        with open(filePath, 'rb') as f:
            obj = pickle.load(f)
        # self.loaded_model = pickle.load(open("../upt_model.pickle.dat", "rb"))
            self.loaded_model = obj

    # def make_data(self,df_data):
    def make_data(self, input_data):
        print(input_data)
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

        columns = ['nose_x', 'leftEye_x', 'rightEye_x', 'leftEar_x', 'rightEar_x', 'leftShoulder_x', 'rightShoulder_x', 'leftElbow_x', 'rightElbow_x', 'leftWrist_x', 'rightWrist_x', 'leftHip_x', 'rightHip_x', 'leftKnee_x', 'rightKnee_x', 'leftAnkle_x', 'rightAnkle_x', 'nose_y', 'leftEye_y', 'rightEye_y', 'leftEar_y', 'rightEar_y', 'leftShoulder_y', 'rightShoulder_y', 'leftElbow_y', 'rightElbow_y', 'leftWrist_y', 'rightWrist_y', 'leftHip_y', 'rightHip_y', 'leftKnee_y', 'rightKnee_y', 'leftAnkle_y', 'rightAnkle_y']
        output_data = pd.concat([varX, varY], ignore_index = True)  
        output_data = output_data.apply(pd.to_numeric, errors = 'coerce')
        output_data = output_data.transpose()
        output_data.columns = columns

        return output_data

    def predict(self, data):
        # result = self.make_data(data)
        y_pred = self.loaded_model.predict(data)
        predictions = [round(value) for value in y_pred]
        return predictions
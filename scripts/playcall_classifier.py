# uses data found in the nfl_data_py package (https://pypi.org/project/nfl-data-py/)


import nfl_data_py as nfl
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.neural_network import MLPClassifier

years = [2020, 2021]
#[print(col) for col in nfl.see_pbp_cols()]
columns = ["play_id", "game_id", "posteam_type", "yardline_100", "quarter_seconds_remaining", "down", "half_seconds_remaining", "game_seconds_remaining", "goal_to_go", "ydstogo", "score_differential", "play_type"]
data = nfl.import_pbp_data(years, columns)
X = data[columns].drop(['play_id', 'game_id', 'play_type'], axis=1)
y = data["play_type"]
posession_le = LabelEncoder()
X['posteam_type'] = posession_le.fit_transform(X['posteam_type'])
class_le = LabelEncoder()
y = class_le.fit_transform(y)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=39)

global rf
rf = RandomForestClassifier(n_estimators=50)
rf.fit(X_train, y_train)
predictions = rf.predict(X_test)

def decide_next_play(game_situation, classifier = rf, label_encoder = class_le):
    """Purpose: Decide what type of play to call next (i.e., run, pass, punt, field_goal, etc.) given a vector 
    representing the team with posession, yard line, down, distance, time remaining"""
    return class_le.inverse_transform(classifier.predict(game_situation))[0]

error_rate = len([i for i in range(len(predictions)) if predictions[i] != y_test[i]]) / len(y_test)
run_pass_error_rate = len([i for i in range(len(predictions)) if (y_test[i] in class_le.transform(['pass', 'run'])) and y_test[i] != predictions[i]]) / len(y_test)


print("RF Error rate", error_rate, "RF Run-pass error rate:", run_pass_error_rate)
# Subsequent experimental classifiers are commented out because they did performed worse than RF.

"""
run_pass_data = (data[columns].drop(['play_id', 'game_id'], axis=1)[data["play_type"].isin(['pass', 'run'])]).dropna()
run_pass_X = run_pass_data.drop(['play_type'], axis=1)
run_pass_X['posteam_type'] = LabelEncoder().fit_transform(run_pass_X['posteam_type'])
run_pass_y = run_pass_data['play_type']
run_pass_le = LabelEncoder()
run_pass_y = run_pass_le.fit_transform(run_pass_y)
rp_X_train, rp_X_test, rp_y_train, rp_y_test = train_test_split(run_pass_X, run_pass_y, test_size=0.2, random_state=39)


lr = LogisticRegression(C=0.01, max_iter=10000)
lr.fit(rp_X_train, rp_y_train)
lr_predictions = lr.predict(rp_X_test)
lr_error_rate = len([i for i in range(len(lr_predictions)) if lr_predictions[i] != rp_y_test[i]]) / len(rp_y_test)
print("Logistic regression run-pass error rate:", lr_error_rate) """
# Logistic regression run-pass error rate: 0.34105580261081625

""" mlp = MLPClassifier(hidden_layer_sizes=(64, 32, 16, 8))
mlp.fit(rp_X_train, rp_y_train)
mlp_predictions = mlp.predict(rp_X_test)

mlp_run_pass_error_rate = len([i for i in range(len(mlp_predictions)) if mlp_predictions[i] != rp_y_test[i]]) / len(rp_y_test)
print("MLP Run-pass error rate:", mlp_run_pass_error_rate) """
# MLP Run-pass error rate: 0.33990819107732034


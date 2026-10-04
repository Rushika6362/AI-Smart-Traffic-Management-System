from sklearn.ensemble import RandomForestRegressor
import numpy as np

def predict_traffic(current_count):

    prediction = current_count + 10

    return prediction
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.gaussian_process import GaussianProcessRegressor
from datautils import DataRetriever


class AirPollutionModel:
    def __init__(self):
        self.data = DataRetriever()
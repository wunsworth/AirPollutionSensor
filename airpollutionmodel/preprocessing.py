from calibration.dataprocessing import loaddata
#import airpollutionmodel as a
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px

def within_dist(lat, lon, limit, data):
    dist = np.sqrt((data['latitude'] - lat)**2 + (data['longitude'] - lon)**2)
    return dist < limit

def get_data(path, isAveraged, window):
    data = pd.read_csv(path)
    data = data[within_dist(0.1849, 32.3452, .3, data)]
    data['created_at'] = pd.to_datetime(data['created_at'], infer_datetime_format = True)
    data = data.sort_values(by = 'created_at').reindex()
    if isAveraged:
        data = average_data(data, window)
    return data

def average_data(data, window):
    if window == 'hour':
        averaged_data = data.groupby([data['channel_id'], data['created_at'].dt.date, data['created_at'].dt.hour]).mean()
        averaged_data.index.names = ['channel_id', 'date', 'hour']
    elif window == 'day':
        averaged_data = data.groupby([data['channel_id'], data['created_at'].dt.date]).mean()
        averaged_data.index.names = ['channel_id', 'date', 'hour']
    else:
        averaged_data = data
    averaged_data.reset_index(inplace = True)
    averaged_data['created_at'] = pd.to_datetime(averaged_data['date']) + pd.to_timedelta(averaged_data['hour'], 'h')
    averaged_data = averaged_data.drop(['date', 'hour'], axis = 1)
    return averaged_data

def plot_channel(data, channels, path = False):
    if type(channels) == str:
        channels = [channels]
    channel_data = data[data['channel_id'].isin(channels)]
    if path:
        fig = px.line_mapbox(channel_data, lat="latitude", lon="longitude", color = 'channel_id', hover_name="channel_id", hover_data=['created_at', 'pm2_5'],
                            zoom=11, height=100, line_group = 'channel_id')
    else:
        fig = px.scatter_mapbox(channel_data, lat="latitude", lon="longitude", color = 'channel_id', hover_name="channel_id", hover_data=['created_at', 'pm2_5'],
                            zoom=11, height=300)
        
    fig.update_layout(mapbox_style="open-street-map",
                      margin={"r":0,"t":0,"l":0,"b":0},
                      width = 900,
                      height = 600)
    fig.show()
import json
from datetime import *
import numpy as np
import pandas as pd

class Sensor:
    """ A sensor class containing ID, location, readings etc.
    
    This class is a parent class for our three types of sensors: high-cost static, low-cost static, and low-cost mobile.
    These objects are intended to form the class structure of part of our Network class.

    Attributes:
        ID: the unique ID of the sensor (str)
        sensorType: the type of sensor (high, low, mobile) (str)
        latitude: the latitude coordinate of the sensor (float)
        longitude: the longitude coordinate of the sensor (float)
        readings: the readings taken from the sensor indexed by datetime (dict)
        calibrations: a record of when the sensor has been calibrated indexed by datetime (dict)
    """
    def __init__(self, ID, sensorType, latitude, longitude):
        self.ID = ID
        self.sensorType = sensorType
        self.latitude = latitude
        self.longitude = longitude

    def __repr__(self):
        return self.as_JSON()

    def data(self, network):
        return network.data[network.data['channel_id'] == self.ID]

    def as_JSON(self):
        d = {
        'ID': int(self.ID),
        'sensorType': str(self.sensorType),
        'latitude': float(self.latitude),
        'longitude': float(self.longitude)
        }

        return json.dumps(d, indent = 4) # json doesn't recognise np datatypes, so need to convert.

class Network:
    """ Describes a sensor network.

    Attributes:
        sensors: a list of Sensor objects, these can be of any type. (list(Sensor))
        IDs: a list of the IDs of the Sensor objects, these can be useful for iterating over.
        data: the dataframe associated with the object
    """
    def __init__(self, data = None):
        self.IDs = []
        self.sensors = dict()
        self.data = None
        self.size = len(self.IDs)
        if data is not None:
            self.from_df(data)
    
    def add_sensors(self, *sensors):
        """ Takes either a Sensor object or a list of Sensor objects and adds them to the network

        Args:
            sensors: a Sensor object or list of Sensor objects to be added. (Sensor/list(Sensor))

        Returns:
            None            
        """
        for sensor in sensors:
            self.sensors[sensor.ID] = sensor
            self.IDs.append(sensor.ID)

    def from_df(self, df):
        """ Takes a pandas dataframe and returns all the data for the sensors in our network

        Args:
            self: the Network object containing our Sensors
            df: the pandas dataframe containing all the data

        Returns:
            None
        """
        self.IDs = list(df['channel_id'].unique())
        self.data = df
        self.sensors = {}
        for ID in self.IDs:
            sensor_data = df[df['channel_id'] == ID]
            if sensor_data['latitude'].var() < 0.1: # 0.1 is a placeholder, this needs tuning.
                self.sensors[ID] = Sensor(ID, 'static', sensor_data['latitude'].mean(), sensor_data['longitude'].mean())
            else:
                self.sensors[ID] = Sensor(ID, 'mobile', None, None)